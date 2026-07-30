from __future__ import annotations

import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from specsmith.agent.broker import PreflightDecision, classify_retry_strategy
from specsmith.agent.verifier import count_test_failures
from specsmith.cli import main
from specsmith.governance_logic import run_verify


@pytest.mark.parametrize(
    ("test_results", "expected"),
    (
        ({"raw": "2287 passed, 6 skipped, 5 xfailed"}, 0),
        ({"raw": "10 passed, 0 failed"}, 0),
        ({"raw": "10 passed, 1 failed"}, 1),
        ({"raw": "FAILED tests/test_x.py::test_y"}, 1),
        ({"raw": "ERROR collecting tests/test_x.py"}, 1),
        ({"raw": "tests not failed; one expected failure"}, 0),
        ({"raw": "tests failed for an unknown reason"}, 1),
        ({"failed": 0, "errors": 0, "raw": "FAILED stale text"}, 0),
        ({"failed": 1, "raw": "10 passed"}, 1),
        ({"failed": "unknown", "raw": "10 passed"}, 1),
    ),
)
def test_count_test_failures_uses_structured_counts_and_result_grammar(
    test_results: dict[str, object],
    expected: int,
) -> None:
    assert count_test_failures(test_results) == expected


def test_run_verify_accepts_expected_failures(tmp_path: Path) -> None:
    result = run_verify(
        diff="+ verified change",
        files_changed=["src/example.py"],
        test_results={
            "passed": 2287,
            "failed": 0,
            "errors": 0,
            "skipped": 6,
            "xfailed": 5,
            "raw": "2287 passed, 6 skipped, 5 xfailed",
        },
        project_dir=tmp_path,
    )

    assert result["equilibrium"] is True
    assert result["retry_strategy"] == ""


def test_cli_verify_and_retry_classifier_share_failure_grammar(tmp_path: Path) -> None:
    payload = {
        "diff": "+ verified change",
        "files_changed": ["src/example.py"],
        "test_results": {"raw": "10 passed, 5 xfailed"},
    }
    cli_result = CliRunner().invoke(
        main,
        ["verify", "--project-dir", str(tmp_path), "--stdin"],
        input=json.dumps(payload),
        env={
            "SPECSMITH_ALLOW_NON_PIPX": "1",
            "SPECSMITH_NO_AUTO_UPDATE": "1",
        },
    )

    assert cli_result.exit_code == 0, cli_result.output
    assert json.loads(cli_result.output)["equilibrium"] is True

    decision = PreflightDecision(
        raw={},
        decision="accepted",
        confidence_target=0.8,
    )
    report = {
        "confidence": 0.4,
        "summary": "",
        "test_results": {"raw": "10 passed, 5 xfailed"},
    }
    assert classify_retry_strategy(report, decision) != "fix_tests"


def test_cli_verify_fails_closed_on_pytest_failure_record(tmp_path: Path) -> None:
    payload = {
        "diff": "+ broken change",
        "files_changed": ["src/example.py"],
        "test_results": {"raw": "FAILED tests/test_x.py::test_y"},
    }
    result = CliRunner().invoke(
        main,
        ["verify", "--project-dir", str(tmp_path), "--stdin"],
        input=json.dumps(payload),
        env={
            "SPECSMITH_ALLOW_NON_PIPX": "1",
            "SPECSMITH_NO_AUTO_UPDATE": "1",
        },
    )

    assert result.exit_code == 2
    output = json.loads(result.output)
    assert output["equilibrium"] is False
    assert output["retry_strategy"] == "fix_tests"
