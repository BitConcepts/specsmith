# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Layer1Labs Silicon, Inc. All rights reserved.
"""Regression coverage for multi-segment governance identifiers (issue #364)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from specsmith.cli import main
from specsmith.governance_logic import run_preflight


def _seed_machine_state(project: Path) -> None:
    state = project / ".specsmith"
    state.mkdir()
    requirements = [
        {"id": "REQ-001"},
        {"id": "REQ-CORE-007"},
        {"id": "REQ-EG-MEM-003"},
        {"id": "REQ-CORE2_MEM-004"},
    ]
    testcases = [
        {"id": "TEST-001", "requirement_id": "REQ-001"},
        {"id": "TEST-CORE-007", "requirement_id": "REQ-CORE-007"},
        {"id": "TEST-EG-017", "requirement_id": "REQ-EG-MEM-003"},
        {"id": "TEST-EG-MEM-017b", "requirement_id": "REQ-EG-MEM-003"},
        {"id": "TEST-CORE2_MEM-004a", "requirement_id": "REQ-CORE2_MEM-004"},
    ]
    (state / "requirements.json").write_text(json.dumps(requirements), encoding="utf-8")
    (state / "testcases.json").write_text(json.dumps(testcases), encoding="utf-8")


@pytest.mark.parametrize(
    ("req_id", "linked_tests"),
    [
        ("REQ-001", ["TEST-001"]),
        ("REQ-CORE-007", ["TEST-CORE-007"]),
        ("REQ-EG-MEM-003", ["TEST-EG-017", "TEST-EG-MEM-017b"]),
        ("REQ-CORE2_MEM-004", ["TEST-CORE2_MEM-004a"]),
    ],
)
def test_direct_requirement_ids_use_one_shared_multi_segment_grammar(
    tmp_path: Path,
    req_id: str,
    linked_tests: list[str],
) -> None:
    _seed_machine_state(tmp_path)

    result = run_preflight(
        f"Implement the governed behavior for {req_id}",
        project_dir=tmp_path,
        predict_only=True,
    )

    assert result["decision"] == "accepted"
    assert result["requirement_ids"] == [req_id]
    assert result["test_case_ids"] == linked_tests


@pytest.mark.parametrize(
    "test_id",
    ["TEST-001", "TEST-CORE-007", "TEST-EG-017", "TEST-EG-MEM-017b", "TEST-CORE2_MEM-004a"],
)
def test_direct_test_ids_use_one_shared_multi_segment_grammar(
    tmp_path: Path,
    test_id: str,
) -> None:
    _seed_machine_state(tmp_path)

    result = run_preflight(
        f"Implement REQ-001 and verify the independent case {test_id}",
        project_dir=tmp_path,
        predict_only=True,
    )

    assert result["decision"] == "accepted"
    assert test_id in result["test_case_ids"]


def test_unknown_multi_segment_identifier_still_fails_closed(tmp_path: Path) -> None:
    _seed_machine_state(tmp_path)

    result = run_preflight(
        "Implement the governed behavior for REQ-EG-MEM-999",
        project_dir=tmp_path,
        predict_only=True,
    )

    assert result["decision"] == "needs_clarification"
    assert result["requirement_ids"] == []
    assert result["test_case_ids"] == []


def test_preflight_req_flag_accepts_known_multi_segment_identifier(tmp_path: Path) -> None:
    _seed_machine_state(tmp_path)

    result = CliRunner().invoke(
        main,
        [
            "preflight",
            "Implement bounded private organism memory",
            "--project-dir",
            str(tmp_path),
            "--req",
            "REQ-EG-MEM-003",
            "--predict-only",
            "--json",
        ],
    )

    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["decision"] == "accepted"
    assert payload["requirement_ids"] == ["REQ-EG-MEM-003"]
    assert payload["test_case_ids"] == ["TEST-EG-017", "TEST-EG-MEM-017b"]
