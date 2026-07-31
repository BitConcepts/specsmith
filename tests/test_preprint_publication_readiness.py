from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pytest

_SCRIPTS_DIR = Path(__file__).parents[1] / "scripts"
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from govern_bench.export_evidence import export_evidence  # noqa: E402
from govern_bench.harness import (  # noqa: E402
    _build_provider_client,
    _call_huggingface_provider,
    _copy_project_fixture,
    _exec_run_command,
    _exec_run_validator,
    _get_project_dir,
    _has_milestone_packet_argument_error,
    _install_acceptance_oracle,
    _project_pythonpath,
)
from govern_bench.install_demo_deps import collect_requirements  # noqa: E402
from govern_bench.metrics import RunResult, SliceStats  # noqa: E402
from govern_bench.profiles import PROFILES  # noqa: E402
from govern_bench.protocol import (  # noqa: E402
    DEFAULT_PROTOCOL_PATH,
    RECOVERY_PROTOCOL_PATH,
    load_protocol,
    protocol_sha256,
    validate_run_contract,
)
from govern_bench.tasks import get_task  # noqa: E402


def test_frozen_protocol_has_exact_publication_contracts() -> None:
    protocol = load_protocol()

    assert protocol["protocol_id"] == "GB-PREPRINT-2026-07-30-V1"
    assert protocol["status"] == "frozen"
    assert protocol["publication_status"] == "unpublished"
    assert [item["id"] for item in protocol["task_suite"]] == ["T28", "T29", "T30"]
    assert protocol["metrics"]["failed_runs"] == "included_in_all_token_and_cost_denominators"
    assert protocol["promotion_gates"]["admission"]["maximum_total_tokens"] == 30_000
    assert len(protocol_sha256()) == 64

    assert PROFILES["publication-matched"].tasks == ("T28", "T29", "T30")
    assert PROFILES["publication-matched"].conditions == (
        "UNGOVERNED",
        "CURSOR_RULES",
        "SPECSMITH_FULL",
    )
    assert PROFILES["publication-matched"].repetitions == 10


def test_publication_contract_fails_closed_on_drift() -> None:
    protocol_id, digest = validate_run_contract(
        profile="publication-matched",
        tasks=["T28", "T29", "T30"],
        conditions=["UNGOVERNED", "CURSOR_RULES", "SPECSMITH_FULL"],
        repetitions=10,
        provider="openai-responses",
        model="gpt-5.6-terra",
        controller="scalar-milestone-packet-authority-v7",
    )
    assert protocol_id == "GB-PREPRINT-2026-07-30-V1"
    assert digest == hashlib.sha256(DEFAULT_PROTOCOL_PATH.read_bytes()).hexdigest()

    with pytest.raises(ValueError, match="does not match frozen protocol"):
        validate_run_contract(
            profile="publication-matched",
            tasks=["T28", "T30"],
            conditions=["UNGOVERNED", "CURSOR_RULES", "SPECSMITH_FULL"],
            repetitions=10,
            provider="openai-responses",
            model="gpt-5.6-terra",
            controller="scalar-milestone-packet-authority-v7",
        )

    with pytest.raises(ValueError, match="not a frozen route"):
        validate_run_contract(
            profile="publication-matched",
            tasks=["T28", "T29", "T30"],
            conditions=["UNGOVERNED", "CURSOR_RULES", "SPECSMITH_FULL"],
            repetitions=10,
            provider="openai-responses",
            model="unregistered-model",
            controller="scalar-milestone-packet-authority-v7",
        )


def test_recovery_protocol_is_frozen_and_scoped_to_invalidated_t30() -> None:
    protocol = load_protocol(RECOVERY_PROTOCOL_PATH)

    assert protocol["protocol_id"] == "GB-PREPRINT-2026-07-30-V2"
    assert protocol["amendment"]["supersedes_protocol"] == "GB-PREPRINT-2026-07-30-V1"
    assert protocol["amendment"]["invalidated_workflow"] == "30578319069"
    assert protocol["amendment"]["invalidated_stratum"] == "T30"
    assert protocol["amendment"]["preserved_v1_strata"] == ["T28", "T29"]
    assert protocol["controls"]["controller"] == "scalar-milestone-packet-authority-v8"

    profile = PROFILES["publication-real-repository-recovery"]
    assert profile.tasks == ("T30",)
    assert profile.conditions == ("UNGOVERNED", "CURSOR_RULES", "SPECSMITH_FULL")
    assert profile.repetitions == 10

    protocol_id, digest = validate_run_contract(
        profile=profile.name,
        tasks=list(profile.tasks),
        conditions=list(profile.conditions),
        repetitions=profile.repetitions,
        provider="openai-responses",
        model="gpt-5.6-sol",
        controller="scalar-milestone-packet-authority-v8",
    )
    assert protocol_id == "GB-PREPRINT-2026-07-30-V2"
    assert digest == hashlib.sha256(RECOVERY_PROTOCOL_PATH.read_bytes()).hexdigest()


