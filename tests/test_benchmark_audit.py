from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pytest
from click.testing import CliRunner

from specsmith.benchmark_audit import (
    _focused_repair_paths,
    audit_benchmark_file,
    audit_benchmark_rows,
    load_benchmark_reference_envelopes,
)
from specsmith.cli import main

_SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))


def _row(
    *,
    condition: str,
    passed: bool,
    input_tokens: int,
    output_tokens: int = 100,
    tests_passed: bool = True,
    task: str = "T28",
    rep: int = 1,
    model: str = "gpt-5.6-sol",
    oracle_passed: bool | None = None,
) -> dict:
    return {
        "task": task,
        "condition": condition,
        "rep": rep,
        "model": model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "llm_turns": 4,
        "passed": passed,
        "tests_passed": tests_passed,
        "project_tests_passed": tests_passed,
        "acceptance_oracle_passed": passed if oracle_passed is None else oracle_passed,
        "skipped": False,
        "error": None,
    }


def test_audit_finds_acceptance_correctness_token_and_context_weaknesses() -> None:
    report = audit_benchmark_rows(
        [
            _row(condition="UNGOVERNED", passed=True, input_tokens=1_000),
            _row(condition="UNGOVERNED", passed=True, input_tokens=1_000, rep=2),
            _row(condition="SPECSMITH_FULL", passed=False, input_tokens=2_000),
            _row(condition="SPECSMITH_FULL", passed=True, input_tokens=2_000, rep=2),
        ]
    )
    codes = {item.code for item in report.weaknesses}

    assert report.complete
    assert report.high_or_critical == 3
    assert report.condition_metrics["SPECSMITH_FULL"]["tokens_per_correct_answer"] == 4_200
    assert {
        "undersampled",
        "acceptance_gap",
        "token_amplification",
        "correctness_regression",
        "context_dominance",
    } <= codes


def test_audit_fails_closed_on_missing_rows_and_bad_shape(tmp_path: Path) -> None:
    artifact = tmp_path / "results.json"
    artifact.write_text(
        json.dumps(
            [
                {
                    **_row(condition="UNGOVERNED", passed=False, input_tokens=0),
                    "skipped": True,
                    "error": "provider unavailable",
                }
            ]
        ),
        encoding="utf-8",
    )

    report = audit_benchmark_file(artifact)
    assert not report.complete
    assert report.valid_rows == 0
    assert report.weaknesses[0].code == "incomplete_evidence"

    with pytest.raises(ValueError, match="JSON list of objects"):
        audit_benchmark_rows(["not-a-row"])  # type: ignore[list-item]

    artifact.write_text(json.dumps({"weaknesses": []}), encoding="utf-8")
    wrong_document = audit_benchmark_file(artifact)
    assert not wrong_document.complete
    assert wrong_document.valid_rows == 0
    assert wrong_document.weaknesses[0].code == "incomplete_evidence"
    assert wrong_document.next_experiment.action == "reject_artifact"

    malformed_row = audit_benchmark_rows([{}])
    assert not malformed_row.complete
    assert malformed_row.weaknesses[0].code == "incomplete_evidence"

    zero_pass = audit_benchmark_rows(
        [_row(condition="SPECSMITH_FULL", passed=False, input_tokens=1_000)]
    )
    assert zero_pass.condition_metrics["SPECSMITH_FULL"]["tokens_per_correct_answer"] is None
    json.dumps(zero_pass.to_dict(), allow_nan=False)

    malformed_grid = audit_benchmark_rows(
        [
            _row(condition="UNGOVERNED", passed=True, input_tokens=100),
            _row(condition="UNGOVERNED", passed=True, input_tokens=100),
            _row(condition="SPECSMITH_LIGHT", passed=True, input_tokens=100),
        ]
    )
    malformed_codes = {item.code for item in malformed_grid.weaknesses}
    assert {"duplicate_cells", "uneven_repetitions"} <= malformed_codes

    missing_grid = audit_benchmark_rows(
        [
            _row(condition="UNGOVERNED", passed=True, input_tokens=100),
            _row(condition="SPECSMITH_FULL", passed=True, input_tokens=100),
            _row(
                condition="UNGOVERNED",
                passed=True,
                input_tokens=100,
                model="open-model",
            ),
        ]
    )
    assert not missing_grid.complete
    assert "missing_cells" in {item.code for item in missing_grid.weaknesses}


