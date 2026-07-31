from __future__ import annotations

import sys
from pathlib import Path

import pytest

_SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from govern_bench import harness as harness_module  # noqa: E402
from govern_bench.conditions import CONDITION_MAP  # noqa: E402
from govern_bench.harness import (  # noqa: E402
    _active_tool_names,
    _build_active_tools,
    _capture_repair_checkpoint,
    _restore_repair_checkpoint,
)
from govern_bench.metrics import RunResult  # noqa: E402
from govern_bench.profiles import PROFILES  # noqa: E402
from govern_bench.protocol import validate_run_contract  # noqa: E402
from govern_bench.run_bench import _policy_rows, _validate_controller_features  # noqa: E402
from govern_bench.tasks import BenchTask  # noqa: E402

from specsmith.benchmark_audit import _condition_rollups  # noqa: E402


def _task() -> BenchTask:
    return BenchTask(
        id="TV9",
        title="Repair release status",
        category="coding",
        difficulty="medium",
        project="fixture",
        task_prompt="Repair release status and its tests.",
        acceptance_criteria="Public tests pass.",
        expected_files_changed=["service.py", "test_service.py"],
    )


def test_v9_1_protocol_freezes_route_controller_and_feature_cell() -> None:
    protocol_id, digest = validate_run_contract(
        profile="literature-v9-ablation",
        tasks=["T28", "T29", "T30"],
        conditions=["SPECSMITH_FULL"],
        repetitions=1,
        provider="openai-responses",
        model="gpt-5.6-sol",
        controller="scalar-milestone-packet-authority-v9",
        controller_features="retrieval,lanes",
    )

    assert protocol_id == "GB-LITERATURE-V9.1-2026-07-31"
    assert len(digest) == 64


def test_v9_tool_surface_keeps_exact_evidence_retrieval(monkeypatch) -> None:
    monkeypatch.setenv(
        "BENCH_CONTROLLER_EXPERIMENT",
        "scalar-milestone-packet-authority-v9",
    )
    tools = _build_active_tools("SPECSMITH_FULL", _task())
    assert _active_tool_names(tools) == {
        "write_file",
        "write_milestone",
        "patch_file",
        "read_evidence",
        "done",
    }


def test_v9_features_are_independently_ablatable(monkeypatch) -> None:
    monkeypatch.setenv(
        "BENCH_CONTROLLER_EXPERIMENT",
        "scalar-milestone-packet-authority-v9",
    )
    monkeypatch.setenv("BENCH_CONTROLLER_FEATURES", "retrieval")
    assert "read_evidence" not in _active_tool_names(_build_active_tools("SPECSMITH_FULL", _task()))


def test_v9_profiles_gate_n1_n5_n10_replication() -> None:
    assert PROFILES["literature-v9-ablation"].repetitions == 1
    assert PROFILES["literature-v9-screen"].repetitions == 5
    assert PROFILES["literature-v9-release"].repetitions == 10
    assert PROFILES["literature-v9-release"].tasks == ("T28", "T29", "T30")


def test_v9_feature_selection_fails_closed() -> None:
    assert _validate_controller_features(" early-stop, critical-replay ") == (
        "early-stop,critical-replay"
    )
    with pytest.raises(ValueError, match="requires early-stop"):
        _validate_controller_features("critical-replay")
    with pytest.raises(ValueError, match="unknown controller features"):
        _validate_controller_features("retrieval,imaginary")


def test_v9_rollups_measure_failed_tokens_context_and_handoffs() -> None:
    rollup = _condition_rollups(
        [
            {
                "condition": "SPECSMITH_FULL",
                "passed": True,
                "input_tokens": 80,
                "output_tokens": 20,
                "llm_turns": 2,
                "working_context_peak_chars": 20_000,
                "working_context_pruned_chars": 5_000,
                "stop_reason": "done",
            },
            {
                "condition": "SPECSMITH_FULL",
                "passed": False,
                "input_tokens": 40,
                "output_tokens": 10,
                "llm_turns": 3,
                "working_context_peak_chars": 18_000,
                "working_context_pruned_chars": 4_000,
                "stop_reason": "milestone_escalation",
            },
        ]
    )["SPECSMITH_FULL"]
    assert rollup["failed_token_share"] == pytest.approx(1 / 3, abs=1e-6)
    assert rollup["milestone_escalation_rate"] == 0.5
    assert rollup["mean_working_context_pruned_chars"] == 4500