@pytest.mark.parametrize(
    ("provider", "model"),
    [
        ("huggingface", "Qwen/Qwen3.6-27B:deepinfra"),
        ("huggingface", "openai/gpt-oss-20b:nscale"),
        ("huggingface", "Qwen/Qwen3-32B:deepinfra"),
        ("huggingface", "Qwen/Qwen3-Coder-30B-A3B-Instruct:scaleway"),
        ("huggingface", "zai-org/GLM-4.7-Flash:deepinfra"),
        ("huggingface", "Qwen/Qwen3.6-35B-A3B:deepinfra"),
    ],
)
def test_open_model_routes_are_preregistered(provider: str, model: str) -> None:
    protocol_id, digest = validate_run_contract(
        profile="publication-open-admission",
        tasks=["T30"],
        conditions=["SPECSMITH_FULL"],
        repetitions=1,
        provider=provider,
        model=model,
        controller="scalar-milestone-packet-authority-v7",
    )

    assert protocol_id == "GB-PREPRINT-2026-07-30-V1"
    assert digest == protocol_sha256()


def test_compact_evidence_manifest_records_protocol_identity(tmp_path: Path) -> None:
    source = tmp_path / "result.json"
    source.write_text(
        json.dumps(
            [
                {
                    "task": "T30",
                    "category": "real_repository_maintenance",
                    "horizon": "standard",
                    "condition": "SPECSMITH_FULL",
                    "rep": 1,
                    "model": "Qwen/Qwen3.6-27B:deepinfra",
                    "provider": "huggingface",
                    "benchmark_profile": "publication-open-admission",
                    "protocol_id": "GB-PREPRINT-2026-07-30-V1",
                    "protocol_sha256": protocol_sha256(),
                    "passed": True,
                    "input_tokens": 100,
                    "output_tokens": 20,
                    "tokens": 120,
                    "cost_usd": 0.01,
                    "rework_turns": 1,
                    "governance_turns": 0,
                    "llm_turns": 1,
                    "wall_clock_s": 1.0,
                }
            ]
        ),
        encoding="utf-8",
    )

    _, manifest_path = export_evidence(
        [source],
        tmp_path / "evidence",
        workflow_id="frozen-run",
        commit_sha="abc123",
    )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert manifest["schema"] == "governancebench-evidence-v2"
    assert manifest["protocols"] == [
        {
            "protocol_id": "GB-PREPRINT-2026-07-30-V1",
            "protocol_sha256": protocol_sha256(),
        }
    ]


def test_t30_is_a_pinned_real_repository_with_hidden_acceptance(tmp_path: Path) -> None:
    task = get_task("T30")
    source = _get_project_dir(task.project)
    manifest = json.loads((source / "UPSTREAM_MANIFEST.json").read_text(encoding="utf-8"))

    assert task.project == "upstream-itsdangerous-rotation"
    assert task.project_subdir == "itsdangerous_rotation"
    assert task.is_long_horizon
    assert task.max_turns == 12
    assert manifest["commit"] == "672971d66a2ef9f85151e53283113f33d642dabd"
    for item in manifest["files"]:
        assert hashlib.sha256((source / item["path"]).read_bytes()).hexdigest() == item["sha256"]

    project = tmp_path / "itsdangerous"
    _copy_project_fixture(source, project)
    passed, _ = _exec_run_validator(project, task, "python tools/validate_rotation_api.py")
    assert not passed
    passed, _ = _exec_run_validator(project, task, "python tools/validate_rotation_docs.py")
    assert not passed
    _install_acceptance_oracle(task, project)
    passed, output = _exec_run_command(
        project,
        "pytest .governancebench_oracle/test_acceptance.py"
        "::test_pinned_provenance_and_license_are_preserved",
    )
    assert passed, output
    passed, _ = _exec_run_command(project, "pytest .governancebench_oracle")
    assert not passed
    assert str(project / "src") in _project_pythonpath(project)