@pytest.mark.parametrize(
    "final_diff",
    [
        "--- a/a.txt\n+++ b/a.txt\n@@ -0,0 +1 @@\n+value--- a/b.txt\n",
        "--- a/a.txt\n+++ b/a.txt\n... [diff compacted]\n",
    ],
)
def test_audit_rejects_unreplayable_diff_evidence(final_diff: str) -> None:
    row = _row(condition="UNGOVERNED", passed=True, input_tokens=100)
    row["final_diff"] = final_diff

    report = audit_benchmark_rows([row])

    assert not report.complete
    weakness = next(item for item in report.weaknesses if item.code == "unreplayable_diff")
    assert weakness.severity == "critical"
    assert weakness.tasks == ["T28"]


def test_audit_reports_turn_tool_and_verification_exhaustion() -> None:
    max_turn = _row(condition="UNGOVERNED", passed=False, input_tokens=100)
    max_turn["stop_reason"] = "max_turns"
    repeated = _row(condition="SPECSMITH_LIGHT", passed=False, input_tokens=100)
    repeated["stop_reason"] = "repeated_tool_loop"
    repeated["agent_transcript"] = [
        {"role": "controller", "repeated_tool_target": "write_file:contract.json"}
    ]
    verify = _row(condition="SPECSMITH_FULL", passed=False, input_tokens=100)
    verify["stop_reason"] = "verification_exhausted"
    blank_write = _row(condition="CURSOR_RULES", passed=False, input_tokens=100)
    blank_write["agent_transcript"] = [
        {
            "role": "tool",
            "results": [
                "ERROR: refusing to replace non-empty file backend/main.py with blank content"
            ],
        }
    ]

    report = audit_benchmark_rows([max_turn, repeated, verify, blank_write])
    codes = {item.code for item in report.weaknesses}

    assert {
        "turn_budget_exhausted",
        "repeated_tool_loop",
        "verification_exhausted",
        "blank_overwrite_rejected",
    } <= codes


def test_audit_identifies_repeated_late_repair_and_context_cost() -> None:
    rows: list[dict] = []
    for rep in range(1, 6):
        repaired = rep <= 4
        row = _row(
            condition="SPECSMITH_FULL",
            passed=True,
            input_tokens=4_000 if repaired else 1_000,
            output_tokens=500,
            rep=rep,
        )
        row["llm_turns"] = 10
        row["rework_turns"] = 2 if repaired else 1
        row["agent_transcript"] = [
            {
                "turn": 1,
                "role": "assistant",
                "tool_calls": ["read_file"] * 10,
                "tool_targets": [f"read_file:component/file{index}.py" for index in range(10)],
            },
            *(
                [
                    {
                        "turn": 8,
                        "role": "controller",
                        "focused_repair": (
                            "Public validator repair boundary: deterministic project checks "
                            "-> backend/main.py. Repair now."
                        ),
                    }
                ]
                if repaired
                else []
            ),
        ]
        row["call_usage"] = [
            {"turn": 1, "cached_input_tokens": 100},
            {"turn": 2, "cached_input_tokens": 0},
            {"turn": 3, "cached_input_tokens": 0},
        ]
        rows.append(row)

    report = audit_benchmark_rows(rows)
    codes = {item.code for item in report.weaknesses}

    assert {
        "systematic_repair_hotspot",
        "first_pass_regression",
        "late_boundary_validation",
        "initial_scope_overread",
        "provider_cache_discontinuity",
    } <= codes
    assert report.next_experiment.action == "optimize_and_rerun"


