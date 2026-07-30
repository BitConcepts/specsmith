from __future__ import annotations

import json
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

_SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

import govern_bench.native_endpoint as native_endpoint  # noqa: E402
from govern_bench.native_endpoint import (  # noqa: E402
    DEFAULT_IMAGE,
    DEFAULT_MODEL,
    DEFAULT_TOOL_PARSER,
    NATIVE_PROBE_MAX_TOKENS,
    _pause_and_delete,
    deployment_kwargs,
    guarded_endpoint_name,
    probe_native_tool_parser,
    wait_for_running,
)


def test_deployment_spec_pins_native_parser_and_bounded_context() -> None:
    spec = deployment_kwargs()

    assert spec["repository"] == DEFAULT_MODEL
    assert spec["custom_image"]["url"] == DEFAULT_IMAGE
    assert spec["min_replica"] == spec["max_replica"] == 1
    assert "scale_to_zero_timeout" not in spec
    assert spec["type"] == "authenticated"
    assert spec["container_args"][0] == "/repository"
    assert spec["container_args"][-2:] == ["--tool-call-parser", DEFAULT_TOOL_PARSER]
    assert spec["container_args"][7:9] == ["--max-model-len", "32768"]


@pytest.mark.parametrize(
    "model",
    (
        "Qwen/Qwen3.6-27B-FP8",
        "Qwen/Qwen3.6-35B-A3B-FP8",
    ),
)
def test_qwen36_spec_uses_official_parser_and_bounded_a100_profile(model: str) -> None:
    spec = deployment_kwargs(
        model=model,
        tool_parser="qwen3_coder",
        reasoning_parser="qwen3",
        language_model_only=True,
        instance_type="nvidia-a100",
        max_model_len=32_768,
    )

    assert spec["instance_type"] == "nvidia-a100"
    assert spec["instance_size"] == "x1"
    assert spec["container_args"][7:9] == ["--max-model-len", "32768"]
    assert "--language-model-only" in spec["container_args"]
    assert spec["container_args"][
        spec["container_args"].index("--reasoning-parser") : spec["container_args"].index(
            "--reasoning-parser"
        )
        + 2
    ] == ["--reasoning-parser", "qwen3"]
    assert spec["container_args"][-2:] == ["--tool-call-parser", "qwen3_coder"]


def test_deployment_spec_rejects_unbounded_compute_and_context() -> None:
    with pytest.raises(ValueError, match="instance type"):
        deployment_kwargs(instance_type="unbounded-gpu")
    with pytest.raises(ValueError, match="model length"):
        deployment_kwargs(max_model_len=1_000_000)
    with pytest.raises(ValueError, match="reasoning parser"):
        deployment_kwargs(reasoning_parser="untrusted")


def test_endpoint_name_guard_rejects_unscoped_mutation_targets() -> None:
    assert guarded_endpoint_name("specsmith-qwen-native-123") == "specsmith-qwen-native-123"
    with pytest.raises(ValueError, match="must start"):
        guarded_endpoint_name("production-endpoint")
    with pytest.raises(ValueError, match="at most 63"):
        guarded_endpoint_name("specsmith-qwen-native-" + ("x" * 60))


class _FakeEndpointApi:
    def __init__(self, endpoints: list[Any]) -> None:
        self.endpoints = endpoints
        self.calls = 0

    def get_inference_endpoint(self, *_args: Any, **_kwargs: Any) -> Any:
        endpoint = self.endpoints[min(self.calls, len(self.endpoints) - 1)]
        self.calls += 1
        return endpoint


def test_wait_for_running_obeys_deadline_and_terminal_states() -> None:
    now = [0.0]

    def sleep(seconds: float) -> None:
        now[0] += seconds

    api = _FakeEndpointApi(
        [
            SimpleNamespace(status="pending", url=None, raw={}),
            SimpleNamespace(status="running", url="https://native.example", raw={}),
        ]
    )
    endpoint = wait_for_running(
        api,
        "specsmith-qwen-native-1",
        namespace="owner",
        token="token",
        timeout_s=5,
        poll_s=1,
        monotonic=lambda: now[0],
        sleep=sleep,
    )
    assert endpoint.url == "https://native.example"

    failed_api = _FakeEndpointApi(
        [SimpleNamespace(status="updateFailed", url=None, raw={"message": "OOM"})]
    )
    with pytest.raises(RuntimeError, match="terminal state"):
        wait_for_running(
            failed_api,
            "specsmith-qwen-native-2",
            namespace="owner",
            token="token",
            timeout_s=5,
            monotonic=lambda: 0,
            sleep=lambda _seconds: None,
        )

    timeout_now = [0.0]
    pending_api = _FakeEndpointApi([SimpleNamespace(status="pending", url=None, raw={})])
    with pytest.raises(TimeoutError, match="within 1s"):
        wait_for_running(
            pending_api,
            "specsmith-qwen-native-3",
            namespace="owner",
            token="token",
            timeout_s=1,
            monotonic=lambda: timeout_now[0],
            sleep=lambda seconds: timeout_now.__setitem__(0, timeout_now[0] + seconds),
        )


