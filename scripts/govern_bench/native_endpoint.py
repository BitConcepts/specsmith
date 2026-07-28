"""Provision a short-lived native-Qwen Hugging Face Inference Endpoint.

The endpoint is intentionally ephemeral: deployment is bounded, a live tool
call proves that vLLM's native parser emits valid OpenAI tool calls, and cleanup
pauses before deleting only names created with this module's guarded prefix.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import time
import urllib.error
import urllib.request
from collections.abc import Callable
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ENDPOINT_PREFIX = "specsmith-qwen-native-"
DEFAULT_MODEL = "Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8"
DEFAULT_IMAGE = "vllm/vllm-openai:v0.24.0"
DEFAULT_TOOL_PARSER = "qwen3_xml"
DEFAULT_HOURLY_COST_USD = 1.80
TERMINAL_FAILURE_STATES = frozenset(
    {
        "failed",
        "updatefailed",
        "paused",
        "scaledtozero",
    }
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(moment: datetime) -> str:
    return moment.isoformat().replace("+00:00", "Z")


def guarded_endpoint_name(value: str) -> str:
    """Return a safe ephemeral endpoint name or fail before any mutation."""
    normalized = re.sub(r"[^a-z0-9-]+", "-", value.casefold()).strip("-")
    if not normalized.startswith(ENDPOINT_PREFIX):
        raise ValueError(f"endpoint name must start with {ENDPOINT_PREFIX!r}")
    if len(normalized) > 63:
        raise ValueError("endpoint name must be at most 63 characters")
    return normalized


def deployment_kwargs(
    *,
    model: str = DEFAULT_MODEL,
    image: str = DEFAULT_IMAGE,
    tool_parser: str = DEFAULT_TOOL_PARSER,
    instance_type: str = "nvidia-l40s",
    instance_size: str = "x1",
) -> dict[str, Any]:
    """Build the pinned, auditable native parser deployment specification."""
    if tool_parser not in {"qwen3_xml", "qwen3_coder"}:
        raise ValueError("tool parser must be qwen3_xml or qwen3_coder")
    return {
        "repository": model,
        "framework": "custom",
        "task": "text-generation",
        "accelerator": "gpu",
        "vendor": "aws",
        "region": "us-east-1",
        "type": "authenticated",
        "instance_type": instance_type,
        "instance_size": instance_size,
        "min_replica": 1,
        "max_replica": 1,
        "scale_to_zero_timeout": 15,
        "custom_image": {
            "healthRoute": "/health",
            "url": image,
        },
        # vllm/vllm-openai uses `vllm serve` as its entrypoint. Hugging Face
        # mounts the selected model at /repository.
        "container_args": [
            "/repository",
            "--served-model-name",
            model,
            "--host",
            "0.0.0.0",
            "--port",
            "80",
            "--max-model-len",
            "32768",
            "--gpu-memory-utilization",
            "0.90",
            "--enable-auto-tool-choice",
            "--tool-call-parser",
            tool_parser,
        ],
        "tags": [
            "specsmith",
            "governancebench",
            "native-qwen-parser",
            tool_parser,
        ],
    }


def wait_for_running(
    api: Any,
    name: str,
    *,
    namespace: str | None,
    token: str,
    timeout_s: float,
    poll_s: float = 15.0,
    monotonic: Callable[[], float] = time.monotonic,
    sleep: Callable[[float], None] = time.sleep,
) -> Any:
    """Poll endpoint state until running, terminal failure, or deadline."""
    deadline = monotonic() + timeout_s
    last_status = "unknown"
    while monotonic() < deadline:
        endpoint = api.get_inference_endpoint(name, namespace=namespace, token=token)
        last_status = str(getattr(endpoint, "status", "unknown") or "unknown")
        normalized = last_status.replace("_", "").casefold()
        if normalized == "running" and getattr(endpoint, "url", None):
            return endpoint
        if normalized in TERMINAL_FAILURE_STATES:
            raw = getattr(endpoint, "raw", {})
            raise RuntimeError(
                f"endpoint entered terminal state {last_status!r}: "
                f"{json.dumps(raw, default=str)[:600]}"
            )
        sleep(min(poll_s, max(0.0, deadline - monotonic())))
    raise TimeoutError(
        f"endpoint {name!r} did not become running within {timeout_s:g}s "
        f"(last status: {last_status})"
    )


def _post_json(
    url: str,
    *,
    token: str,
    payload: dict[str, Any],
    timeout_s: float,
) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout_s) as response:  # noqa: S310
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"native parser probe HTTP {exc.code}: {body[:600]}") from exc


def probe_native_tool_parser(
    base_url: str,
    *,
    model: str,
    token: str,
    timeout_s: float,
    post: Callable[..., dict[str, Any]] = _post_json,
) -> dict[str, Any]:
    """Prove the deployed parser emits a valid native tool call."""
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": "Call record_probe exactly once with value native-qwen.",
            }
        ],
        "tools": [
            {
                "type": "function",
                "function": {
                    "name": "record_probe",
                    "description": "Record the native parser compatibility probe.",
                    "strict": True,
                    "parameters": {
                        "type": "object",
                        "properties": {"value": {"type": "string"}},
                        "required": ["value"],
                        "additionalProperties": False,
                    },
                },
            }
        ],
        "tool_choice": "required",
        "temperature": 0,
        "max_tokens": 128,
    }
    data = post(
        f"{base_url.rstrip('/')}/chat/completions",
        token=token,
        payload=payload,
        timeout_s=timeout_s,
    )
    choices = data.get("choices") or []
    message = (choices[0].get("message") or {}) if choices else {}
    calls = message.get("tool_calls") or []
    if len(calls) != 1:
        raise RuntimeError(f"native parser probe returned {len(calls)} tool calls, expected one")
    function = calls[0].get("function") or {}
    if function.get("name") != "record_probe":
        raise RuntimeError("native parser probe returned the wrong tool name")
    arguments = json.loads(str(function.get("arguments") or "{}"))
    if arguments != {"value": "native-qwen"}:
        raise RuntimeError(f"native parser probe returned invalid arguments: {arguments!r}")
    usage = data.get("usage") or {}
    return {
        "passed": True,
        "finish_reason": choices[0].get("finish_reason"),
        "prompt_tokens": int(usage.get("prompt_tokens") or 0),
        "completion_tokens": int(usage.get("completion_tokens") or 0),
    }


def deploy(
    *,
    name: str,
    output: Path,
    model: str,
    image: str,
    tool_parser: str,
    deploy_timeout_s: float,
    probe_timeout_s: float,
    token: str,
) -> dict[str, Any]:
    """Create, await, probe, and receipt one native-Qwen endpoint."""
    from huggingface_hub import HfApi  # noqa: PLC0415

    safe_name = guarded_endpoint_name(name)
    api = HfApi(token=token)
    namespace = str(api.whoami(token=token).get("name") or "")
    if not namespace:
        raise RuntimeError("could not resolve the Hugging Face token namespace")
    created_at = _utc_now()
    spec = deployment_kwargs(model=model, image=image, tool_parser=tool_parser)
    api.create_inference_endpoint(
        safe_name,
        namespace=namespace,
        token=token,
        **spec,
    )
    endpoint = wait_for_running(
        api,
        safe_name,
        namespace=namespace,
        token=token,
        timeout_s=deploy_timeout_s,
    )
    running_at = _utc_now()
    base_url = f"{str(endpoint.url).rstrip('/')}/v1"
    probe = probe_native_tool_parser(
        base_url,
        model=model,
        token=token,
        timeout_s=probe_timeout_s,
    )
    receipt = {
        "endpoint_name": safe_name,
        "namespace": namespace,
        "model": model,
        "engine": "vllm",
        "engine_image": image,
        "tool_parser": tool_parser,
        "instance_type": spec["instance_type"],
        "instance_size": spec["instance_size"],
        "hourly_cost_usd": DEFAULT_HOURLY_COST_USD,
        "created_at": _iso(created_at),
        "running_at": _iso(running_at),
        "deployment_seconds": round((running_at - created_at).total_seconds(), 3),
        "base_url": base_url,
        "native_tool_probe": probe,
    }
    output.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return receipt


def _pause_and_delete(
    api: Any,
    *,
    name: str,
    namespace: str,
    token: str,
) -> tuple[bool, bool, str]:
    """Attempt both cleanup operations so a pause error cannot skip deletion."""
    paused = False
    deleted = False
    errors: list[str] = []
    try:
        api.pause_inference_endpoint(name, namespace=namespace, token=token)
        paused = True
    except Exception as exc:  # noqa: BLE001
        errors.append(f"pause: {type(exc).__name__}: {exc}")
    try:
        api.delete_inference_endpoint(name, namespace=namespace, token=token)
        deleted = True
    except Exception as exc:  # noqa: BLE001
        errors.append(f"delete: {type(exc).__name__}: {exc}")
    return paused, deleted, "; ".join(errors)


def cleanup(
    *,
    name: str,
    output: Path,
    token: str,
    deployment_receipt: Path | None = None,
) -> dict[str, Any]:
    """Pause and delete one guarded ephemeral endpoint."""
    from huggingface_hub import HfApi  # noqa: PLC0415

    safe_name = guarded_endpoint_name(name)
    api = HfApi(token=token)
    namespace = str(api.whoami(token=token).get("name") or "")
    paused, deleted, error = _pause_and_delete(
        api,
        name=safe_name,
        namespace=namespace,
        token=token,
    )

    cleaned_at = _utc_now()
    created_at: datetime | None = None
    if deployment_receipt is not None and deployment_receipt.exists():
        prior = json.loads(deployment_receipt.read_text(encoding="utf-8"))
        raw_created = str(prior.get("created_at") or "").replace("Z", "+00:00")
        if raw_created:
            created_at = datetime.fromisoformat(raw_created)
    billed_seconds = max(0.0, (cleaned_at - created_at).total_seconds()) if created_at else None
    receipt = {
        "endpoint_name": safe_name,
        "namespace": namespace,
        "paused": paused,
        "deleted": deleted,
        "cleaned_at": _iso(cleaned_at),
        "approximate_billed_seconds": round(billed_seconds, 3)
        if billed_seconds is not None
        else None,
        "approximate_endpoint_cost_usd": round(
            billed_seconds / 3_600 * DEFAULT_HOURLY_COST_USD,
            6,
        )
        if billed_seconds is not None
        else None,
        "error": error or None,
    }
    output.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    if not deleted:
        raise RuntimeError(error or "endpoint cleanup did not confirm deletion")
    return receipt


def _token() -> str:
    token = os.environ.get("HF_TOKEN", "").strip()
    if not token:
        raise RuntimeError("HF_TOKEN is required")
    return token


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    deploy_parser = subparsers.add_parser("deploy")
    deploy_parser.add_argument("--name", required=True)
    deploy_parser.add_argument("--output", type=Path, required=True)
    deploy_parser.add_argument("--model", default=DEFAULT_MODEL)
    deploy_parser.add_argument("--image", default=DEFAULT_IMAGE)
    deploy_parser.add_argument(
        "--tool-parser",
        choices=("qwen3_xml", "qwen3_coder"),
        default=DEFAULT_TOOL_PARSER,
    )
    deploy_parser.add_argument("--deploy-timeout-s", type=float, default=1_200)
    deploy_parser.add_argument("--probe-timeout-s", type=float, default=120)

    cleanup_parser = subparsers.add_parser("cleanup")
    cleanup_parser.add_argument("--name", required=True)
    cleanup_parser.add_argument("--output", type=Path, required=True)
    cleanup_parser.add_argument("--deployment-receipt", type=Path)
    return parser


def main() -> int:
    args = _parser().parse_args()
    if args.command == "deploy":
        receipt = deploy(
            name=args.name,
            output=args.output,
            model=args.model,
            image=args.image,
            tool_parser=args.tool_parser,
            deploy_timeout_s=args.deploy_timeout_s,
            probe_timeout_s=args.probe_timeout_s,
            token=_token(),
        )
    else:
        receipt = cleanup(
            name=args.name,
            output=args.output,
            deployment_receipt=args.deployment_receipt,
            token=_token(),
        )
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