def test_three_row_diagnostic_exposes_unanimous_repair_hotspot() -> None:
    rows = []
    for rep in range(1, 4):
        row = _row(
            condition="SPECSMITH_FULL",
            passed=True,
            input_tokens=10_000,
            rep=rep,
        )
        row["rework_turns"] = 3
        row["agent_transcript"] = [
            {
                "turn": 3,
                "role": "controller",
                "focused_repair": (
                    "Public validator repair boundary: deterministic project checks "
                    "-> backend/main.py."
                ),
            }
        ]
        rows.append(row)

    report = audit_benchmark_rows(rows)

    assert "systematic_repair_hotspot" in {weakness.code for weakness in report.weaknesses}
    assert report.next_experiment.action == "optimize_and_rerun"


def test_repair_path_parser_prefers_observed_patch_and_ignores_supplied_imports() -> None:
    row = {
        "agent_transcript": [
            {
                "turn": 3,
                "role": "controller",
                "focused_repair": (
                    "Active public-validator repair boundary: python tools/validate_ui.py -> "
                    "ui/src/App.tsx, ui/src/api.ts, ui/tests/release-control.spec.ts.\n\n"
                    "## ui/src/App.tsx\n"
                    'import "./styles.css";\n'
                ),
            },
            {
                "turn": 4,
                "role": "assistant",
                "tool_calls": ["patch_file"],
                "tool_targets": ["patch_file:ui/tests/release-control.spec.ts"],
            },
        ]
    }

    assert _focused_repair_paths(row) == ["ui/tests/release-control.spec.ts"]


def test_repair_path_parser_falls_back_to_legacy_boundary_header() -> None:
    row = {
        "agent_transcript": [
            {
                "role": "controller",
                "focused_repair": (
                    "Active public-validator repair boundary: python tools/validate_ui.py "
                    "-> ui/src/App.tsx.\n\n"
                    "## ui/src/App.tsx\n"
                    'import "./styles.css";\n'
                ),
            }
        ]
    }

    assert _focused_repair_paths(row) == ["ui/src/app.tsx"]


def test_repair_hotspot_names_the_observed_patched_file() -> None:
    rows = []
    for rep in range(1, 4):
        row = _row(
            condition="SPECSMITH_FULL",
            passed=True,
            input_tokens=10_000,
            rep=rep,
            task="T29",
        )
        row["rework_turns"] = 2
        row["agent_transcript"] = [
            {
                "turn": 3,
                "role": "controller",
                "focused_repair": (
                    "Active public-validator repair boundary: python tools/validate_ui.py -> "
                    "ui/src/App.tsx, ui/src/api.ts, ui/tests/release-control.spec.ts."
                ),
            },
            {
                "turn": 4,
                "role": "assistant",
                "tool_calls": ["patch_file"],
                "tool_targets": ["patch_file:ui/tests/release-control.spec.ts"],
            },
        ]
        rows.append(row)

    report = audit_benchmark_rows(rows)
    weakness = next(item for item in report.weaknesses if item.code == "systematic_repair_hotspot")

    assert "ui/tests/release-control.spec.ts" in weakness.evidence
    assert "ui/src/app.tsx" not in weakness.evidence


def test_default_run_bench_audit_path_tracks_json_output() -> None:
    from govern_bench.run_bench import _default_audit_path

    args = argparse.Namespace(
        audit_output=None,
        json_output="artifacts/bench-results.json",
        output="report.md",
    )
    assert _default_audit_path(args) == Path("artifacts/bench-results.audit.json")


def test_file_audit_infers_dry_run_provenance(tmp_path: Path) -> None:
    artifact = tmp_path / "dry.json"
    row = _row(condition="UNGOVERNED", passed=True, input_tokens=100)
    row["dry_run"] = True
    artifact.write_text(json.dumps([row]), encoding="utf-8")

    report = audit_benchmark_file(artifact)

    assert report.dry_run
    assert report.weaknesses[0].code == "synthetic_evidence"
    assert report.next_experiment.action == "reject_artifact"
    assert not report.next_experiment.ready_for_repetition


