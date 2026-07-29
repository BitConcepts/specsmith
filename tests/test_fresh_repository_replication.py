from __future__ import annotations

from pathlib import Path

from scripts.govern_bench.harness import (
    _copy_project_fixture,
    _exec_run_command,
    _exec_run_validator,
    _get_project_dir,
    _install_acceptance_oracle,
)
from scripts.govern_bench.tasks import get_task


def test_t29_is_an_independent_bounded_polyglot_repository() -> None:
    incident = get_task("T28")
    release = get_task("T29")

    assert release.is_long_horizon
    assert release.max_turns == incident.max_turns == 20
    assert release.enforce_completion_validators
    assert release.project != incident.project
    assert release.project_subdir == "release_control_plane"
    assert release.expected_files_changed != incident.expected_files_changed
    assert {"python", "go", "typescript", "json-schema", "css"} <= set(release.languages)
    assert [len(milestone["files"]) for milestone in release.milestones] == [3, 2, 4, 1]
    assert "incident" not in release.task_prompt.casefold()
    assert "release" not in incident.task_prompt.casefold()


def test_t29_clean_starter_fails_public_validators_and_hidden_oracle(tmp_path: Path) -> None:
    task = get_task("T29")
    project = tmp_path / "release-control-plane"
    _copy_project_fixture(_get_project_dir(task.project), project)

    for command in (
        "python tools/validate_api.py",
        "python tools/validate_contract.py",
        "python tools/validate_ui.py",
    ):
        passed, _output = _exec_run_validator(project, task, command)
        assert not passed, f"clean T29 starter unexpectedly passed {command}"

    _install_acceptance_oracle(task, project)
    passed, output = _exec_run_command(project, "pytest .governancebench_oracle")
    assert not passed, f"clean T29 starter unexpectedly satisfied its oracle:\n{output}"


def test_t29_uses_separate_validator_and_oracle_sources() -> None:
    root = Path(__file__).resolve().parents[1] / "scripts" / "govern_bench"

    assert (root / "oracles" / "T29" / "test_acceptance.py").is_file()
    assert (root / "projects" / "release_control_plane" / "tools" / "validate_api.py").is_file()
    assert "T28" not in (root / "oracles" / "T29" / "test_acceptance.py").read_text(
        encoding="utf-8"
    )
