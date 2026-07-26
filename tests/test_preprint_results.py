from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

_SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from govern_bench.render_preprint_results import render_results  # noqa: E402


def _summary(
    *,
    repetitions: int = 10,
    tasks: list[str] | None = None,
    runs: int = 80,
) -> dict:
    metrics = {
        "runs": float(runs),
        "pass_rate": 1.0,
        "tokens_per_correct_answer": 100.0,
        "cost_of_pass": 0.01,
    }
    return {
        "schema": "governancebench-model-comparison-v1",
        "tasks": tasks or ["T1", "T2", "T6", "T7", "T10", "T11", "T13", "T28"],
        "comparisons": [
            {
                "smaller_model": "gpt-5.6-terra",
                "stronger_model": "gpt-5.6-sol",
                "smaller_full": metrics,
                "smaller_ungoverned": metrics,
                "stronger_full": metrics,
                "stronger_ungoverned": metrics,
                "inference": {
                    "minimum_repetitions_per_task": repetitions,
                    "point": {"tpca_ratio": 0.7},
                    "fixed_suite_95_ci": {
                        "tpca_ratio": [0.6, 0.8],
                        "pass_rate_difference": [-0.04, 0.04],
                    },
                    "task_cluster_95_ci": {
                        "tpca_ratio": [0.5, 0.9],
                        "pass_rate_difference": [-0.05, 0.05],
                    },
                    "claims": {
                        "release_ready": True,
                        "fixed_suite_substitution": True,
                        "cross_task_substitution": True,
                    },
                },
            }
        ],
    }


def test_preprint_renderer_emits_preregistered_claims(tmp_path: Path) -> None:
    summary = tmp_path / "summary.json"
    summary.write_text(json.dumps(_summary()), encoding="utf-8")
    coding_summary = tmp_path / "coding-summary.json"
    coding_summary.write_text(
        json.dumps(
            _summary(
                tasks=["T1", "T2", "T10", "T11", "T13", "T28"],
                runs=60,
            )
        ),
        encoding="utf-8",
    )

    rendered = render_results(
        summary,
        tmp_path / "results.tex",
        workflow_id="12345",
        commit_sha="abcdef123456789",
        coding_summary_path=coding_summary,
    )

    assert "eight-task, four-cell, n=10" in rendered
    assert "0.600--0.800" in rendered
    assert "-4.0--4.0\\,pp" in rendered
    assert "cross-task substitution was supported" in rendered
    assert "abcdef123456" in rendered
    assert "Coding-only sensitivity" in rendered
    assert "60/60 coding cells" in rendered


@pytest.mark.parametrize(
    ("repetitions", "tasks"),
    [
        (5, None),
        (10, ["T1", "T2"]),
    ],
)
def test_preprint_renderer_rejects_nonrelease_evidence(
    tmp_path: Path,
    repetitions: int,
    tasks: list[str] | None,
) -> None:
    summary = tmp_path / "summary.json"
    summary.write_text(
        json.dumps(_summary(repetitions=repetitions, tasks=tasks)),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="require|complete"):
        render_results(
            summary,
            tmp_path / "results.tex",
            workflow_id="12345",
            commit_sha="abcdef",
        )