def test_upstream_dependency_group_is_provisioned() -> None:
    requirements = collect_requirements(Path(__file__).parents[1] / "scripts/govern_bench/projects")

    assert "freezegun" in requirements
    assert "pytest" in requirements
    assert "tox" not in requirements


def test_huggingface_native_transport_normalizes_structured_content(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("HF_TOKEN", "test-token")
    provider, client = _build_provider_client("huggingface")
    captured: dict[str, object] = {}

    def fake_post(
        url: str,
        *,
        body: dict[str, object],
        headers: dict[str, str] | None = None,
        timeout_s: float = 120,
    ) -> dict[str, object]:
        captured.update(url=url, body=body, headers=headers, timeout_s=timeout_s)
        return {
            "choices": [
                {
                    "message": {
                        "content": {"text": "structured provider content"},
                        "tool_calls": [
                            {
                                "id": "call-1",
                                "function": {
                                    "name": "read_file",
                                    "arguments": {"path": "README.md"},
                                },
                            }
                        ],
                    },
                    "finish_reason": "tool_calls",
                }
            ],
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 4,
                "prompt_tokens_details": {"cached_tokens": 2},
            },
        }

    monkeypatch.setattr("govern_bench.harness._http_post_json", fake_post)
    response = _call_huggingface_provider(
        client,
        "Qwen/Qwen3-Coder-30B-A3B-Instruct:scaleway",
        [{"role": "user", "content": "inspect"}],
        [],
        tool_choice="auto",
        timeout_s=30,
    )

    assert provider == "huggingface"
    assert response.message.content == '{"text": "structured provider content"}'
    assert response.message.tool_calls[0].name == "read_file"
    assert response.message.tool_calls[0].arguments == '{"path": "README.md"}'
    assert response.usage.prompt_tokens == 10
    assert response.usage.completion_tokens == 4
    assert response.usage.cached_tokens == 2
    assert captured["url"] == "https://router.huggingface.co/v1/chat/completions"
    assert captured["headers"] == {"Authorization": "Bearer test-token"}
    assert captured["timeout_s"] == 30


def test_milestone_packet_recovery_reads_normalized_tool_content() -> None:
    assert _has_milestone_packet_argument_error(
        [
            {
                "role": "tool",
                "tool_call_id": "call-1",
                "content": (
                    "ERROR: at least path_1 and content_1 are required; "
                    "provide a complete milestone packet"
                ),
            }
        ]
    )
    assert not _has_milestone_packet_argument_error(
        [{"role": "tool", "tool_call_id": "call-2", "content": "OK: wrote files"}]
    )


def test_github_collection_matches_src_layout_runtime_path() -> None:
    workflow = (Path(__file__).parents[1] / ".github/workflows/bench.yml").read_text(
        encoding="utf-8"
    )

    assert workflow.count('PYTHONPATH="$PWD/src:$PWD"') == 2


def test_failed_run_expenditure_is_explicit_and_inclusive() -> None:
    runs = [
        RunResult(
            task_id="T30",
            condition_id="SPECSMITH_FULL",
            rep=1,
            model="candidate",
            input_tokens=800,
            output_tokens=200,
            api_cost_usd=0.10,
            lint_passed=True,
            tests_passed=True,
        ),
        RunResult(
            task_id="T30",
            condition_id="SPECSMITH_FULL",
            rep=2,
            model="candidate",
            input_tokens=2_000,
            output_tokens=1_000,
            api_cost_usd=0.30,
            lint_passed=False,
            tests_passed=False,
        ),
    ]

    stats = SliceStats.from_runs(runs)

    assert stats.pass_rate == 0.5
    assert stats.tokens_per_correct_answer == 4_000
    assert stats.failed_run_count == 1
    assert stats.failed_run_tokens == 3_000
    assert stats.failed_run_cost_usd == pytest.approx(0.30)
    assert stats.failed_token_share == pytest.approx(0.75)
    assert stats.failed_cost_share == pytest.approx(0.75)


