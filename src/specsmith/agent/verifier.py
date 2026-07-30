# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Layer1Labs Silicon, Inc. All rights reserved.
"""Real verifier signal for the Grace orchestrator (REQ-108).

Replaces the hardcoded ``0.85 / 0.4 / 0.0`` confidence in
``Orchestrator._build_task_result`` with a real signal derived from:

* test_results (failures > 0  -> confidence <= 0.5)
* ruff_errors  (>= 1          -> confidence x 0.7)
* mypy_errors  (>= 1          -> confidence x 0.8)

Equilibrium is reached only when all three gates are clean **and** the
measured confidence meets or exceeds the preflight ``confidence_target``.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

_FAILURE_COUNT_RE = re.compile(r"\b(\d+)\s+(?:failed|failures?|errors?)\b", re.IGNORECASE)
_PYTEST_FAILURE_LINE_RE = re.compile(r"^\s*(?:FAILED|ERROR)\s+\S+", re.MULTILINE)
_BENIGN_FAILURE_TEXT_RE = re.compile(
    r"\b(?:xfailed|not\s+failed|expected\s+failures?|no\s+failures?)\b",
    re.IGNORECASE,
)
_AMBIGUOUS_FAILURE_RE = re.compile(r"\b(?:failed|failures?|errors?)\b", re.IGNORECASE)


def count_test_failures(test_results: dict[str, Any] | None) -> int:
    """Count real test failures without treating expected failures as failures.

    Explicit structured fields are authoritative. If they are absent, common
    numeric summaries and pytest failure records are parsed. Ambiguous
    unstructured failure text fails closed.
    """
    results = test_results or {}
    structured_seen = False
    structured_invalid = False
    failed = 0
    for key in ("failed", "failures", "errors"):
        if key not in results:
            continue
        structured_seen = True
        value = results.get(key)
        try:
            if isinstance(value, (dict, list, set, tuple)):
                failed += len(value)
            else:
                failed += max(0, int(value or 0))
        except (TypeError, ValueError):
            structured_invalid = True
    if structured_seen:
        return max(failed, 1 if structured_invalid else 0)

    raw_text = str(results.get("raw", "") or "")
    numeric_matches = [int(match.group(1)) for match in _FAILURE_COUNT_RE.finditer(raw_text)]
    if numeric_matches:
        return sum(numeric_matches)

    pytest_records = _PYTEST_FAILURE_LINE_RE.findall(raw_text)
    if pytest_records:
        return len(pytest_records)

    remainder = _BENIGN_FAILURE_TEXT_RE.sub("", raw_text)
    return 1 if _AMBIGUOUS_FAILURE_RE.search(remainder) else 0


@dataclass
class VerifierReport:
    """Inputs to the verifier; produced by parsing the orchestrator output."""

    test_passed: int = 0
    test_failed: int = 0
    ruff_errors: int = 0
    mypy_errors: int = 0
    has_changes: bool = False


@dataclass
class VerifierVerdict:
    """Outputs of the verifier; consumed by the harness."""

    confidence: float
    equilibrium: bool
    summary: str


def score(
    report: VerifierReport,
    *,
    confidence_target: float = 0.7,
) -> VerifierVerdict:
    """Score a :class:`VerifierReport` into a :class:`VerifierVerdict`.

    Deterministic, pure function so the harness behaviour is reproducible.
    """
    base = 1.0 if report.has_changes else 0.0
    if report.test_failed > 0:
        base = min(base, 0.5)
    if report.ruff_errors > 0:
        base *= 0.7
    if report.mypy_errors > 0:
        base *= 0.8
    base = round(max(0.0, min(1.0, base)), 3)

    clean = report.test_failed == 0 and report.ruff_errors == 0 and report.mypy_errors == 0
    equilibrium = clean and report.has_changes and base >= confidence_target

    parts: list[str] = []
    if report.has_changes:
        parts.append(f"{report.test_passed} passed / {report.test_failed} failed")
    else:
        parts.append("no changes detected")
    if report.ruff_errors:
        parts.append(f"{report.ruff_errors} ruff error(s)")
    if report.mypy_errors:
        parts.append(f"{report.mypy_errors} mypy error(s)")
    summary = "; ".join(parts) + (" — equilibrium" if equilibrium else " — retry recommended")

    return VerifierVerdict(confidence=base, equilibrium=equilibrium, summary=summary)


def report_from_chat_sections(
    sections: dict[str, str],
    *,
    files_changed: list[str] | None = None,
) -> VerifierReport:
    """Build a :class:`VerifierReport` from parsed Grace output-contract sections.

    The orchestrator's ``_parse_output_contract`` produces a dict keyed by
    ``plan``, ``commands_to_run``, ``files_changed``, ``diff``,
    ``test_results``, and ``next_action``. We extract structured signals
    from the free-form ``test_results`` text. This is deliberately
    forgiving: passes/failures are counted by simple regex.
    """
    import re

    raw = sections.get("test_results", "") or ""
    test_passed = 0
    test_failed = 0
    m_pass = re.search(r"(\d+)\s+passed", raw, re.IGNORECASE)
    if m_pass:
        test_passed = int(m_pass.group(1))
    m_fail = re.search(r"(\d+)\s+failed", raw, re.IGNORECASE)
    if m_fail:
        test_failed = int(m_fail.group(1))

    diff_text = sections.get("diff", "") or ""
    has_changes = bool(diff_text.strip()) or bool(files_changed)

    # ruff/mypy signals are not in the standard contract; scan the raw test
    # output for the canonical error markers.
    ruff_errors = len(re.findall(r"^\s*[A-Z]\d{3,4}\s", raw, re.MULTILINE))
    mypy_errors = len(re.findall(r"\berror:", raw))

    return VerifierReport(
        test_passed=test_passed,
        test_failed=test_failed,
        ruff_errors=ruff_errors,
        mypy_errors=mypy_errors,
        has_changes=has_changes,
    )


__all__ = [
    "VerifierReport",
    "VerifierVerdict",
    "report_from_chat_sections",
    "score",
]
