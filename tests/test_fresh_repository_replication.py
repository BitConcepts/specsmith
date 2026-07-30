from __future__ import annotations

from pathlib import Path

import pytest

from scripts.govern_bench.harness import (
    _copy_project_fixture,
    _exec_run_command,
    _exec_run_validator,
    _get_project_dir,
    _install_acceptance_oracle,
    _milestone_work_packet,
    _validator_boundaries_for_task,
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
        "python tools/validate_styles.py",
    ):
        passed, _output = _exec_run_validator(project, task, command)
        assert not passed, f"clean T29 starter unexpectedly passed {command}"

    _install_acceptance_oracle(task, project)
    passed, output = _exec_run_command(project, "pytest .governancebench_oracle")
    assert not passed, f"clean T29 starter unexpectedly satisfied its oracle:\n{output}"


def test_t29_milestone_three_validates_css_as_its_own_boundary() -> None:
    task = get_task("T29")
    ui_milestone = task.milestones[2]

    assert "python tools/validate_styles.py" in ui_milestone["validators"]
    assert _validator_boundaries_for_task(task, "python tools/validate_styles.py") == [
        "ui/src/styles.css"
    ]


def test_t29_v6_milestone_three_names_the_playwright_visibility_invariant(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    task = get_task("T29")
    completed = [str(path) for milestone in task.milestones[:2] for path in milestone["files"]]
    monkeypatch.setenv(
        "BENCH_CONTROLLER_EXPERIMENT",
        "scalar-milestone-packet-authority-v6",
    )

    packet = _milestone_work_packet(task, completed)

    assert "Active work packet 3/4: operator UI journey" in packet
    assert "toBeVisible()" in packet
    assert "before filter and approve interactions" in packet


def test_t29_ui_validator_accepts_structural_empty_state_and_css_contract(
    tmp_path: Path,
) -> None:
    task = get_task("T29")
    project = tmp_path / "release-control-plane"
    _copy_project_fixture(_get_project_dir(task.project), project)
    (project / "ui" / "src" / "App.tsx").write_text(
        (
            "useState useEffect loading error environment state approve "
            'releases.length === 0 <p>No releases found</p> <label role="status">'
        ),
        encoding="utf-8",
    )
    (project / "ui" / "src" / "api.ts").write_text(
        (
            'const p = new URLSearchParams(); p.set("environment", environment); '
            'p.set("state", state); fetch(`/api/releases/${encodeURIComponent(id)}`, '
            '{ method: "PATCH" });'
        ),
        encoding="utf-8",
    )
    (project / "ui" / "tests" / "release-control.spec.ts").write_text(
        "page.route selectOption approve toBeVisible",
        encoding="utf-8",
    )
    (project / "ui" / "src" / "styles.css").write_text(
        (
            "button:focus-visible { outline: 2px solid blue; }\n"
            "button:disabled { opacity: .6; }\n"
            "@media (max-width: 40rem) { main { padding: 1rem; } }\n"
        ),
        encoding="utf-8",
    )

    ui_passed, ui_output = _exec_run_validator(project, task, "python tools/validate_ui.py")
    css_passed, css_output = _exec_run_validator(project, task, "python tools/validate_styles.py")

    assert ui_passed, ui_output
    assert css_passed, css_output


def test_t29_uses_separate_validator_and_oracle_sources() -> None:
    root = Path(__file__).resolve().parents[1] / "scripts" / "govern_bench"

    assert (root / "oracles" / "T29" / "test_acceptance.py").is_file()
    assert (root / "projects" / "release_control_plane" / "tools" / "validate_api.py").is_file()
    assert (root / "projects" / "release_control_plane" / "tools" / "validate_styles.py").is_file()
    assert "T28" not in (root / "oracles" / "T29" / "test_acceptance.py").read_text(
        encoding="utf-8"
    )
