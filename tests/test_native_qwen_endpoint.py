from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

_SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from govern_bench.native_endpoint import (  # noqa: E402
    DEFAULT_IMAGE,
    DEFAULT_MODEL,
    DEFAULT_TOOL_PARSER,
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
    assert captured["payload"]["tool_choice"] == "required"


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
    assert 'BENCH_PROVIDER_MAX_RETRIES: "0"' in workflow
    assert "- required-only" in workflow
    assert 'EXPERIMENTS="scalar-native-patch-scoped-required"' in workflow
    assert "if: always()" in workflow
    assert "native_endpoint.py cleanup" in workflow
    assert "Fail closed on benchmark errors" in workflow
