# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Layer1Labs Silicon, Inc. All rights reserved.
"""Small deterministic primitives for token-efficient governed agents.

The controller deliberately owns bookkeeping that language models perform
poorly: lane selection, bounded working memory, lossless evidence references,
stall detection, and milestone handoff.  It does not decide whether code is
correct; executable validators retain that authority.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


class ControllerLane(str, Enum):
    """The smallest deterministic workflow suitable for a task."""

    GATE = "gate"
    COMPILED_PATCH = "compiled_patch"
    MILESTONE = "milestone"


def select_controller_lane(
    *,
    is_safety_task: bool = False,
    is_clarification_task: bool = False,
    is_long_horizon: bool = False,
    expected_files: Sequence[str] = (),
    milestones: Sequence[Mapping[str, object]] = (),
    languages: Sequence[str] = (),
) -> ControllerLane:
    """Choose a deterministic controller lane without spending model tokens.

    Bounded maintenance stays on a localization/patch/validation lane.  Work
    with explicit long-horizon metadata, several milestones, multiple
    languages, or a wide write scope retains milestone governance.
    """

    if is_safety_task or is_clarification_task:
        return ControllerLane.GATE
    if (
        is_long_horizon
        or len(milestones) > 1
        or len({lang.casefold() for lang in languages if lang}) > 1
        or len({path for path in expected_files if path}) > 4
    ):
        return ControllerLane.MILESTONE
    return ControllerLane.COMPILED_PATCH


@dataclass(frozen=True)
class EvidenceRecord:
    """Full-fidelity evidence stored outside the active model context."""

    ref: str
    kind: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)


class EvidenceVault:
    """Content-addressed evidence with optional JSONL persistence.

    The working context contains only stable references and short previews;
    exact observations remain available through :meth:`get`.
    """

    def __init__(self, root: Path | None = None) -> None:
        self.root = root.resolve() if root is not None else None
        self._records: dict[str, EvidenceRecord] = {}
        self._path = self.root / ".specsmith" / "controller-evidence.jsonl" if self.root else None

    def put(
        self,
        content: object,
        *,
        kind: str,
        metadata: Mapping[str, Any] | None = None,
    ) -> str:
        """Store exact evidence idempotently and return its stable reference."""

        exact = content if isinstance(content, str) else json.dumps(content, sort_keys=True)
        digest = hashlib.sha256(f"{kind}\0{exact}".encode()).hexdigest()[:16]
        ref = f"EV-{digest.upper()}"
        if ref in self._records:
            return ref
        record = EvidenceRecord(ref, kind, exact, dict(metadata or {}))
        self._records[ref] = record
        if self._path is not None:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            with self._path.open("a", encoding="utf-8", newline="\n") as stream:
                stream.write(json.dumps(asdict(record), sort_keys=True) + "\n")
        return ref

    def get(self, ref: str) -> EvidenceRecord | None:
        """Return exact evidence, loading the persisted vault on demand."""

        record = self._records.get(ref)
        if record is not None or self._path is None or not self._path.exists():
            return record
        for line in self._path.read_text(encoding="utf-8").splitlines():
            try:
                payload = json.loads(line)
                loaded = EvidenceRecord(
                    ref=str(payload["ref"]),
                    kind=str(payload["kind"]),
                    content=str(payload["content"]),
                    metadata=dict(payload.get("metadata") or {}),
                )
            except (KeyError, TypeError, ValueError, json.JSONDecodeError):
                continue
            self._records[loaded.ref] = loaded
        return self._records.get(ref)

    @property
    def refs(self) -> list[str]:
        """Return deterministic evidence references currently known."""

        return sorted(self._records)


@dataclass(frozen=True)
class WorkingContextStats:
    before_chars: int
    after_chars: int
    pruned_chars: int
    archived_refs: tuple[str, ...]
    retained_tool_pairs: int


def should_compact_working_context(
    *, completed_milestones: int, last_compacted_milestones: int
) -> bool:
    """Compact only after crossing a validated milestone boundary.

    Active-milestone tool exchanges are working state, not archival evidence.
    Keeping them intact prevents a rolling context window from hiding the
    exact API contract or failure chain that the current repair still needs.
    """

    return completed_milestones > last_compacted_milestones


def _message_chars(message: Mapping[str, Any]) -> int:
    return len(json.dumps(message, sort_keys=True, default=str))


def _tool_exchange_groups(messages: Sequence[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    """Group an assistant tool request with its contiguous tool responses."""

    groups: list[list[dict[str, Any]]] = []
    index = 0
    while index < len(messages):
        message = messages[index]
        group = [message]
        if message.get("role") == "assistant" and message.get("tool_calls"):
            index += 1
            while index < len(messages) and messages[index].get("role") == "tool":
                group.append(messages[index])
                index += 1
            groups.append(group)
            continue
        groups.append(group)
        index += 1
    return groups


def bound_working_messages(
    messages: Sequence[dict[str, Any]],
    *,
    vault: EvidenceVault,
    controller_state: Mapping[str, Any],
    recent_tool_pairs: int = 5,
    max_chars: int = 48_000,
) -> tuple[list[dict[str, Any]], WorkingContextStats]:
    """Keep the task contract and recent tool pairs; archive older evidence.

    The operation is deterministic and never discards exact evidence.  It is
    safe to call after every tool turn; already-bounded histories are returned
    without generating duplicate vault records.
    """

    copied = [dict(message) for message in messages]
    before = sum(_message_chars(message) for message in copied)
    if len(copied) <= 2 and before <= max_chars:
        return copied, WorkingContextStats(before, before, 0, (), 0)

    first_user = next(
        (index for index, message in enumerate(copied) if message.get("role") == "user"),
        len(copied) - 1,
    )
    header = copied[: first_user + 1]
    groups = _tool_exchange_groups(copied[first_user + 1 :])
    tool_group_indexes = [
        index
        for index, group in enumerate(groups)
        if group and group[0].get("role") == "assistant" and group[0].get("tool_calls")
    ]
    keep_tool_indexes = set(tool_group_indexes[-max(0, recent_tool_pairs) :])
    # Preserve recent controller/user guidance even if it is not a tool pair.
    non_tool_indexes = [index for index in range(len(groups)) if index not in tool_group_indexes]
    keep_indexes = keep_tool_indexes | set(non_tool_indexes[-2:])

    archived: list[str] = []
    kept_groups: list[list[dict[str, Any]]] = []
    for index, group in enumerate(groups):
        if index in keep_indexes:
            kept_groups.append(group)
            continue
        ref = vault.put(group, kind="tool_exchange", metadata={"group": index})
        archived.append(ref)

    state_payload = dict(controller_state)
    if archived:
        state_payload["archived_evidence"] = archived
    state_message = {
        "role": "user",
        "content": (
            "[SPECSMITH WORKING STATE]\n"
            + json.dumps(state_payload, sort_keys=True, separators=(",", ":"))
            + "\nUse read_evidence only when exact archived content is necessary."
        ),
    }
    bounded = [*header, state_message]
    for group in kept_groups:
        bounded.extend(group)

    # If the recent window still exceeds the cap, drop oldest retained tool
    # pairs one at a time, always preserving the contract and newest pair.
    while sum(_message_chars(message) for message in bounded) > max_chars:
        candidate = next(
            (
                index
                for index, message in enumerate(bounded)
                if index > len(header)
                and message.get("role") == "assistant"
                and message.get("tool_calls")
            ),
            None,
        )
        if candidate is None:
            break
        end = candidate + 1
        while end < len(bounded) and bounded[end].get("role") == "tool":
            end += 1
        if not any(
            message.get("role") == "assistant" and message.get("tool_calls")
            for message in bounded[end:]
        ):
            break
        group = bounded[candidate:end]
        archived.append(vault.put(group, kind="tool_exchange", metadata={"cap_pruned": True}))
        del bounded[candidate:end]
        state_payload["archived_evidence"] = archived
        bounded[len(header)]["content"] = (
            "[SPECSMITH WORKING STATE]\n"
            + json.dumps(state_payload, sort_keys=True, separators=(",", ":"))
            + "\nUse read_evidence only when exact archived content is necessary."
        )

    after = sum(_message_chars(message) for message in bounded)
    retained = sum(
        1 for message in bounded if message.get("role") == "assistant" and message.get("tool_calls")
    )
    return bounded, WorkingContextStats(
        before_chars=before,
        after_chars=after,
        pruned_chars=max(0, before - after),
        archived_refs=tuple(dict.fromkeys(archived)),
        retained_tool_pairs=retained,
    )


@dataclass(frozen=True)
class ProgressDecision:
    action: str
    reason: str
    no_progress_turns: int
    repeated_failure_count: int


class ProgressGuard:
    """Convert execution progress into bounded recover/replay/escalate actions."""

    def __init__(self, *, replay_limit: int = 1, escalation_turns: int = 3) -> None:
        self.replay_limit = max(0, replay_limit)
        self.escalation_turns = max(2, escalation_turns)
        self.last_milestones = 0
        self.last_file_count = 0
        self.last_failure_signature = ""
        self.no_progress_turns = 0
        self.repeated_failure_count = 0
        self.replays = 0
        self.narration_stops = 0

    def observe(
        self,
        *,
        milestones_completed: int,
        file_count: int,
        failure_signature: str = "",
        had_tool_action: bool = True,
    ) -> ProgressDecision:
        progressed = (
            milestones_completed > self.last_milestones or file_count > self.last_file_count
        )
        if progressed:
            self.no_progress_turns = 0
        else:
            self.no_progress_turns += 1

        if failure_signature and failure_signature == self.last_failure_signature:
            self.repeated_failure_count += 1
        elif failure_signature:
            self.repeated_failure_count = 1
        else:
            self.repeated_failure_count = 0

        if not had_tool_action:
            self.narration_stops += 1
        else:
            self.narration_stops = 0

        self.last_milestones = max(self.last_milestones, milestones_completed)
        self.last_file_count = max(self.last_file_count, file_count)
        self.last_failure_signature = failure_signature

        if self.narration_stops >= 2:
            return self._decision("escalate", "repeated narration without a tool action")
        if self.repeated_failure_count >= 2 and self.replays < self.replay_limit:
            self.replays += 1
            return self._decision("replay", "validator failure repeated at the same milestone")
        if self.repeated_failure_count >= 3:
            return self._decision("escalate", "validator failure persisted after bounded replay")
        if self.no_progress_turns >= self.escalation_turns:
            return self._decision("escalate", "no validated milestone progress within the bound")
        if self.no_progress_turns == self.escalation_turns - 1:
            return self._decision("recover", "one bounded recovery remains before escalation")
        return self._decision("continue", "progress remains within the controller bound")

    def _decision(self, action: str, reason: str) -> ProgressDecision:
        return ProgressDecision(
            action=action,
            reason=reason,
            no_progress_turns=self.no_progress_turns,
            repeated_failure_count=self.repeated_failure_count,
        )

    def acknowledge_nonterminal_escalation(self) -> None:
        """Start a fresh bounded recovery window after an unaccepted handoff.

        An escalation signal is terminal only when a configured stronger route
        can receive it.  Otherwise the current route keeps its partial progress
        and receives another bounded window instead of failing immediately.
        """

        self.no_progress_turns = 0
        self.repeated_failure_count = 0
        self.narration_stops = 0
        self.last_failure_signature = ""


@dataclass(frozen=True)
class MilestoneHandoff:
    """Minimal sufficient state for a stronger model to resume one milestone."""

    task_id: str
    controller_lane: str
    reason: str
    active_milestone: str
    files_written: tuple[str, ...]
    validator_failures: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    input_tokens: int
    output_tokens: int
    final_diff: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def trace_policy_examples(transcript: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Compile deterministic controller decisions into small-policy examples."""

    examples: list[dict[str, Any]] = []
    for event in transcript:
        if event.get("role") != "controller":
            continue
        decision = event.get("progress_decision")
        if not isinstance(decision, Mapping):
            continue
        examples.append(
            {
                "features": {
                    "turn": int(event.get("turn") or 0),
                    "milestones_completed": int(event.get("milestones_completed") or 0),
                    "files_written": int(event.get("files_written") or 0),
                    "failure_signature": str(event.get("failure_signature") or ""),
                },
                "label": str(decision.get("action") or "continue"),
                "reason": str(decision.get("reason") or ""),
            }
        )
    return examples
