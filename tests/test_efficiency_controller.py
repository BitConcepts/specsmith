from __future__ import annotations

from pathlib import Path

from specsmith.efficiency_controller import (
    ControllerLane,
    EvidenceVault,
    ProgressGuard,
    bound_working_messages,
    select_controller_lane,
    trace_policy_examples,
)
from specsmith.retrieval import build_role_entries, rank_role_entries, render_role_packet


def test_lane_selection_uses_smallest_deterministic_workflow() -> None:
    assert select_controller_lane(is_safety_task=True) is ControllerLane.GATE
    assert (
        select_controller_lane(expected_files=["src/service.py", "tests/test_service.py"])
        is ControllerLane.COMPILED_PATCH
    )
    assert select_controller_lane(languages=["python", "typescript"]) is ControllerLane.MILESTONE
    assert (
        select_controller_lane(milestones=[{"name": "api"}, {"name": "ui"}])
        is ControllerLane.MILESTONE
    )


def test_evidence_vault_is_content_addressed_and_lossless(tmp_path: Path) -> None:
    vault = EvidenceVault(tmp_path)
    ref = vault.put("full validator output", kind="validator", metadata={"turn": 3})
    assert vault.put("full validator output", kind="validator") == ref
    assert vault.get(ref) is not None
    assert vault.get(ref).content == "full validator output"  # type: ignore[union-attr]

    reloaded = EvidenceVault(tmp_path)
    assert reloaded.get(ref) is not None
    assert reloaded.get(ref).metadata == {"turn": 3}  # type: ignore[union-attr]


def test_working_context_keeps_five_tool_pairs_and_archives_exact_history() -> None:
    messages: list[dict] = [
        {"role": "system", "content": "contract"},
        {"role": "user", "content": "task"},
    ]
    for index in range(7):
        messages.extend(
            [
                {
                    "role": "assistant",
                    "content": "",
                    "tool_calls": [
                        {
                            "id": f"call-{index}",
                            "type": "function",
                            "function": {"name": "read_file", "arguments": "{}"},
                        }
                    ],
                },
                {
                    "role": "tool",
                    "tool_call_id": f"call-{index}",
                    "content": f"exact result {index}",
                },
            ]
        )

    bounded, stats = bound_working_messages(
        messages,
        vault=EvidenceVault(),
        controller_state={"milestone": "api", "tests": "pending"},
        recent_tool_pairs=5,
        max_chars=100_000,
    )

    retained = [message for message in bounded if message.get("tool_calls")]
    assert len(retained) == 5
    assert len(stats.archived_refs) == 2
    assert stats.pruned_chars > 0
    assert "SPECSMITH WORKING STATE" in bounded[2]["content"]


def test_progress_guard_replays_once_then_escalates_repeated_failure() -> None:
    guard = ProgressGuard(replay_limit=1, escalation_turns=4)
    first = guard.observe(
        milestones_completed=1,
        file_count=2,
        failure_signature="validator:css",
    )
    second = guard.observe(
        milestones_completed=1,
        file_count=2,
        failure_signature="validator:css",
    )
    third = guard.observe(
        milestones_completed=1,
        file_count=2,
        failure_signature="validator:css",
    )
    assert first.action == "continue"
    assert second.action == "replay"
    assert third.action == "escalate"


def test_trace_policy_examples_use_controller_decisions_only() -> None:
    transcript = [
        {"turn": 1, "role": "assistant", "content": "ignored"},
        {
            "turn": 2,
            "role": "controller",
            "milestones_completed": 1,
            "files_written": 3,
            "failure_signature": "abc",
            "progress_decision": {"action": "replay", "reason": "same failure"},
        },
    ]
    assert trace_policy_examples(transcript) == [
        {
            "features": {
                "turn": 2,
                "milestones_completed": 1,
                "files_written": 3,
                "failure_signature": "abc",
            },
            "label": "replay",
            "reason": "same failure",
        }
    ]


def test_role_retrieval_prefers_task_and_failure_relevant_files(tmp_path: Path) -> None:
    (tmp_path / "api").mkdir()
    (tmp_path / "web").mkdir()
    (tmp_path / "tests").mkdir()
    (tmp_path / "api" / "release.py").write_text(
        "def release_status():\n    return {'status': 'ready'}\n",
        encoding="utf-8",
    )
    (tmp_path / "web" / "ReleaseButton.tsx").write_text(
        "export function ReleaseButton() { return <button>Release</button>; }\n",
        encoding="utf-8",
    )
    (tmp_path / "tests" / "test_release.py").write_text(
        "def test_release_status():\n    assert True\n",
        encoding="utf-8",
    )

    entries = build_role_entries(tmp_path)
    ranked = rank_role_entries(
        entries,
        "release status UI",
        failure_context="ReleaseButton rendering failed",
        limit=2,
    )

    assert ranked[0]["path"] == "web/ReleaseButton.tsx"
    assert "interactive user interface" in render_role_packet(ranked)
    assert "return <button>" not in render_role_packet(ranked)
