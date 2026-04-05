# SPDX-License-Identifier: MIT
# Copyright (c) 2026 BitConcepts, LLC. All rights reserved.
"""Belief Artifact model — core AEE primitive.

A BeliefArtifact is a codable, testable, deployable unit of knowledge.
In specsmith, requirements, architectural decisions, and constraints are all
modelled as BeliefArtifacts — claims about what the system does, should do,
or must not do, each with an explicit epistemic boundary (the assumptions and
context within which the claim must hold) and a confidence level.

Theoretical basis
-----------------
Applied Epistemic Engineering (AEE) treats belief systems like code:
codable, testable, and deployable. The five foundational axioms are:

  1. Observability   — Every belief must be inspectable. Hidden assumptions
                       are a stop condition (Hard Rule H13).
  2. Falsifiability  — Every belief must be challengeable. A claim that cannot
                       be challenged is not an engineering artifact; it is dogma.
  3. Irreducibility  — Beliefs must be decomposed to their primitive propositions.
                       Compound beliefs that cannot be reduced often hide Logic Knots.
  4. Reconstructability — After stress-testing, every failed belief must yield a
                         reconstructed belief that satisfies Observability and
                         Falsifiability. Recovery is always possible; it may require
                         modifying the scope, not just the claim.
  5. Convergence     — Systematic application of the Stress-Test (S) and Recovery (R)
                       operators always converges to an Equilibrium Point E where
                       S(G) yields no new failure modes.

References
----------
- Applied Epistemic Engineering: https://appliedepistemicengineering.com/
- ARE framework: https://github.com/organvm-i-theoria/auto-revision-epistemic-engine
- VERITAS/CERTUS: https://github.com/AionSystem/VERITAS
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class ConfidenceLevel(str, Enum):
    """Epistemic confidence assigned to a BeliefArtifact.

    Maps to a numeric score used by CertaintyEngine:
      UNKNOWN  → 0.0   (no evidence, new claim)
      LOW      → 0.25  (asserted but not stress-tested)
      MEDIUM   → 0.55  (stress-tested with minor failures resolved)
      HIGH     → 0.85  (stress-tested, equilibrium reached, evidence present)
    """

    UNKNOWN = "unknown"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

    @property
    def score(self) -> float:
        """Numeric score for propagation calculations."""
        return _CONFIDENCE_SCORES[self]


_CONFIDENCE_SCORES: dict[ConfidenceLevel, float] = {
    ConfidenceLevel.UNKNOWN: 0.0,
    ConfidenceLevel.LOW: 0.25,
    ConfidenceLevel.MEDIUM: 0.55,
    ConfidenceLevel.HIGH: 0.85,
}


class BeliefStatus(str, Enum):
    """Lifecycle status of a BeliefArtifact."""

    DRAFT = "draft"  # Proposed, not yet accepted
    ACCEPTED = "accepted"  # Accepted by human operator
    STRESS_TESTED = "stress-tested"  # Has been through stress-testing
    RECONSTRUCTED = "reconstructed"  # Rebuilt after stress-test failures
    DEPRECATED = "deprecated"  # Superseded; kept for audit trail


class FailureSeverity(str, Enum):
    """Severity of a failure mode in the Failure-Mode Graph."""

    CRITICAL = "critical"  # Blocks progress; must be resolved before proceeding
    HIGH = "high"  # Significant weakness; should be resolved
    MEDIUM = "medium"  # Noteworthy; monitor and address
    LOW = "low"  # Minor; informational


@dataclass
class FailureMode:
    """A single failure mode discovered by the StressTester.

    A failure mode represents a stress-test→breakpoint relation in the
    Failure-Mode Graph G. Every FailureMode has an adversarial challenge
    that exposed it and a description of the breakpoint.
    """

    artifact_id: str
    challenge: str  # The adversarial challenge that exposed this failure
    breakpoint: str  # What breaks when the challenge is applied
    severity: FailureSeverity = FailureSeverity.MEDIUM
    recovery_hint: str = ""  # Suggested recovery path (RecoveryOperator expands this)
    resolved: bool = False


@dataclass
class BeliefArtifact:
    """A codable, testable, deployable unit of knowledge.

    BeliefArtifacts are the fundamental unit of the AEE framework. In
    specsmith, every requirement, architectural decision, and constraint
    is representable as a BeliefArtifact.

    Fields
    ------
    artifact_id : str
        Unique identifier (e.g. "REQ-CLI-001", "DEC-001", "ARCH-BE-001").
    propositions : list[str]
        Atomic, independently testable claims that compose this belief.
        Each proposition must satisfy Observability (inspectable) and
        Falsifiability (challengeable). Compound claims should be split.
    epistemic_boundary : list[str]
        The assumptions and context within which all propositions must hold.
        This is the Δ in AEE notation. Explicit boundaries prevent hidden
        assumptions (which violate H13 — Epistemic Boundaries Required).
    inferential_links : list[str]
        IDs of BeliefArtifacts this artifact logically depends on or derives
        from. Used by FailureModeGraph to detect Logic Knots and by
        CertaintyEngine to propagate confidence.
    confidence : ConfidenceLevel
        Current epistemic confidence (UNKNOWN → LOW → MEDIUM → HIGH).
    status : BeliefStatus
        Lifecycle status.
    failure_modes : list[FailureMode]
        Failure modes discovered during stress-testing. Empty until
        StressTester has been applied.
    source_text : str
        The original requirement or decision text this was parsed from.
    component : str
        The component code (e.g. "CLI", "AEE", "TRC") from the REQ ID.
    priority : str
        Priority from the source document (P1, P2, P3, or empty).
    """

    artifact_id: str
    propositions: list[str] = field(default_factory=list)
    epistemic_boundary: list[str] = field(default_factory=list)
    inferential_links: list[str] = field(default_factory=list)
    confidence: ConfidenceLevel = ConfidenceLevel.UNKNOWN
    status: BeliefStatus = BeliefStatus.DRAFT
    failure_modes: list[FailureMode] = field(default_factory=list)
    source_text: str = ""
    component: str = ""
    priority: str = ""

    @property
    def is_accepted(self) -> bool:
        return self.status in (
            BeliefStatus.ACCEPTED,
            BeliefStatus.STRESS_TESTED,
            BeliefStatus.RECONSTRUCTED,
        )

    @property
    def has_failures(self) -> bool:
        return any(not fm.resolved for fm in self.failure_modes)

    @property
    def unresolved_failures(self) -> list[FailureMode]:
        return [fm for fm in self.failure_modes if not fm.resolved]

    @property
    def critical_failures(self) -> list[FailureMode]:
        return [
            fm
            for fm in self.failure_modes
            if not fm.resolved and fm.severity == FailureSeverity.CRITICAL
        ]


# ---------------------------------------------------------------------------
# Markdown parser — converts REQUIREMENTS.md entries to BeliefArtifacts
# ---------------------------------------------------------------------------

_REQ_HEADING = re.compile(r"^#{1,3}\s+(REQ-([A-Z0-9_]+)-(\d+))\s*(?:—\s*(.+))?$")
_FIELD_LINE = re.compile(r"^\s*-\s+\*\*(.+?)\*\*:\s*(.+)$")


def parse_requirements_as_beliefs(path: Path) -> list[BeliefArtifact]:
    """Parse a REQUIREMENTS.md file and return a list of BeliefArtifacts.

    Each requirement becomes a BeliefArtifact with:
    - artifact_id  ← the REQ-XXX-NNN identifier
    - propositions ← the description text (split at semicolons if compound)
    - component    ← the component code extracted from the ID
    - priority     ← from **Priority:** field if present
    - status       ← from **Status:** field (defaults to DRAFT)
    - confidence   ← UNKNOWN for new artifacts, higher if status is accepted+
    - epistemic_boundary ← from **Platform:** field if present
    """
    if not path.exists():
        return []

    content = path.read_text(encoding="utf-8")
    artifacts: list[BeliefArtifact] = []
    current: BeliefArtifact | None = None
    current_desc = ""

    for line in content.splitlines():
        m = _REQ_HEADING.match(line)
        if m:
            if current is not None:
                _finalise(current, current_desc)
                artifacts.append(current)
            req_id = m.group(1)
            component = m.group(2)
            desc_inline = m.group(4) or ""
            current = BeliefArtifact(
                artifact_id=req_id,
                component=component,
                source_text=desc_inline,
            )
            current_desc = desc_inline
            continue

        if current is None:
            continue

        fm = _FIELD_LINE.match(line)
        if fm:
            key = fm.group(1).lower()
            val = fm.group(2).strip()
            if key in ("description", "desc"):
                current_desc = val
                current.source_text = val
            elif key == "priority":
                current.priority = val
            elif key == "status":
                current.status = _map_status(val)
                current.confidence = _infer_confidence(current.status)
            elif key in ("platform", "platforms"):
                current.epistemic_boundary = [f"Platform: {val}"]
            elif key in ("test", "covers", "tests"):
                pass  # linked tests — not part of BeliefArtifact directly
        else:
            # Inline description continuation (bullet lines)
            stripped = line.strip().lstrip("-").strip()
            if stripped and not stripped.startswith("#") and not current_desc:
                current_desc = stripped

    if current is not None:
        _finalise(current, current_desc)
        artifacts.append(current)

    return artifacts


def _finalise(artifact: BeliefArtifact, desc: str) -> None:
    """Populate propositions from description text."""
    if not desc:
        return
    artifact.source_text = artifact.source_text or desc
    # Split compound claims at semicolons or " and " patterns
    parts = re.split(r";|\band\b(?=\s+[A-Z])", desc)
    artifact.propositions = [p.strip() for p in parts if p.strip()]
    if not artifact.epistemic_boundary:
        artifact.epistemic_boundary = ["Assumed correct project environment"]


def _map_status(val: str) -> BeliefStatus:
    val_lower = val.lower()
    if "accept" in val_lower:
        return BeliefStatus.ACCEPTED
    if "stress" in val_lower:
        return BeliefStatus.STRESS_TESTED
    if "reconstruct" in val_lower:
        return BeliefStatus.RECONSTRUCTED
    if "deprecat" in val_lower:
        return BeliefStatus.DEPRECATED
    return BeliefStatus.DRAFT


def _infer_confidence(status: BeliefStatus) -> ConfidenceLevel:
    return {
        BeliefStatus.DRAFT: ConfidenceLevel.UNKNOWN,
        BeliefStatus.ACCEPTED: ConfidenceLevel.LOW,
        BeliefStatus.STRESS_TESTED: ConfidenceLevel.MEDIUM,
        BeliefStatus.RECONSTRUCTED: ConfidenceLevel.HIGH,
        BeliefStatus.DEPRECATED: ConfidenceLevel.LOW,
    }.get(status, ConfidenceLevel.UNKNOWN)