def test_open_admission_status_cannot_claim_unearned_promotion() -> None:
    status_path = Path(__file__).parents[1] / "paper/data/publication-open-admission-status.json"
    status = json.loads(status_path.read_text(encoding="utf-8"))

    assert status["protocol_id"] == "GB-PREPRINT-2026-07-30-V1"
    assert status["protocol_sha256"] == protocol_sha256()
    assert len(status["complete_results"]) == 3
    assert all(not row["passed"] and not row["promoted"] for row in status["complete_results"])
    assert status["promotion_outcome"]["admitted_models"] == []
    assert status["promotion_outcome"]["screen_n5_runs"] == []
    assert status["promotion_outcome"]["release_n10_runs"] == []
    assert status["evaluator_disclosure"] == {
        "v1_t30_hidden_stratum_invalidated": True,
        "reason": (
            "The V1 hidden evaluator contained an impossible license-label assertion "
            "and is excluded from correctness inference."
        ),
        "negative_admission_preserved": True,
        "basis": (
            "Each complete open-model cell independently failed the public project-test "
            "gate before hidden-oracle credit; the censoring classifications also do "
            "not depend on the hidden evaluator."
        ),
        "replacement_protocol": "GB-PREPRINT-2026-07-30-V2",
    }
    assert {row["classification"] for row in status["censored_routes"]} == {
        "provider_incompatible",
        "provider_unavailable",
    }
    assert status["expenditure"]["complete_failed_tokens"] == sum(
        row["tokens"] for row in status["complete_results"]
    )
    assert status["expenditure"]["censored_partial_tokens"] == sum(
        row["partial_tokens"] for row in status["censored_routes"]
    )
    assert status["expenditure"]["all_observed_tokens"] == (
        status["expenditure"]["complete_failed_tokens"]
        + status["expenditure"]["censored_partial_tokens"]
    )


def test_v1_invalidation_excludes_only_t30_and_names_frozen_recovery() -> None:
    record_path = Path(__file__).parents[1] / "paper/data/publication-v1-invalidation.json"
    record = json.loads(record_path.read_text(encoding="utf-8"))

    assert record["protocol_id"] == "GB-PREPRINT-2026-07-30-V1"
    assert record["workflow_id"] == "30578319069"
    assert record["discovered_before_publication"] is True
    assert [row["task"] for row in record["invalidated_strata"]] == ["T30"]
    assert {row["task"] for row in record["preserved_strata"]} == {"T28", "T29"}
    assert record["censored_cells"] == [
        {
            "task": "T28",
            "condition": "UNGOVERNED",
            "model": "openai-responses/gpt-5.6-terra",
            "repetitions": [4, 6],
            "classification": "provider_timeout",
        }
    ]
    assert record["recovery"]["protocol_id"] == "GB-PREPRINT-2026-07-30-V2"
    assert (
        record["recovery"]["protocol_sha256"]
        == hashlib.sha256(RECOVERY_PROTOCOL_PATH.read_bytes()).hexdigest()
    )


def test_publication_readiness_status_matches_v2_inference() -> None:
    data_root = Path(__file__).parents[1] / "paper/data"
    status = json.loads(
        (data_root / "publication-readiness-status.json").read_text(encoding="utf-8")
    )
    summary = json.loads(
        (data_root / "preprint-real-repo-v2-30589098641" / "summary.json").read_text(
            encoding="utf-8"
        )
    )

    assert status["preprint_submission_status"] == "not_submitted"
    assert [item["status"] for item in status["items"]] == [
        "complete",
        "complete_for_current_scope",
        "complete",
        "complete",
        "complete_negative",
    ]
    comparison = summary["comparisons"][0]["inference"]
    h3 = status["v2_hypothesis_outcomes"]["H3_terra_full_vs_sol_raw"]
    assert h3["fixed_suite_substitution"] == comparison["claims"]["fixed_suite_substitution"]
    assert h3["cross_task_substitution"] == comparison["claims"]["cross_task_substitution"]
    assert h3["point_tpca_ratio"] == pytest.approx(comparison["point"]["tpca_ratio"], abs=1e-6)

    within = {
        (item["model"], item["baseline_condition"]): item["inference"]["claims"][
            "fixed_suite_substitution"
        ]
        for item in summary["within_model_comparisons"]
    }
    assert within == {
        ("gpt-5.6-terra", "UNGOVERNED"): False,
        ("gpt-5.6-terra", "CURSOR_RULES"): False,
        ("gpt-5.6-sol", "UNGOVERNED"): False,
        ("gpt-5.6-sol", "CURSOR_RULES"): False,
    }