def test_policy_rows_retain_route_and_controller_provenance() -> None:
    rows = _policy_rows(
        [
            {
                "task": "T30",
                "condition": "SPECSMITH_FULL",
                "model": "small-model",
                "provider": "huggingface",
                "rep": 1,
                "controller_experiment": "scalar-milestone-packet-authority-v9",
                "controller_features": "all",
                "policy_examples": [
                    {"features": {"turn": 2}, "label": "replay", "reason": "repeat"}
                ],
            }
        ]
    )
    assert rows[0]["task"] == "T30"
    assert rows[0]["provider"] == "huggingface"
    assert rows[0]["label"] == "replay"


def test_critical_replay_restores_only_the_focused_boundary(tmp_path: Path) -> None:
    focused = tmp_path / "service.py"
    unrelated = tmp_path / "README.md"
    focused.write_text("VALUE = 'failing'\n", encoding="utf-8")
    unrelated.write_text("keep\n", encoding="utf-8")
    checkpoint = _capture_repair_checkpoint(tmp_path, ["service.py"], "sig")

    focused.write_text("VALUE = 'candidate-one'\n", encoding="utf-8")
    unrelated.write_text("changed elsewhere\n", encoding="utf-8")
    assert _restore_repair_checkpoint(tmp_path, checkpoint) == ["service.py"]

    assert focused.read_text(encoding="utf-8") == "VALUE = 'failing'\n"
    assert unrelated.read_text(encoding="utf-8") == "changed elsewhere\n"


def test_run_task_cascades_from_handoff_without_restarting(
    tmp_path: Path,
    monkeypatch,
) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "service.py").write_text("VALUE = 1\n", encoding="utf-8")
    calls: list[dict] = []

    monkeypatch.setattr(harness_module, "_get_project_dir", lambda _project: source)
    monkeypatch.setattr(
        harness_module,
        "_build_provider_client",
        lambda provider, base_url=None: (provider, object()),
    )

    def fake_loop(**kwargs):
        calls.append(kwargs)
        if kwargs.get("resume_handoff") is None:
            return RunResult(
                task_id="TV9",
                condition_id="SPECSMITH_FULL",
                rep=1,
                model="small-model",
                input_tokens=100,
                output_tokens=20,
                api_cost_usd=0.01,
                llm_turns=3,
                handoff={
                    "task_id": "TV9",
                    "reason": "stalled milestone",
                    "files_written": ["service.py"],
                    "validator_failures": ["pytest failed"],
                },
                agent_transcript=[{"role": "controller", "first": True}],
            )
        return RunResult(
            task_id="TV9",
            condition_id="SPECSMITH_FULL",
            rep=1,
            model="gpt-5.6-sol",
            input_tokens=40,
            output_tokens=10,
            api_cost_usd=0.02,
            lint_passed=True,
            tests_passed=True,
            llm_turns=2,
            files_written=["service.py", "test_service.py"],
            agent_transcript=[{"role": "controller", "second": True}],
        )

    monkeypatch.setattr(harness_module, "_run_agent_loop", fake_loop)
    result = harness_module.run_task(
        _task(),
        CONDITION_MAP["SPECSMITH_FULL"],
        model="small-model",
        provider="huggingface",
        escalation_model="gpt-5.6-sol",
        escalation_provider="openai-responses",
    )

    assert len(calls) == 2
    assert calls[0]["defer_hidden_oracle"] is True
    assert calls[1]["resume_handoff"]["files_written"] == ["service.py"]
    assert result.model == "small-model->gpt-5.6-sol"
    assert result.input_tokens == 140
    assert result.output_tokens == 30
    assert result.api_cost_usd == 0.03
    assert result.llm_turns == 5
    assert result.passed is True
    assert any("cascade" in event for event in result.agent_transcript)