def test_native_parser_probe_requires_exact_structured_tool_call() -> None:
    captured: dict[str, Any] = {}

    def post(url: str, **kwargs: Any) -> dict[str, Any]:
        captured.update({"url": url, **kwargs})
        return {
            "choices": [
                {
                    "finish_reason": "tool_calls",
                    "message": {
                        "tool_calls": [
                            {
                                "function": {
                                    "name": "record_probe",
                                    "arguments": '{"value":"native-qwen"}',
                                }
                            }
                        ]
                    },
                }
            ],
            "usage": {"prompt_tokens": 20, "completion_tokens": 8},
        }

    result = probe_native_tool_parser(
        "https://native.example/v1",
        model=DEFAULT_MODEL,
        token="token",
        timeout_s=12,
        post=post,
    )

    assert result == {
        "passed": True,
        "finish_reason": "tool_calls",
        "prompt_tokens": 20,
        "completion_tokens": 8,
    }
    assert captured["url"] == "https://native.example/v1/chat/completions"
    assert captured["timeout_s"] == 12
    assert captured["payload"]["tool_choice"] == "auto"
    assert captured["payload"]["max_tokens"] == NATIVE_PROBE_MAX_TOKENS == 2_048
    assert captured["payload"]["messages"][0]["role"] == "system"


def test_native_parser_probe_reports_compact_unparsed_response() -> None:
    def post(_url: str, **_kwargs: Any) -> dict[str, Any]:
        return {
            "choices": [
                {
                    "finish_reason": "stop",
                    "message": {
                        "content": "I should call record_probe.",
                        "reasoning_content": "The user requested a tool call.",
                    },
                }
            ]
        }

    with pytest.raises(RuntimeError, match='"finish_reason": "stop"') as exc_info:
        probe_native_tool_parser(
            "https://native.example/v1",
            model=DEFAULT_MODEL,
            token="token",
            timeout_s=12,
            post=post,
        )

    assert "I should call record_probe." in str(exc_info.value)
    assert "The user requested a tool call." in str(exc_info.value)


def test_failed_probe_preserves_deployment_and_cost_receipt(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    class Api:
        def __init__(self, **_kwargs: Any) -> None:
            pass

        def whoami(self, **_kwargs: Any) -> dict[str, str]:
            return {"name": "owner"}

        def create_inference_endpoint(self, *_args: Any, **_kwargs: Any) -> None:
            pass

    monkeypatch.setitem(sys.modules, "huggingface_hub", SimpleNamespace(HfApi=Api))
    monkeypatch.setattr(
        native_endpoint,
        "wait_for_running",
        lambda *_args, **_kwargs: SimpleNamespace(url="https://native.example"),
    )

    def fail_probe(*_args: Any, **_kwargs: Any) -> dict[str, Any]:
        raise RuntimeError("zero parsed calls")

    monkeypatch.setattr(native_endpoint, "probe_native_tool_parser", fail_probe)
    output = tmp_path / "receipt.json"

    with pytest.raises(RuntimeError, match="zero parsed calls"):
        native_endpoint.deploy(
            name="specsmith-qwen-native-receipt",
            output=output,
            model="Qwen/Qwen3.6-27B-FP8",
            image=DEFAULT_IMAGE,
            tool_parser="qwen3_coder",
            reasoning_parser="qwen3",
            language_model_only=True,
            instance_type="nvidia-a100",
            instance_size="x1",
            max_model_len=32_768,
            hourly_cost_usd=2.50,
            deploy_timeout_s=10,
            probe_timeout_s=10,
            token="token",
        )

    receipt = json.loads(output.read_text(encoding="utf-8"))
    assert receipt["hourly_cost_usd"] == 2.50
    assert receipt["created_at"]
    assert receipt["running_at"]
    assert receipt["native_tool_probe"] == {
        "passed": False,
        "status": "failed",
        "error": "RuntimeError: zero parsed calls",
    }


def test_cleanup_attempts_delete_even_when_pause_fails() -> None:
    calls: list[str] = []

    class Api:
        def pause_inference_endpoint(self, *_args: Any, **_kwargs: Any) -> None:
            calls.append("pause")
            raise RuntimeError("already paused")

        def delete_inference_endpoint(self, *_args: Any, **_kwargs: Any) -> None:
            calls.append("delete")

    paused, deleted, error = _pause_and_delete(
        Api(),
        name="specsmith-qwen-native-123",
        namespace="owner",
        token="token",
    )

    assert calls == ["pause", "delete"]
    assert not paused
    assert deleted
    assert "already paused" in error


def test_native_workflow_always_cleans_up_and_fails_closed() -> None:
    workflow = (
        Path(__file__).parent.parent / ".github" / "workflows" / "qwen-native-bench.yml"
    ).read_text(encoding="utf-8")

    assert "huggingface_hub==1.25.1" in workflow
    assert 'NATIVE_QWEN_TOOL_PARSER: "qwen3_xml"' in workflow
    assert "Qwen/Qwen3.6-27B-FP8" in workflow
    assert "Qwen/Qwen3.6-35B-A3B-FP8" in workflow
    assert "NATIVE_QWEN_REASONING_PARSER=qwen3" in workflow
    assert "NATIVE_QWEN_INSTANCE_TYPE=nvidia-a100" in workflow
    assert workflow.count("NATIVE_QWEN_MAX_MODEL_LEN=65536") == 2
    assert "--language-model-only" in workflow
    assert 'BENCH_PROVIDER_MAX_RETRIES: "0"' in workflow
    assert "- required-only" in workflow
    assert "- hybrid-v2-only" in workflow
    assert 'EXPERIMENTS="scalar-parallel-hybrid-v2"' in workflow
    assert '--reps "${{ inputs.repetitions }}"' in workflow
    assert 'EXPERIMENTS="scalar-native-patch-scoped-required"' in workflow
    assert "if: always()" in workflow
    assert "native_endpoint.py cleanup" in workflow
    assert "Fail closed on benchmark errors" in workflow
