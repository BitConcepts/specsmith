from __future__ import annotations

import sys
from pathlib import Path

import pytest

from specsmith.benchmark_audit import audit_benchmark_rows

_SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from govern_bench import harness as harness_module  # noqa: E402
from govern_bench.harness import (  # noqa: E402
    NormalizedToolCall,
    _action_batch_signature,
    _active_boundary_has_current_evidence,
    _active_tool_names,
    _boundary_context_packet,
    _build_active_tools,
    _build_focused_repair_tools,
    _can_recover_nonterminal_narration,
    _cell_timeout_seconds,
    _compact_completed_boundary_context,
    _completed_milestone_count,
    _consolidate_write_receipts,
    _controller_experiment,
    _controller_tool_choice,
    _exec_edit_file,
    _exec_patch_file,
    _exec_read_file_with_evidence,
    _exec_read_files_with_evidence,
    _exec_write_files,
    _exec_write_milestone,
    _focused_validator_failures,
    _focused_validator_repair_boundaries,
    _focused_validator_repair_progress,
    _looks_like_nonterminal_narration,
    _milestone_contract,
    _milestone_progress,
    _milestone_work_packet,
    _next_incomplete_boundary_paths,
    _noop_action_signature,
    _openai_sampling_params,
    _openai_tools_to_responses,
    _provider_max_retries,
    _read_paths_from_calls,
    _record_written_evidence,
    _repair_failure_signature,
    _repeated_write_recovery,
    _replace_adaptive_progress_message,
    _request_timeout_seconds,
    _run_missing_completion_validators,
    _scope_contract,
    _scope_progress,
    _serialized_done_tool_call,
    _serialized_function_tool_call,
    _stable_repair_schema_experiment,
    _updated_repeated_action_batch_streak,
    _updated_repeated_noop_streak,
    _updated_repeated_write_streak,
    _updated_serialized_action_count,
    _updated_unchanged_read_only_streak,
    _write_paths_from_calls,
)
from govern_bench.metrics import estimate_cost, model_tier  # noqa: E402
from govern_bench.select_models import load_registry, select  # noqa: E402
from govern_bench.tasks import get_task  # noqa: E402


def test_unchanged_file_reads_return_digest_receipts_until_content_changes(
    tmp_path: Path,
) -> None:
    path = tmp_path / "component.py"
    path.write_text("VALUE = 1\n", encoding="utf-8")
    evidence: dict[str, tuple[str, int]] = {}

    first, first_suppressed = _exec_read_file_with_evidence(
        tmp_path, "component.py", evidence, turn=1, compress_unchanged=True
    )
    repeated, repeated_suppressed = _exec_read_file_with_evidence(
        tmp_path, "component.py", evidence, turn=2, compress_unchanged=True
    )
    path.write_text("VALUE = 2\n", encoding="utf-8")
    changed, changed_suppressed = _exec_read_file_with_evidence(
        tmp_path, "component.py", evidence, turn=3, compress_unchanged=True
    )

    assert first == "VALUE = 1\n"
    assert not first_suppressed
    assert repeated_suppressed
    assert "UNCHANGED" in repeated
    assert "VALUE = 1" not in repeated
    assert changed == "VALUE = 2\n"
    assert not changed_suppressed


def test_missing_file_reads_are_versioned_absence_evidence(tmp_path: Path) -> None:
    evidence: dict[str, tuple[str, int]] = {}
    first, first_suppressed = _exec_read_file_with_evidence(
        tmp_path,
        "new_test.py",
        evidence,
        turn=2,
        compress_unchanged=True,
    )
    repeated, repeated_suppressed = _exec_read_file_with_evidence(
        tmp_path,
        "new_test.py",
        evidence,
        turn=3,
        compress_unchanged=True,
    )

    assert first.startswith("ERROR: file not found:")
    assert not first_suppressed
    assert repeated_suppressed
    assert "remains absent" in repeated


def test_successful_model_writes_become_known_evidence(tmp_path: Path) -> None:
    path = tmp_path / "component.py"
    path.write_text("VALUE = 2\n", encoding="utf-8")
    evidence: dict[str, tuple[str, int]] = {}

    _record_written_evidence(tmp_path, ["component.py"], evidence, turn=4)
    repeated, suppressed = _exec_read_file_with_evidence(
        tmp_path,
        "component.py",
        evidence,
        turn=5,
        compress_unchanged=True,
    )

    assert suppressed
    assert "prior read from turn 4" in repeated
    assert "VALUE = 2" not in repeated


def test_repair_failure_signature_ignores_volatile_ids_and_numbers() -> None:
    first = _repair_failure_signature(
        ["pytest FAILED: tmp/run-123 expected 4 got 5 550e8400-e29b-41d4-a716-446655440000"]
    )
    equivalent = _repair_failure_signature(
        ["pytest FAILED: tmp/run-987 expected 8 got 9 123e4567-e89b-42d3-a456-426614174000"]
    )
    changed = _repair_failure_signature(["pytest FAILED: missing authorization boundary"])

    assert first == equivalent
    assert first != changed
    assert _repair_failure_signature([]) == ""


def test_repeated_write_streak_requires_success_and_unchanged_failure() -> None:
    boundary = ("backend/main.py",)

    assert _updated_repeated_write_streak(0, boundary, boundary, "same", "same") == 1
    assert _updated_repeated_write_streak(2, boundary, boundary, "changed", "old") == 0
    assert _updated_repeated_write_streak(2, (), boundary, "same", "same") == 2
    assert (
        _updated_repeated_write_streak(
            2,
            ("tests/test_backend.py",),
            boundary,
            "same",
            "same",
        )
        == 0
    )


def test_repeated_parallel_action_batch_stops_without_retaining_bodies() -> None:
    first = [
        NormalizedToolCall(
            id="write-1",
            name="write_file",
            arguments='{"path":"one.py","content":"PRIVATE BODY"}',
        ),
        NormalizedToolCall(
            id="patch-1",
            name="patch_file",
            arguments=('{"path":"two.py","old_text_1":"OLD PRIVATE","new_text_1":"NEW PRIVATE"}'),
        ),
    ]
    same = [
        NormalizedToolCall(id=call.id + "-again", name=call.name, arguments=call.arguments)
        for call in first
    ]
    changed = [
        NormalizedToolCall(
            id="write-2",
            name="write_file",
            arguments='{"path":"three.py","content":"DIFFERENT PRIVATE BODY"}',
        ),
        first[1],
    ]

    signature = _action_batch_signature(first)
    assert len(signature) == 16
    assert "PRIVATE" not in signature
    assert _action_batch_signature(same) == signature
    assert _updated_repeated_action_batch_streak(0, signature, signature) == 1
    assert (
        _updated_repeated_action_batch_streak(
            2,
            _action_batch_signature(changed),
            signature,
        )
        == 0
    )
    assert _action_batch_signature(first[:1]) == ""


