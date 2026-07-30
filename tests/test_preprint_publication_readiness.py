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
    _install_acceptance_oracle,
    _project_pythonpath,
)
from govern_bench.install_demo_deps import collect_requirements  # noqa: E402
from govern_bench.metrics import RunResult, SliceStats  # noqa: E402
from govern_bench.profiles import PROFILES  # noqa: E402
from govern_bench.protocol import (  # noqa: E402
    DEFAULT_PROTOCOL_PATH,
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
        )

    with pytest.raises(ValueError, match="not a frozen route"):
        validate_run_contract(
            profile="publication-matched",
            tasks=["T28", "T29", "T30"],
            conditions=["UNGOVERNED", "CURSOR_RULES", "SPECSMITH_FULL"],
            repetitions=10,
            provider="openai-responses",
            model="unregistered-model",
        )


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
    assert task.max_turns == 12
    assert manifest["commit"] == "672971d66a2ef9f85151e53283113f33d642dabd"
    for item in manifest["files"]:
        assert hashlib.sha256((source / item["path"]).read_bytes()).hexdigest() == item["sha256"]

    project = tmp_path / "itsdangerous"
    _copy_project_fixture(source, project)
    passed, _ = _exec_run_validator(project, task, "python tools/validate_rotation_api.py")
    assert not passed
    _install_acceptance_oracle(task, project)
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