def test_audit_selects_next_experiment_from_measured_evidence() -> None:
    correct_diagnostic = audit_benchmark_rows(
        [
            _row(
                condition="CURSOR_RULES",
                passed=True,
                input_tokens=2_000,
                output_tokens=300,
            ),
            _row(
                condition="SPECSMITH_FULL",
                passed=True,
                input_tokens=1_000,
                output_tokens=300,
            ),
        ]
    )
    assert correct_diagnostic.next_experiment.action == "repeat_screen"
    assert correct_diagnostic.next_experiment.ready_for_repetition

    cursor_only_scope = _row(
        condition="CURSOR_RULES",
        passed=True,
        input_tokens=2_000,
        output_tokens=300,
    )
    cursor_only_scope["expected_files_changed"] = ["expected.py"]
    cursor_only_scope["files_written"] = ["extra.py"]
    governed_clean = _row(
        condition="SPECSMITH_FULL",
        passed=True,
        input_tokens=1_000,
        output_tokens=300,
    )
    baseline_weakness = audit_benchmark_rows([cursor_only_scope, governed_clean])
    assert baseline_weakness.next_experiment.action == "repeat_screen"

    cache_observation_rows = []
    for rep in range(1, 6):
        row = _row(
            condition="SPECSMITH_FULL",
            passed=True,
            input_tokens=1_000,
            output_tokens=300,
            rep=rep,
        )
        row["call_usage"] = [
            {"turn": 1, "cached_input_tokens": 100},
            {"turn": 2, "cached_input_tokens": 0},
            {"turn": 3, "cached_input_tokens": 0},
        ]
        cache_observation_rows.append(row)
    cache_observation = audit_benchmark_rows(cache_observation_rows)
    assert "provider_cache_discontinuity" in {
        weakness.code for weakness in cache_observation.weaknesses
    }
    assert cache_observation.next_experiment.action == "expand_release_sample"
    assert cache_observation.next_experiment.ready_for_repetition

    schema_churn_rows = []
    for rep in range(1, 6):
        row = _row(
            condition="SPECSMITH_FULL",
            passed=True,
            input_tokens=1_000,
            output_tokens=300,
            rep=rep,
        )
        row["call_usage"] = [
            {"turn": 1, "tool_schema_hash": "schema-a"},
            {"turn": 2, "tool_schema_hash": "schema-b"},
        ]
        schema_churn_rows.append(row)
    schema_churn = audit_benchmark_rows(schema_churn_rows)
    assert "tool_schema_discontinuity" in {weakness.code for weakness in schema_churn.weaknesses}
    assert schema_churn.next_experiment.action == "optimize_and_rerun"

    correctness_failure = audit_benchmark_rows(
        [
            _row(condition="CURSOR_RULES", passed=True, input_tokens=1_000),
            _row(condition="SPECSMITH_FULL", passed=False, input_tokens=1_000),
        ]
    )
    assert correctness_failure.next_experiment.action == "repair_and_rerun"
    assert "cursor_correctness_regression" in correctness_failure.next_experiment.evidence_codes

    inefficient = audit_benchmark_rows(
        [
            _row(
                condition="CURSOR_RULES",
                passed=True,
                input_tokens=1_000,
                output_tokens=300,
            ),
            _row(
                condition="SPECSMITH_FULL",
                passed=True,
                input_tokens=2_000,
                output_tokens=300,
            ),
        ]
    )
    assert inefficient.next_experiment.action == "optimize_and_rerun"
    assert "cursor_efficiency_regression" in inefficient.next_experiment.evidence_codes

    standalone_failure = audit_benchmark_rows(
        [
            _row(
                condition="SPECSMITH_FULL",
                passed=False,
                input_tokens=1_000,
                model="open-model",
            )
        ]
    )
    assert standalone_failure.next_experiment.action == "repair_and_rerun"
    assert "governed_failure" in standalone_failure.next_experiment.evidence_codes