def test_identical_single_action_noops_stop_after_one_recovery() -> None:
    call = NormalizedToolCall(
        id="patch-1",
        name="patch_file",
        arguments='{"path":"backend/main.py","old_text_1":"400","new_text_1":"422"}',
    )
    result = [{"role": "tool", "tool_call_id": "patch-1", "content": "NO-OP: already applied"}]
    signature = _noop_action_signature([call], result)

    assert signature
    assert _noop_action_signature([call], [{**result[0], "content": "OK: patched"}]) == ""
    first = _updated_repeated_noop_streak(0, signature, "")
    second = _updated_repeated_noop_streak(first, signature, signature)
    assert first == 1
    assert second == 2


def test_long_horizon_milestones_are_bounded_and_progress_replaces_history() -> None:
    task = get_task("T28")
    contract = _milestone_contract(task)
    tools = [
        tool["function"]["name"]
        for tool in _build_active_tools(
            "SPECSMITH_FULL",
            task,
            composite_files=task.is_long_horizon,
        )
    ]

    assert len(task.milestones) == 4
    assert "shared contract and API" in contract
    assert "interactive UI journey" in contract
    assert "no separate planning turn" in contract
    assert "supplies current content for each active milestone" in contract
    assert "validates completed milestones immediately" in contract
    assert "existing dependencies and standard libraries" in contract
    assert tools == ["read_files", "write_files", "read_file", "write_file", "done"]
    assert "backend/main.py" in _milestone_progress(task, ["contracts/incident.schema.json"])
    assert "worker boundary" in _milestone_progress(
        task,
        [
            "contracts/incident.schema.json",
            "backend/main.py",
            "tests/test_backend.py",
        ],
    )
    worker_paths = ["worker/main.go", "worker/main_test.go"]
    assert (
        _next_incomplete_boundary_paths(
            task,
            [
                "contracts/incident.schema.json",
                "backend/main.py",
                "tests/test_backend.py",
            ],
        )
        == worker_paths
    )
    evidence = {path: ("digest", 1) for path in worker_paths}
    assert _active_boundary_has_current_evidence(
        task,
        [
            "contracts/incident.schema.json",
            "backend/main.py",
            "tests/test_backend.py",
        ],
        evidence,
    )
    evidence.pop("worker/main_test.go")
    assert not _active_boundary_has_current_evidence(
        task,
        [
            "contracts/incident.schema.json",
            "backend/main.py",
            "tests/test_backend.py",
        ],
        evidence,
    )

    messages = _replace_adaptive_progress_message([], "first")
    messages = _replace_adaptive_progress_message(messages, "second")
    assert len(messages) == 1
    assert messages[0]["content"].endswith("second")


@pytest.mark.parametrize(
    ("experiment", "expected_tools", "tool_choice"),
    [
        (
            "control",
            ["read_files", "write_files", "read_file", "write_file", "done"],
            "auto",
        ),
        (
            "required-tools",
            ["read_files", "write_files", "read_file", "write_file", "done"],
            "required",
        ),
        ("scalar-parallel", ["read_file", "write_file", "done"], "auto"),
        ("scalar-parallel-required", ["read_file", "write_file", "done"], "required"),
        ("scalar-parallel-compact", ["read_file", "write_file", "done"], "required"),
        ("scalar-parallel-compact-auto", ["read_file", "write_file", "done"], "auto"),
        (
            "scalar-parallel-edit",
            ["read_file", "write_file", "edit_file", "done"],
            "auto",
        ),
        (
            "scalar-native-patch",
            ["read_file", "write_file", "patch_file", "done"],
            "auto",
        ),
        (
            "scalar-native-patch-scoped",
            ["write_file", "patch_file", "done"],
            "auto",
        ),
        (
            "scalar-native-patch-scoped-required",
            ["write_file", "patch_file", "done"],
            "required",
        ),
        ("scalar-parallel-write-only", ["write_file", "done"], "auto"),
        ("scalar-parallel-validator-authority", ["read_file", "write_file", "done"], "auto"),
        (
            "scalar-milestone-bundle",
            ["read_file", "write_file", "write_milestone", "done"],
            "auto",
        ),
        (
            "scalar-milestone-packet",
            ["write_file", "write_milestone", "done"],
            "auto",
        ),
        (
            "scalar-milestone-packet-adaptive",
            ["write_file", "write_milestone", "done"],
            "auto",
        ),
        (
            "scalar-milestone-packet-patch",
            ["write_file", "write_milestone", "patch_file", "done"],
            "auto",
        ),
        (
            "scalar-milestone-packet-authority",
            ["write_file", "write_milestone", "patch_file", "done"],
            "auto",
        ),
        (
            "scalar-milestone-packet-authority-v2",
            ["write_file", "write_milestone", "patch_file", "done"],
            "auto",
        ),
        (
            "scalar-milestone-packet-authority-v3",
            ["write_file", "write_milestone", "patch_file", "done"],
            "auto",
        ),
        (
            "scalar-milestone-packet-authority-v4",
            ["write_file", "write_milestone", "patch_file", "done"],
            "auto",
        ),
    ],
)
def test_controller_experiments_are_versioned_and_isolate_tool_protocol(
    monkeypatch: pytest.MonkeyPatch,
    experiment: str,
    expected_tools: list[str],
    tool_choice: str,
) -> None:
    monkeypatch.setenv("BENCH_CONTROLLER_EXPERIMENT", experiment)
    task = get_task("T28")

    assert _controller_experiment() == experiment
    assert [
        tool["function"]["name"] for tool in _build_active_tools("SPECSMITH_FULL", task)
    ] == expected_tools
    assert _controller_tool_choice("SPECSMITH_FULL", experiment) == tool_choice
    assert _controller_tool_choice("UNGOVERNED", experiment) == "auto"
    contract = _milestone_contract(task)
    if experiment.startswith("scalar-milestone"):
        assert "one write_milestone call" in contract
        milestone_tool = next(
            tool
            for tool in _build_active_tools("SPECSMITH_FULL", task)
            if tool["function"]["name"] == "write_milestone"
        )
        properties = milestone_tool["function"]["parameters"]["properties"]
        if experiment == "scalar-milestone-packet-authority-v4":
            assert "bounded files array" in contract
            assert set(properties) == {"files"}
        else:
            assert "fixed path_N/content_N scalar pairs" in contract
            assert not any(spec.get("type") == "array" for spec in properties.values())
        if experiment.startswith("scalar-milestone-packet"):
            assert milestone_tool["function"]["strict"] is True
            parameters = milestone_tool["function"]["parameters"]
            assert set(parameters["required"]) == set(properties)
            if experiment != "scalar-milestone-packet-authority-v4":
                assert {"type": "null"} in properties["path_2"]["anyOf"]
            native_tool = _openai_tools_to_responses([milestone_tool])[0]
            assert native_tool["strict"] is True
        if experiment == "scalar-milestone-packet-patch":
            assert "prefer one atomic patch_file call" in contract
    elif experiment.startswith("scalar-parallel") or experiment.startswith("scalar-native-patch"):
        assert "Issue independent write_file calls together" in contract
        assert "use write_files" not in contract
        if experiment == "scalar-parallel-edit":
            assert "prefer edit_file" in contract
        elif experiment.startswith("scalar-native-patch"):
            assert "prefer one atomic patch_file call" in contract
            patch_tool = next(
                tool
                for tool in _build_active_tools("SPECSMITH_FULL", task)
                if tool["function"]["name"] == "patch_file"
            )
            properties = patch_tool["function"]["parameters"]["properties"]
            assert not any(spec.get("type") == "array" for spec in properties.values())
            assert properties["old_text_1"]["minLength"] == 1
            assert patch_tool["function"]["strict"] is True
            parameters = patch_tool["function"]["parameters"]
            assert set(parameters["required"]) == set(properties)
            assert {"type": "null"} in properties["old_text_2"]["anyOf"]
            assert _openai_tools_to_responses([patch_tool])[0]["strict"] is True
    else:
        assert "use write_files" in contract


