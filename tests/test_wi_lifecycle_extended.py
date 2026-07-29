from __future__ import annotations

import json
from pathlib import Path

from click.testing import CliRunner

from specsmith.cli import main
from specsmith.risk import assess_work_item_risk
from specsmith.wi_store import WorkItem, WorkItemStore


def test_verify_cmd_equilibrium_marks_work_item_implemented(tmp_path: Path) -> None:
    store = WorkItemStore(tmp_path)
    wi = store.create("WI-VERIFY01", intent="verify lifecycle wiring")
    assert wi.status == "open"

    diff_path = tmp_path / "changes.diff"
    diff_path.write_text(
        "--- a/src/sample.py\n+++ b/src/sample.py\n@@ -1 +1 @@\n+print('ok')\n",
        encoding="utf-8",
    )
    tests_path = tmp_path / "test-results.json"
    tests_path.write_text('{"passed": 1, "failed": 0}', encoding="utf-8")

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "verify",
            "--project-dir",
            str(tmp_path),
            "--diff",
            str(diff_path),
            "--tests",
            str(tests_path),
            "--changed",
            "src/sample.py",
            "--work-item-id",
            wi.id,
        ],
        env={"SPECSMITH_ALLOW_NON_PIPX": "1"},
    )
    assert result.exit_code == 0

    updated = WorkItemStore(tmp_path).get(wi.id)
    assert updated is not None
    assert updated.status == "implemented"


def test_approve_cmd_sets_human_review_status_approved(tmp_path: Path) -> None:
    store = WorkItemStore(tmp_path)
    wi = store.create("WI-APPROVE02", intent="approval lifecycle wiring")
    assert wi.human_review_status == "pending"

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "approve",
            "implementation",
            "--work-item",
            wi.id,
            "--rationale",
            "Looks good",
            "--project-dir",
            str(tmp_path),
        ],
        env={"SPECSMITH_ALLOW_NON_PIPX": "1"},
    )
    assert result.exit_code == 0

    updated = WorkItemStore(tmp_path).get(wi.id)
    assert updated is not None
    assert updated.human_review_status == "approved"


def test_set_files_touched_sets_files_on_work_item(tmp_path: Path) -> None:
    store = WorkItemStore(tmp_path)
    wi = store.create("WI-FILES03", intent="track touched files")
    assert wi.files_touched == []

    updated = store.set_files_touched(wi.id, ["src/a.py", "tests/test_a.py"])
    assert updated is not None
    assert updated.files_touched == ["src/a.py", "tests/test_a.py"]

    reloaded = WorkItemStore(tmp_path).get(wi.id)
    assert reloaded is not None
    assert reloaded.files_touched == ["src/a.py", "tests/test_a.py"]


def test_verify_cmd_flattens_nested_changed_files_before_persistence(tmp_path: Path) -> None:
    store = WorkItemStore(tmp_path)
    wi = store.create("WI-FILES04", intent="normalize verification paths")
    payload = {
        "diff": "--- a/src/a.py\n+++ b/src/a.py\n@@ -0,0 +1 @@\n+pass\n",
        "files_changed": [
            ["src/a.py"],
            ["tests/test_a.py", "", ["src/a.py", "docs/a.md"]],
            42,
        ],
        "test_results": {"passed": 3, "failed": 0},
        "logs": "tests passed",
    }

    result = CliRunner().invoke(
        main,
        [
            "verify",
            "--stdin",
            "--project-dir",
            str(tmp_path),
            "--work-item-id",
            wi.id,
        ],
        input=json.dumps(payload),
        env={"SPECSMITH_ALLOW_NON_PIPX": "1"},
    )

    assert result.exit_code == 0, result.output
    assert json.loads(result.output)["files_changed"] == [
        "src/a.py",
        "tests/test_a.py",
        "docs/a.md",
    ]
    reloaded = store.get(wi.id)
    assert reloaded is not None
    assert reloaded.files_touched == ["src/a.py", "tests/test_a.py", "docs/a.md"]


def test_risk_assessment_tolerates_tampered_nested_file_paths() -> None:
    item = WorkItem(
        id="WI-TAMPER05",
        test_case_ids=["TEST-027"],
        files_touched=[["src/auth.py"], ["tests/test_auth.py"], 42],  # type: ignore[list-item]
    )

    assessment = assess_work_item_risk(item)

    assert "security_sensitive_paths" in assessment.factors