def test_frontier_reference_blocks_expensive_candidate_repetition(tmp_path: Path) -> None:
    references = {
        "T28": {
            "condition": "SPECSMITH_FULL",
            "model": "gpt-5.6-sol",
            "tokens_per_correct_answer": 32_000,
            "repetitions": 5,
            "commit": "anchor-commit",
            "source": "https://example.invalid/run/1",
        }
    }
    candidate = audit_benchmark_rows(
        [
            _row(
                condition="SPECSMITH_FULL",
                passed=True,
                input_tokens=70_000,
                model="glm-5.2",
            )
        ],
        reference_envelopes=references,
    )
    assert candidate.next_experiment.action == "advance_candidate"
    assert candidate.next_experiment.ready_for_repetition is False
    assert "frontier_efficiency_regression" in {weakness.code for weakness in candidate.weaknesses}

    stale = tmp_path / "references.json"
    stale.write_text(
        json.dumps(
            {
                "tasks": {
                    "T28": {
                        **references["T28"],
                        "repetitions": 1,
                    }
                }
            }
        ),
        encoding="utf-8",
    )
    assert load_benchmark_reference_envelopes(stale) == {}


def test_release_reference_blocks_same_model_controller_regression() -> None:
    references = {
        "T10": {
            "condition": "SPECSMITH_FULL",
            "model": "gpt-5.6-sol",
            "tokens_per_correct_answer": 14_000,
            "repetitions": 10,
            "commit": "anchor-commit",
            "source": "https://example.invalid/run/2",
        }
    }
    candidate = audit_benchmark_rows(
        [
            _row(
                task="T10",
                condition="SPECSMITH_FULL",
                passed=True,
                input_tokens=60_000,
                model="gpt-5.6-sol",
            )
        ],
        reference_envelopes=references,
    )

    assert candidate.next_experiment.action == "optimize_and_rerun"
    assert candidate.next_experiment.ready_for_repetition is False
    assert "controller_efficiency_regression" in candidate.next_experiment.evidence_codes


def test_shipped_frontier_reference_tracks_release_quality_sol_screen() -> None:
    references = load_benchmark_reference_envelopes()
    reference = references["T28"]

    assert reference["condition"] == "SPECSMITH_FULL"
    assert reference["model"] == "gpt-5.6-sol"
    assert reference["tokens_per_correct_answer"] == pytest.approx(17_501.7)
    assert reference["repetitions"] == 10
    assert reference["commit"] == "71b316fd9b4d857bf07d913cdc0fe33b5732f38e"
    assert reference["source"].endswith("/actions/runs/30199359636")
    assert references["T1"]["tokens_per_correct_answer"] == pytest.approx(10_215.8)
    assert references["T10"]["tokens_per_correct_answer"] == pytest.approx(13_841.7)
    assert references["T13"]["tokens_per_correct_answer"] == pytest.approx(10_742.3)


def test_specsmith_audit_writes_combined_project_and_benchmark_report(tmp_path: Path) -> None:
    benchmark = tmp_path / "benchmark.json"
    benchmark.write_text(
        json.dumps(
            [
                _row(condition="UNGOVERNED", passed=True, input_tokens=1_000),
                _row(condition="SPECSMITH_FULL", passed=False, input_tokens=2_000),
            ]
        ),
        encoding="utf-8",
    )
    output = tmp_path / "audit.json"

    result = CliRunner().invoke(
        main,
        [
            "audit",
            "--project-dir",
            str(tmp_path),
            "--benchmark-results",
            str(benchmark),
            "--report",
            str(output),
        ],
        env={"SPECSMITH_ALLOW_NON_PIPX": "1", "SPECSMITH_NO_AUTO_UPDATE": "1"},
    )

    assert result.exit_code == 1
    assert "Benchmark outcome weaknesses" in result.output
    assert "acceptance_gap" in result.output
    assert "Next experiment: repair_and_rerun" in result.output
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["project"]["healthy"] is False
    assert payload["benchmark"]["high_or_critical"] == 3