def test_unknown_controller_experiment_fails_loudly(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("BENCH_CONTROLLER_EXPERIMENT", "mystery")
    with pytest.raises(RuntimeError, match="Unsupported BENCH_CONTROLLER_EXPERIMENT"):
        _controller_experiment()


def test_benchmark_workflow_exposes_scoped_native_patch_experiment() -> None:
    workflow = (Path(__file__).parent.parent / ".github" / "workflows" / "bench.yml").read_text(
        encoding="utf-8"
    )
    assert "scalar-native-patch-scoped" in workflow
    assert "scalar-native-patch-scoped-required" in workflow
    assert "scalar-milestone-packet-authority-v3" in workflow
    assert "scalar-milestone-packet-authority-v4" in workflow
    native_workflow = (
        Path(__file__).parent.parent / ".github" / "workflows" / "qwen-native-bench.yml"
    ).read_text(encoding="utf-8")
    assert "milestone-packets" in native_workflow
    assert "milestone-authority-only" in native_workflow
    assert "milestone-authority-v2-only" in native_workflow
    assert "scalar-milestone-packet-adaptive" in native_workflow
    assert "scalar-milestone-packet-patch" in native_workflow
    assert "scalar-milestone-packet-authority" in native_workflow
    assert "scalar-milestone-packet-authority-v2" in native_workflow


def test_benchmark_deadlines_and_retry_policy_are_bounded(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("BENCH_REQUEST_TIMEOUT_S", raising=False)
    monkeypatch.delenv("BENCH_CELL_TIMEOUT_S", raising=False)
    monkeypatch.delenv("BENCH_PROVIDER_MAX_RETRIES", raising=False)
    assert _request_timeout_seconds() == 120
    assert _cell_timeout_seconds() == 900
    assert _provider_max_retries() == 0

    monkeypatch.setenv("BENCH_REQUEST_TIMEOUT_S", "45.5")
    monkeypatch.setenv("BENCH_CELL_TIMEOUT_S", "300")
    monkeypatch.setenv("BENCH_PROVIDER_MAX_RETRIES", "1")
    assert _request_timeout_seconds() == 45.5
    assert _cell_timeout_seconds() == 300
    assert _provider_max_retries() == 1

    monkeypatch.setenv("BENCH_REQUEST_TIMEOUT_S", "inf")
    with pytest.raises(RuntimeError, match="between 5 and 600"):
        _request_timeout_seconds()
    monkeypatch.setenv("BENCH_PROVIDER_MAX_RETRIES", "3")
    with pytest.raises(RuntimeError, match="between 0 and 2"):
        _provider_max_retries()


def test_native_endpoint_compute_is_not_double_counted_as_api_token_cost() -> None:
    assert (
        estimate_cost(
            "Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8",
            1_000_000,
            1_000_000,
        )
        == 0
    )


def test_compact_experiment_evicts_completed_boundary_bodies_and_write_history(
    tmp_path: Path,
) -> None:
    (tmp_path / "one.py").write_text("VALUE = 1\n", encoding="utf-8")
    (tmp_path / "two.py").write_text("VALUE = 2\n", encoding="utf-8")
    evidence: dict[str, tuple[str, int]] = {}
    packet = _boundary_context_packet(
        tmp_path,
        ["one.py", "two.py"],
        evidence,
        turn=0,
        replaceable=True,
    )
    messages = [
        {"role": "user", "content": f"Task contract\n\n{packet}"},
        {"role": "user", "content": "[Specsmith write receipts] stale turn receipt"},
    ]

    partial = _compact_completed_boundary_context(messages, ["one.py"])
    assert "VALUE = 1" in partial[0]["content"]
    completed = _compact_completed_boundary_context(partial, ["one.py", "two.py"])
    consolidated = _consolidate_write_receipts(
        completed,
        tmp_path,
        ["one.py", "two.py"],
    )

    serialized = str(consolidated)
    assert "VALUE = 1" not in serialized
    assert "VALUE = 2" not in serialized
    assert "completed boundary receipt" in serialized
    assert (
        sum(
            str(message.get("content") or "").startswith("[Specsmith write receipts]")
            for message in consolidated
        )
        == 1
    )
    assert "one.py" in serialized and "two.py" in serialized
    assert "stale turn receipt" not in serialized


def test_milestone_packet_compiles_only_the_active_public_boundary(tmp_path: Path) -> None:
    task = get_task("T28")
    packet = _milestone_work_packet(task, [])

    assert "Active work packet 1/4: shared contract and API" in packet
    assert "contracts/incident.schema.json" in packet
    assert "Schema declares exactly the seven incident fields" in packet
    assert "Controller-owned checks after the write" in packet
    assert "worker/main.go" not in packet
    assert "NormalizeAlert rejects" not in packet

    first_milestone = [str(path) for path in task.milestones[0]["files"]]
    assert _completed_milestone_count(task, first_milestone) == 1
    next_packet = _milestone_work_packet(task, first_milestone)
    assert "Active work packet 2/4: worker boundary" in next_packet
    assert "NormalizeAlert rejects" in next_packet
    assert "Schema declares exactly" not in next_packet

    for path in first_milestone:
        target = tmp_path / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f"starter {path}\n", encoding="utf-8")
    evidence: dict[str, tuple[str, int]] = {}
    context = _boundary_context_packet(
        tmp_path,
        first_milestone,
        evidence,
        turn=0,
        replaceable=True,
        work_packet=packet,
    )
    assert packet in context
    assert "starter backend/main.py" in context


def test_native_edit_interface_is_exact_bounded_and_tracks_changes(tmp_path: Path) -> None:
    path = tmp_path / "component.py"
    path.write_text("VALUE = 1\nKEEP = True\n", encoding="utf-8")
    written: list[str] = []

    assert _exec_edit_file(
        tmp_path,
        "component.py",
        "VALUE = 1",
        "VALUE = 2",
        written,
    ).startswith("OK:")
    assert path.read_text(encoding="utf-8") == "VALUE = 2\nKEEP = True\n"
    assert written == ["component.py"]
    assert _exec_edit_file(
        tmp_path,
        "missing.py",
        "VALUE = 1",
        "VALUE = 2",
        written,
    ).startswith("ERROR: file not found")
    assert (
        _exec_edit_file(
            tmp_path,
            "component.py",
            "",
            "VALUE = 3",
            written,
        )
        == "ERROR: old_text must be non-empty text"
    )

    path.write_text("VALUE = 2\nVALUE = 2\n", encoding="utf-8")
    ambiguous = _exec_edit_file(
        tmp_path,
        "component.py",
        "VALUE = 2",
        "VALUE = 3",
        written,
    )
    assert "ambiguous" in ambiguous
    assert path.read_text(encoding="utf-8") == "VALUE = 2\nVALUE = 2\n"

    hidden = tmp_path / ".specsmith" / "state.json"
    hidden.parent.mkdir()
    hidden.write_text('{"trusted": true}\n', encoding="utf-8")
    assert _exec_edit_file(
        tmp_path,
        ".specsmith/state.json",
        "true",
        "false",
        written,
    ).startswith("ERROR: controller governance state")
    assert hidden.read_text(encoding="utf-8") == '{"trusted": true}\n'


def test_native_patch_interface_is_atomic_bounded_and_tracks_changes(tmp_path: Path) -> None:
    path = tmp_path / "component.py"
    original = "from typing import Optional\n\nVALUE: str = 'one'\nKEEP = True\n"
    path.write_text(original, encoding="utf-8")
    written: list[str] = []
    args = {
        "path": "component.py",
        "old_text_1": "from typing import Optional",
        "new_text_1": "from typing import Literal, Optional",
        "old_text_2": "VALUE: str = 'one'",
        "new_text_2": "VALUE: Literal['one', 'two'] = 'one'",
    }

    assert _exec_patch_file(tmp_path, "component.py", args, written).startswith("OK:")
    assert path.read_text(encoding="utf-8") == (
        "from typing import Literal, Optional\n\n"
        "VALUE: Literal['one', 'two'] = 'one'\nKEEP = True\n"
    )
    assert written == ["component.py"]

    path.write_text(original, encoding="utf-8")
    invalid = {**args, "old_text_2": "MISSING"}
    assert _exec_patch_file(tmp_path, "component.py", invalid, written).startswith(
        "ERROR: old_text_2 not found"
    )
    assert path.read_text(encoding="utf-8") == original

    overlapping = {
        "path": "component.py",
        "old_text_1": "VALUE: str = 'one'",
        "new_text_1": "VALUE = 'two'",
        "old_text_2": "str = 'one'",
        "new_text_2": "str = 'two'",
    }
    assert "overlap" in _exec_patch_file(tmp_path, "component.py", overlapping, written)
    assert path.read_text(encoding="utf-8") == original


def test_scalar_milestone_bundle_validates_pairs_before_writing(tmp_path: Path) -> None:
    written: list[str] = []
    output, successful = _exec_write_milestone(
        tmp_path,
        {
            "path_1": "one.py",
            "content_1": "ONE = 1\n",
            "path_2": "two.py",
            "content_2": "TWO = 2\n",
            "path_3": None,
            "content_3": None,
            "path_4": None,
            "content_4": None,
        },
        written,
    )

    assert output.count("OK:") == 2
    assert successful == ["one.py", "two.py"]
    assert written == successful
    assert (tmp_path / "one.py").read_text(encoding="utf-8") == "ONE = 1\n"
    assert (tmp_path / "two.py").read_text(encoding="utf-8") == "TWO = 2\n"

    invalid, invalid_paths = _exec_write_milestone(
        tmp_path,
        {
            "path_1": "safe.py",
            "content_1": "SAFE = True\n",
            "path_2": "missing-content.py",
        },
        written,
    )
    assert invalid == "ERROR: content_2 must be text"
    assert invalid_paths == []
    assert not (tmp_path / "safe.py").exists()

    duplicate, duplicate_paths = _exec_write_milestone(
        tmp_path,
        {
            "path_1": "same.py",
            "content_1": "ONE = 1\n",
            "path_2": "./same.py",
            "content_2": "TWO = 2\n",
        },
        written,
    )
    assert duplicate.startswith("ERROR: duplicate milestone path")
    assert duplicate_paths == []
    assert not (tmp_path / "same.py").exists()

    out_of_scope, out_of_scope_paths = _exec_write_milestone(
        tmp_path,
        {
            "path_1": "allowed.py",
            "content_1": "ALLOWED = True\n",
            "path_2": "later.py",
            "content_2": "LATER = True\n",
        },
        written,
        allowed_paths=["allowed.py"],
    )
    assert "outside the active milestone boundary" in out_of_scope
    assert out_of_scope_paths == []
    assert not (tmp_path / "allowed.py").exists()
    assert not (tmp_path / "later.py").exists()


def test_accepted_aee_work_uses_one_compact_schema_and_bounded_scope() -> None:
    task = get_task("T1")
    active = _build_active_tools("SPECSMITH_FULL", task)
    initial = [tool["function"]["name"] for tool in active]
    diagnostic = [
        tool["function"]["name"]
        for tool in _build_active_tools("SPECSMITH_FULL", task, diagnostics_required=True)
    ]

    assert initial == ["read_files", "write_files", "read_file", "write_file", "done"]
    assert diagnostic == initial
    assert "run_command" not in _active_tool_names(active)
    repair_names = _active_tool_names(
        _build_focused_repair_tools(
            "SPECSMITH_FULL",
            task,
            composite_files=True,
            repair_written=True,
        )
    )
    assert repair_names == set(initial)
    assert not {"list_files", "run_command", "ask_clarification"} & set(diagnostic)
    assert "app/main.py" in _scope_contract(task)
    assert "assertions must not mutate shared state" in _scope_contract(task)
    assert task.initial_context_paths == ["app/main.py", "tests/test_main.py"]
    assert get_task("T10").initial_context_paths == [
        "app/main.py",
        "app/models.py",
        "tests/test_main.py",
        "pyproject.toml",
    ]
    assert get_task("T11").initial_context_paths[:3] == [
        "app/models.py",
        "app/main.py",
        "tests/test_main.py",
    ]
    assert get_task("T13").initial_context_paths == []
    assert "tests/test_main.py" in _scope_progress(task, ["app/main.py"])
    assert "call done" in _scope_progress(task, task.expected_files_changed)


def test_serialized_routes_receive_bounded_composite_file_tools(tmp_path: Path) -> None:
    task = get_task("T28")
    scalar_calls = [NormalizedToolCall(id="1", name="read_file", arguments="{}")]
    count = _updated_serialized_action_count(0, scalar_calls)
    count = _updated_serialized_action_count(
        count,
        [NormalizedToolCall(id="2", name="read_files", arguments="{}")],
    )
    count = _updated_serialized_action_count(count, scalar_calls)
    assert count == 2

    names = [
        tool["function"]["name"]
        for tool in _build_active_tools(
            "SPECSMITH_FULL",
            task,
            composite_files=True,
            composite_reads=True,
        )
    ]
    assert names == [
        "read_files",
        "write_files",
        "read_file",
        "write_file",
        "done",
    ]

    written: list[str] = []
    output, successful = _exec_write_files(
        tmp_path,
        [
            {"path": "one.py", "content": "ONE = 1\n"},
            {"path": "two.py", "content": "TWO = 2\n"},
        ],
        written,
    )
    assert successful == ["one.py", "two.py"]
    assert written == successful
    assert output.count("OK:") == 2

    content, suppressed = _exec_read_files_with_evidence(
        tmp_path,
        successful,
        {},
        turn=3,
        compress_unchanged=True,
    )
    assert "## one.py" in content and "## two.py" in content
    assert suppressed == []
    assert _read_paths_from_calls(
        [
            NormalizedToolCall(
                id="read-many",
                name="read_files",
                arguments='{"paths":["one.py","two.py"]}',
            )
        ]
    ) == ["one.py", "two.py"]
    repeated_reads = [
        NormalizedToolCall(
            id="read-one",
            name="read_file",
            arguments='{"path":"one.py"}',
        )
    ]
    assert _updated_unchanged_read_only_streak(0, repeated_reads, ["one.py"]) == 1
    assert _updated_unchanged_read_only_streak(1, repeated_reads, ["one.py"]) == 2
    assert _updated_unchanged_read_only_streak(2, repeated_reads, []) == 0
    assert (
        _updated_unchanged_read_only_streak(
            2,
            [NormalizedToolCall(id="write", name="write_file", arguments="{}")],
            [],
        )
        == 0
    )

    focus = _focused_validator_repair_progress(
        task,
        [
            "ruff check . FAILED:\nui/src/App.tsx:20:1 lint failure",
            "python tools/validate_contract.py FAILED:\nmissing field",
            "python tools/validate_ui.py FAILED:\nmissing role selector",
        ],
    )
    assert "ui/src/App.tsx" in focus
    assert "contracts/incident.schema.json" not in focus
    assert "queue and recheck" in focus
    assert "do not reread validator" in focus.casefold()


def test_pytest_repair_keeps_implementation_and_test_boundaries() -> None:
    task = get_task("T13")

    boundaries = _focused_validator_repair_boundaries(
        task,
        [
            "pytest FAILED:\n"
            "tests/test_process.py:69: Error: No such option '--filter'. "
            "Did you mean '--filters'?"
        ],
    )

    assert ("pytest", ["cli/commands/process.py", "tests/test_process.py"]) in boundaries


def test_validator_authority_prioritizes_independent_boundary(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("BENCH_CONTROLLER_EXPERIMENT", "scalar-parallel-validator-authority")
    task = get_task("T28")
    failures = [
        "pytest FAILED:\nself-authored test expects query parameters",
        "python tools/validate_api.py FAILED:\nPOST must accept the contract body",
    ]

    assert _focused_validator_repair_boundaries(task, failures) == [
        ("python tools/validate_api.py", ["backend/main.py"])
    ]
    assert _focused_validator_failures(task, failures) == [failures[1]]


def test_milestone_authority_repair_surface_is_atomic_and_path_focused(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("BENCH_CONTROLLER_EXPERIMENT", "scalar-milestone-packet-authority")
    task = get_task("T28")
    repair_tools = _build_focused_repair_tools(
        "SPECSMITH_FULL",
        task,
        composite_files=True,
        repair_written=True,
    )

    assert [tool["function"]["name"] for tool in repair_tools] == ["patch_file", "done"]
    assert all(tool["function"]["strict"] is True for tool in repair_tools)
    failures = [
        "pytest FAILED:\nself-authored tests expect HTTP 200",
        "python tools/validate_api.py FAILED:\nPOST must return HTTP 201",
    ]
    assert _focused_validator_failures(task, failures) == [failures[1]]

    monkeypatch.setenv("BENCH_CONTROLLER_EXPERIMENT", "scalar-milestone-packet-authority-v2")
    assert [
        tool["function"]["name"]
        for tool in _build_focused_repair_tools(
            "SPECSMITH_FULL",
            task,
            composite_files=True,
            repair_written=True,
        )
    ] == ["patch_file", "done"]

    monkeypatch.setenv("BENCH_CONTROLLER_EXPERIMENT", "scalar-milestone-packet-authority-v3")
    stable_tools = _build_focused_repair_tools(
        "SPECSMITH_FULL",
        task,
        composite_files=True,
        repair_written=True,
    )
    assert [tool["function"]["name"] for tool in stable_tools] == [
        "write_file",
        "write_milestone",
        "patch_file",
        "done",
    ]
    assert all(tool["function"]["strict"] is True for tool in stable_tools)
    assert _stable_repair_schema_experiment("scalar-milestone-packet-authority-v3")


def test_single_file_milestone_packet_uses_unambiguous_write_tool() -> None:
    task = get_task("T28")
    completed = [
        "contracts/incident.schema.json",
        "backend/main.py",
        "tests/test_backend.py",
        "worker/main.go",
        "worker/main_test.go",
        "ui/src/api.ts",
        "ui/src/App.tsx",
        "ui/src/styles.css",
        "ui/tests/incident-console.spec.ts",
    ]

    packet = _milestone_work_packet(task, completed)

    assert "Allowed write paths: docs/architecture.md" in packet
    assert "implement this one-file milestone now with write_file" in packet
    assert "one write_milestone call" not in packet


def test_native_milestone_schema_is_compact_strict_and_atomic(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("BENCH_CONTROLLER_EXPERIMENT", "scalar-milestone-packet-authority-v4")
    tools = _build_active_tools(
        "SPECSMITH_FULL",
        get_task("T28"),
        composite_files=True,
    )
    milestone = next(tool for tool in tools if tool["function"]["name"] == "write_milestone")

    assert milestone["function"]["strict"] is True
    assert set(milestone["function"]["parameters"]["properties"]) == {"files"}
    assert _openai_tools_to_responses([milestone])[0]["strict"] is True

    written: list[str] = []
    output, paths = _exec_write_milestone(
        tmp_path,
        {
            "files": [
                {"path": "a.py", "content": "A = 1\n"},
                {"path": "b.py", "content": "B = 2\n"},
            ]
        },
        written,
        allowed_paths=["a.py", "b.py"],
    )

    assert output == "OK: wrote 6 bytes to a.py\nOK: wrote 6 bytes to b.py"
    assert paths == ["a.py", "b.py"]
    assert written == ["a.py", "b.py"]

    rejected, rejected_paths = _exec_write_milestone(
        tmp_path,
        {"files": [{"path": "a.py", "content": "changed\n"}, {"path": "c.py"}]},
        written,
        allowed_paths=["a.py", "c.py"],
    )
    assert rejected == "ERROR: content_2 must be text"
    assert rejected_paths == []
    assert (tmp_path / "a.py").read_text(encoding="utf-8") == "A = 1\n"


def test_full_completion_applies_one_bounded_ruff_safe_fix(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[str] = []
    lint_results = iter([(False, "fixable lint"), (True, "clean")])

    def fake_command(_root: Path, command: str) -> tuple[bool, str]:
        calls.append(command)
        if command == "ruff check .":
            return next(lint_results)
        if command == "ruff check . --fix":
            return True, "Fixed 1 error."
        return True, "passed"

    monkeypatch.setattr(harness_module, "_exec_run_command", fake_command)
    receipts: list[str] = []
    lint_ok, tests_ok, _validators, failures = _run_missing_completion_validators(
        tmp_path,
        get_task("T2"),
        False,
        False,
        set(),
        repair_receipts=receipts,
    )

    assert lint_ok and tests_ok and failures == []
    assert calls == [
        "ruff check .",
        "ruff format .",
        "ruff check . --fix",
        "ruff check .",
        "pytest",
    ]
    assert receipts and "formatting/default-safe fixes" in receipts[0]


def test_open_model_sampling_uses_official_model_specific_defaults(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("BENCH_TEMPERATURE", raising=False)

    assert _openai_sampling_params("Qwen/Qwen3-Coder-Next:novita") == {
        "temperature": 1.0,
        "top_p": 0.95,
    }
    assert _openai_sampling_params("Qwen/Qwen3-Coder-480B-A35B-Instruct:novita") == {
        "temperature": 0.7,
        "top_p": 0.8,
    }
    assert _openai_sampling_params("Qwen/Qwen3.6-35B-A3B:deepinfra") == {
        "temperature": 0.6,
        "top_p": 0.95,
    }
    assert _openai_sampling_params("deepseek-ai/DeepSeek-V4-Flash:deepinfra") == {
        "temperature": 1.0,
        "top_p": 1.0,
    }
    assert _openai_sampling_params("nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16:deepinfra") == {
        "temperature": 1.0,
        "top_p": 0.95,
    }

    monkeypatch.setenv("BENCH_TEMPERATURE", "0.33")
    assert _openai_sampling_params("Qwen/Qwen3-Coder-Next:novita") == {"temperature": 0.33}


@pytest.mark.parametrize(
    ("content", "expected"),
    [
        ("Let me update the tests next.", True),
        ("Now I'll run the validator.", True),
        ("Now implementing Milestone 2: Go worker boundary.", True),
        ("Implementing Milestone 3 across all four files in one batch.", True),
        ("I'll implement Milestone 2: the Go worker boundary.", True),
        ("I will implement the next requirement boundary.", True),
        ("I'll write the UI boundary files for milestone 3.", True),
        ("I have enough evidence. Writing milestone 2 now.", True),
        ("All four milestones have implementation evidence. Calling done.", True),
        ("All four milestones are written. Calling `done` for validation.", True),
        ("The repair is ready to call done now.", True),
        ("The implementation and tests are complete.", False),
        ("The files were written and validated.", False),
    ],
)
def test_nonterminal_narration_detection_is_narrow(content: str, expected: bool) -> None:
    assert _looks_like_nonterminal_narration(content) is expected


def test_second_narration_recovery_requires_new_write_scope_progress() -> None:
    narration = "Now milestone 3. I'll write all four UI files."

    assert _can_recover_nonterminal_narration(
        narration,
        recovery_count=0,
        files_written=[],
        write_count_at_last_recovery=0,
    )
    assert _can_recover_nonterminal_narration(
        narration,
        recovery_count=1,
        files_written=["backend/main.py"],
        write_count_at_last_recovery=1,
        write_revision_count=2,
    )
    assert not _can_recover_nonterminal_narration(
        narration,
        recovery_count=1,
        files_written=[],
        write_count_at_last_recovery=0,
    )
    assert _can_recover_nonterminal_narration(
        narration,
        recovery_count=1,
        files_written=["backend/main.py"],
        write_count_at_last_recovery=0,
    )
    assert not _can_recover_nonterminal_narration(
        narration,
        recovery_count=2,
        files_written=["backend/main.py", "worker/main.go"],
        write_count_at_last_recovery=1,
    )


def test_repeated_repair_loop_never_advances_past_failed_authority() -> None:
    recovery = _repeated_write_recovery(
        "backend/main.py",
        1,
        ["worker/main.go"],
        active_repair=True,
    )

    assert "authoritative validator still fails" in recovery
    assert "Do not advance to another milestone" in recovery
    assert "worker/main.go" not in recovery


def test_serialized_done_recovery_requires_exact_schema_and_complete_scope() -> None:
    task = get_task("T28")
    complete_scope = list(task.expected_files_changed)
    payload = '{"explanation":"All requirement-linked work is complete.","refused":false}'

    recovered = _serialized_done_tool_call(payload, task, complete_scope, turn=17)

    assert recovered is not None
    assert recovered.id == "serialized-done-17"
    assert recovered.name == "done"
    assert _serialized_done_tool_call(payload, task, complete_scope[:-1], turn=17) is None
    assert (
        _serialized_done_tool_call(
            '{"explanation":"done","refused":false,"extra":true}',
            task,
            complete_scope,
            turn=17,
        )
        is None
    )
    assert (
        _serialized_done_tool_call(
            '{"explanation":"done","refused":true}',
            task,
            complete_scope,
            turn=17,
        )
        is None
    )


def test_text_serialized_active_function_is_recovered_through_normal_tools() -> None:
    content = '<function=write_files>{"files":[{"path":"one.py","content":"VALUE = 1\\n"}]}'

    recovered = _serialized_function_tool_call(
        content,
        {"read_files", "write_files", "done"},
        turn=5,
    )

    assert recovered is not None
    assert recovered.id == "serialized-function-5"
    assert recovered.name == "write_files"
    assert '"path":"one.py"' in recovered.arguments
    assert (
        _serialized_function_tool_call(
            '<function=run_command>{"command":"rm -rf ."}',
            {"write_files", "done"},
            turn=5,
        )
        is None
    )
    tagged = _serialized_function_tool_call(
        '<function=write_file>{"path":"one.py","content":"VALUE = 1\\n"}/function>',
        {"write_file"},
        turn=6,
    )
    assert tagged is not None
    assert tagged.name == "write_file"


def test_write_boundary_signature_covers_scalar_and_composite_calls() -> None:
    calls = [
        NormalizedToolCall(
            id="1",
            name="write_file",
            arguments='{"path":"two.py","content":"TWO = 2"}',
        ),
        NormalizedToolCall(
            id="2",
            name="write_files",
            arguments='{"files":[{"path":"one.py","content":"ONE = 1"}]}',
        ),
        NormalizedToolCall(
            id="3",
            name="edit_file",
            arguments='{"path":"three.py","old_text":"OLD","new_text":"NEW"}',
        ),
        NormalizedToolCall(
            id="4",
            name="write_milestone",
            arguments=(
                '{"path_1":"four.py","content_1":"FOUR = 4",'
                '"path_2":"five.py","content_2":"FIVE = 5"}'
            ),
        ),
    ]

    assert _write_paths_from_calls(calls) == [
        "five.py",
        "four.py",
        "one.py",
        "three.py",
        "two.py",
    ]
    assert _write_paths_from_calls([NormalizedToolCall(id="5", name="done", arguments="{}")]) == []
    assert (
        _serialized_function_tool_call(
            'Narration <function=write_files>{"files":[]}',
            {"write_files"},
            turn=5,
        )
        is None
    )


def _audit_row(*, condition: str, passed: bool, transcript: list[dict] | None = None) -> dict:
    return {
        "task": "T28",
        "category": "long_horizon_product",
        "horizon": "long",
        "condition": condition,
        "rep": 1,
        "model": "Qwen/Qwen3-Coder-Next:novita",
        "input_tokens": 20_000,
        "output_tokens": 1_000,
        "llm_turns": 20,
        "passed": passed,
        "tests_passed": passed,
        "project_tests_passed": True,
        "acceptance_oracle_passed": passed,
        "stop_reason": "done" if passed else "max_turns",
        "agent_transcript": transcript or [],
        "skipped": False,
        "error": None,
    }


def test_audit_exposes_task_type_reread_and_milestone_inefficiencies() -> None:
    read_cycle = [
        "read_file:backend/main.py",
        "read_file:worker/main.go",
        "read_file:ui/src/App.tsx",
        "read_file:docs/architecture.md",
    ]
    transcript = [
        {
            "role": "assistant",
            "tool_targets": [
                *read_cycle,
                *read_cycle,
                *read_cycle,
                "write_file:backend/main.py",
                "write_file:tests/test_backend.py",
                "write_file:worker/main.go",
                "write_file:worker/main_test.go",
                "write_file:ui/src/App.tsx",
                "write_file:docs/architecture.md",
            ],
        }
    ]
    report = audit_benchmark_rows(
        [
            _audit_row(condition="CURSOR_RULES", passed=True),
            _audit_row(condition="SPECSMITH_FULL", passed=False, transcript=transcript),
        ]
    )
    codes = {weakness.code for weakness in report.weaknesses}

    assert "broad_reread_churn" in codes
    assert "milestone_fragmentation" in codes
    assert "cursor_correctness_regression" in codes
    assert report.task_type_metrics["long_horizon_product"]["CURSOR_RULES"]["pass_rate"] == 1.0


def test_audit_exposes_tool_serialization_text_stops_and_scope_expansion() -> None:
    serialized = _audit_row(condition="SPECSMITH_FULL", passed=False)
    serialized.update(
        {
            "stop_reason": "text_response",
            "expected_files_changed": ["backend/main.py"],
            "files_written": ["backend/main.py", "notes/debug.txt"],
            "agent_transcript": [
                {
                    "role": "assistant",
                    "tool_calls": ["read_file"],
                    "tool_targets": [f"read_file:file-{index}.txt"],
                }
                for index in range(6)
            ],
        }
    )

    report = audit_benchmark_rows([serialized])
    codes = {weakness.code for weakness in report.weaknesses}

    assert {"premature_text_stop", "tool_call_serialization", "scope_expansion"} <= codes


def test_audit_identifies_provider_tool_continuation_failure() -> None:
    failed = _audit_row(condition="SPECSMITH_FULL", passed=False)
    failed.update(
        {
            "stop_reason": "empty_response",
            "agent_transcript": [
                {
                    "role": "assistant",
                    "tool_calls": ["read_file"],
                    "tool_targets": ["read_file:contracts/incident.schema.json"],
                    "content": "",
                },
                {"role": "assistant", "tool_calls": [], "tool_targets": [], "content": ""},
                {"role": "assistant", "tool_calls": [], "tool_targets": [], "content": ""},
            ],
        }
    )

    report = audit_benchmark_rows([failed])
    weaknesses = {item.code: item for item in report.weaknesses}

    assert "tool_continuation_failure" in weaknesses
    assert "model-native tool protocol" in weaknesses["tool_continuation_failure"].recommendation
    assert report.next_experiment.action == "repair_and_rerun"
    assert "tool_continuation_failure" in report.next_experiment.evidence_codes


def test_audit_identifies_suppressed_read_loop() -> None:
    failed = _audit_row(condition="SPECSMITH_FULL", passed=False)
    failed.update(
        {
            "stop_reason": "repeated_tool_loop",
            "agent_transcript": [
                {
                    "turn": 3,
                    "role": "controller",
                    "suppressed_read_loop": ["worker/main.go"],
                    "count": 3,
                }
            ],
        }
    )

    report = audit_benchmark_rows([failed])
    weaknesses = {item.code: item for item in report.weaknesses}

    assert "suppressed_read_loop" in weaknesses
    assert "evidence already present" in weaknesses["suppressed_read_loop"].recommendation
    assert report.next_experiment.action == "repair_and_rerun"


def test_audit_identifies_finish_reason_and_composite_payload_failures() -> None:
    row = _audit_row(condition="SPECSMITH_FULL", passed=True)
    row.update(
        {
            "call_usage": [{"turn": 1, "finish_reason": "length"}],
            "agent_transcript": [
                {
                    "turn": 1,
                    "role": "controller",
                    "composite_write_payload_failure": 1,
                }
            ],
        }
    )

    report = audit_benchmark_rows([row])
    weaknesses = {item.code: item for item in report.weaknesses}

    assert {"completion_truncation", "composite_write_payload_failure"} <= set(weaknesses)
    assert "do not infer truncation" in weaknesses["completion_truncation"].recommendation


def test_qwen_agentic_coding_candidates_have_hf_routes_pricing_and_tiers() -> None:
    registry = load_registry(_SCRIPTS_DIR / "govern_bench" / "models.yml")
    candidates = select(registry, groups={"open-qwen"})

    assert {candidate["label"] for candidate in candidates} == {
        "qwen3-coder-next",
        "qwen3-coder-480b",
        "qwen3.6-35b-deepinfra",
    }
    assert all(candidate["provider"] == "huggingface" for candidate in candidates)
    assert estimate_cost("Qwen/Qwen3-Coder-Next:novita", 1_000_000, 1_000_000) == pytest.approx(
        1.70
    )
    assert model_tier("Qwen/Qwen3-Coder-Next:novita") == "open-large"
    assert model_tier("Qwen/Qwen3-Coder-480B-A35B-Instruct:novita") == "open-xl"
    assert estimate_cost("Qwen/Qwen3.6-35B-A3B:deepinfra", 1_000_000, 1_000_000) == pytest.approx(
        1.10
    )


def test_open_frontier_candidates_have_verified_routes_pricing_and_tiers() -> None:
    registry = load_registry(_SCRIPTS_DIR / "govern_bench" / "models.yml")
    candidates = select(registry, groups={"open-frontier"})

    assert {candidate["label"] for candidate in candidates} == {
        "kimi-k2.7-code",
        "glm-5.2",
        "deepseek-v4-pro",
        "deepseek-v4-flash",
        "nemotron-3-ultra",
        "minimax-m3",
    }
    assert all(candidate["provider"] == "huggingface" for candidate in candidates)
    expected_costs = {
        "moonshotai/Kimi-K2.7-Code:deepinfra": 4.24,
        "moonshotai/Kimi-K2.7-Code:together": 4.95,
        "moonshotai/Kimi-K2.7-Code:novita": 4.95,
        "zai-org/GLM-5.2:deepinfra": 3.93,
        "deepseek-ai/DeepSeek-V4-Pro:novita": 4.80,
        "deepseek-ai/DeepSeek-V4-Flash:deepinfra": 0.27,
        "nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16:deepinfra": 6.00,
        "MiniMaxAI/MiniMax-M3:novita": 1.50,
    }
    for candidate in candidates:
        model = candidate["model"]
        assert estimate_cost(model, 1_000_000, 1_000_000) == pytest.approx(expected_costs[model])
        assert model_tier(model) == "open-xl"


def test_openai_native_registry_keeps_family_routes_evidence_separated() -> None:
    registry = load_registry(_SCRIPTS_DIR / "govern_bench" / "models.yml")
    candidates = select(registry, groups={"openai-native"})

    assert candidates == [
        {
            "label": "gpt-5.6-sol-responses",
            "provider": "openai-responses",
            "model": "gpt-5.6-sol",
            "group": "openai-native",
            "tier": "frontier",
        },
        {
            "label": "gpt-5.6-terra-responses",
            "provider": "openai-responses",
            "model": "gpt-5.6-terra",
            "group": "openai-native",
            "tier": "mid",
        },
        {
            "label": "gpt-5.6-luna-responses",
            "provider": "openai-responses",
            "model": "gpt-5.6-luna",
            "group": "openai-native",
            "tier": "mini",
        },
    ]


def test_gpt_oss_admission_uses_pinned_tool_route_and_exact_pricing() -> None:
    registry = load_registry(_SCRIPTS_DIR / "govern_bench" / "models.yml")
    candidates = select(registry, groups={"open"}, model_ids={"gpt-oss-120b"})

    assert candidates == [
        {
            "label": "gpt-oss-120b",
            "provider": "huggingface",
            "model": "openai/gpt-oss-120b:novita",
            "group": "open",
            "tier": "open-xl",
        }
    ]
    assert estimate_cost("openai/gpt-oss-120b:novita", 1_000_000, 1_000_000) == pytest.approx(0.30)
    assert model_tier("openai/gpt-oss-120b:novita") == "open-xl"
