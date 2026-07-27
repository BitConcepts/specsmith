from __future__ import annotations

import sys
from pathlib import Path

import pytest

from specsmith.benchmark_audit import audit_benchmark_rows

_SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from govern_bench.harness import _openai_sampling_params  # noqa: E402
from govern_bench.metrics import estimate_cost, model_tier  # noqa: E402
from govern_bench.select_models import load_registry, select  # noqa: E402


def test_mid_model_admission_cohort_has_exact_routes_prices_and_sampling() -> None:
    registry = load_registry(_SCRIPTS_DIR / "govern_bench" / "models.yml")
    candidates = select(registry, groups={"open-mid-admission"})

    assert {candidate["label"] for candidate in candidates} == {
        "qwen3.6-27b",
        "gpt-oss-20b",
        "qwen3-coder-30b",
        "glm-4.7-flash",
    }
    assert all(candidate["provider"] == "huggingface" for candidate in candidates)
    assert all(model_tier(candidate["model"]) == "open-mid" for candidate in candidates)
    expected_costs = {
        "Qwen/Qwen3.6-27B:deepinfra": 3.52,
        "openai/gpt-oss-20b:nscale": 0.25,
        "Qwen/Qwen3-Coder-30B-A3B-Instruct:scaleway": 1.14,
        "zai-org/GLM-4.7-Flash:deepinfra": 0.46,
    }
    for candidate in candidates:
        assert estimate_cost(candidate["model"], 1_000_000, 1_000_000) == pytest.approx(
            expected_costs[candidate["model"]]
        )

    assert _openai_sampling_params("Qwen/Qwen3-Coder-30B-A3B-Instruct:scaleway") == {
        "temperature": 0.7,
        "top_p": 0.8,
    }
    assert _openai_sampling_params("zai-org/GLM-4.7-Flash:deepinfra") == {
        "temperature": 0.7,
        "top_p": 1.0,
    }


def test_near_mid_followup_has_exact_route_price_tier_and_sampling() -> None:
    registry = load_registry(_SCRIPTS_DIR / "govern_bench" / "models.yml")
    candidates = select(registry, groups={"open-mid-followup"})

    assert candidates == [
        {
            "label": "qwen3-32b",
            "provider": "huggingface",
            "model": "Qwen/Qwen3-32B:deepinfra",
            "group": "open-mid-followup",
            "tier": "open-mid",
        }
    ]
    assert model_tier(candidates[0]["model"]) == "open-mid"
    assert estimate_cost(candidates[0]["model"], 1_000_000, 1_000_000) == pytest.approx(0.36)
    assert _openai_sampling_params(candidates[0]["model"]) == {
        "temperature": 0.6,
        "top_p": 0.95,
    }


def test_suspended_initial_reads_are_not_reported_as_loaded_context() -> None:
    row = {
        "task": "T28",
        "condition": "SPECSMITH_FULL",
        "rep": 1,
        "model": "mid-model",
        "input_tokens": 1_000,
        "output_tokens": 100,
        "llm_turns": 2,
        "passed": True,
        "tests_passed": True,
        "project_tests_passed": True,
        "acceptance_oracle_passed": True,
        "skipped": False,
        "error": None,
        "agent_transcript": [
            {
                "turn": 1,
                "role": "assistant",
                "tool_targets": [
                    "read_files:" + ",".join(f"component/file{i}.py" for i in range(10))
                ],
            },
            {
                "turn": 1,
                "role": "tool",
                "suppressed_unchanged_reads": [f"component/file{i}.py" for i in range(10)],
            },
        ],
    }

    report = audit_benchmark_rows([row])

    assert "initial_scope_overread" not in {item.code for item in report.weaknesses}
