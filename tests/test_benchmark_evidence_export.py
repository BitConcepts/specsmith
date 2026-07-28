from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

import pytest

_SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from govern_bench.export_evidence import (  # noqa: E402
    EXCLUDED_FIELDS,
    export_evidence,
    verify_evidence,
)


def _row(**overrides: object) -> dict:
    row = {
        "task": "T1",
        "category": "bugfix",
        "horizon": "standard",
        "condition": "SPECSMITH_FULL",
        "rep": 1,
        "model": "gpt-5.6-terra",
        "provider": "openai",
        "benchmark_profile": "substitution-release",
        "dry_run": False,
        "skipped": False,
        "error": None,
        "passed": True,
        "acceptance_oracle_passed": True,
        "project_tests_passed": True,
        "input_tokens": 100,
        "output_tokens": 20,
        "cached_input_tokens": 40,
        "cache_write_tokens": 0,
        "tokens": 120,
        "cost_usd": 0.004,
        "rework_turns": 1,
        "governance_turns": 2,
        "llm_turns": 2,
        "wall_clock_s": 1.25,
        "stop_reason": "done",
        "expected_files_changed": ["app.py"],
        "files_written": ["app.py"],
        "languages": ["python"],
        "call_usage": [{"tool_schema_hash": "abc123"}],
        "agent_transcript": [{"content": "private prompt"}],
        "final_diff": "secret source patch",
        "governance_decision": {"instruction": "private"},
        "lint_output": "verbose",
        "test_output": "verbose",
        "verify_result": {"summary": "private"},
    }
    row.update(overrides)
    return row


def test_export_is_compact_hashed_and_excludes_trace_payloads(tmp_path: Path) -> None:
    source = tmp_path / "bench-results.json"
    source.write_text(json.dumps([_row()]), encoding="utf-8")

    cells_path, manifest_path = export_evidence(
        [source],
        tmp_path / "evidence",
        workflow_id="12345",
        commit_sha="abcde",
    )

    rows = list(csv.DictReader(cells_path.open(encoding="utf-8")))
    assert rows[0]["workflow_id"] == "12345"
    assert rows[0]["model"] == "gpt-5.6-terra"
    assert rows[0]["tool_schema_hashes"] == "abc123"
    serialized = cells_path.read_text(encoding="utf-8")
    assert "private prompt" not in serialized
    assert "secret source patch" not in serialized
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["row_count"] == 1
    assert set(EXCLUDED_FIELDS) <= set(manifest["excluded_fields"])
    assert len(manifest["cells_csv_sha256"]) == 64
    assert len(manifest["cells_canonical_sha256"]) == 64
    verified = verify_evidence(manifest_path, source_dir=tmp_path)
    assert verified["rows"] == 1
    assert verified["verified_sources"] == 1


@pytest.mark.parametrize(
    "overrides",
    [
        {"dry_run": True},
        {"skipped": True},
        {"error": "provider failed"},
    ],
)
def test_export_rejects_incomplete_evidence(tmp_path: Path, overrides: dict) -> None:
    source = tmp_path / "bench-results.json"
    source.write_text(json.dumps([_row(**overrides)]), encoding="utf-8")

    with pytest.raises(ValueError, match="rejects"):
        export_evidence(
            [source],
            tmp_path / "evidence",
            workflow_id="12345",
            commit_sha="abcde",
        )


def test_export_rejects_duplicate_cells(tmp_path: Path) -> None:
    source = tmp_path / "bench-results.json"
    source.write_text(json.dumps([_row(), _row()]), encoding="utf-8")

    with pytest.raises(ValueError, match="duplicate"):
        export_evidence(
            [source],
            tmp_path / "evidence",
            workflow_id="12345",
            commit_sha="abcde",
        )


def test_verifier_rejects_tampered_compact_data(tmp_path: Path) -> None:
    source = tmp_path / "bench-results.json"
    source.write_text(json.dumps([_row()]), encoding="utf-8")
    cells_path, manifest_path = export_evidence(
        [source],
        tmp_path / "evidence",
        workflow_id="12345",
        commit_sha="abcde",
    )
    cells_path.write_text(cells_path.read_text(encoding="utf-8") + "tampered\n")

    with pytest.raises(ValueError, match="SHA-256"):
        verify_evidence(manifest_path)


def test_verifier_finds_sources_in_nested_download_tree(tmp_path: Path) -> None:
    source = tmp_path / "download" / "bench-model-run" / "bench-results.json"
    source.parent.mkdir(parents=True)
    source.write_text(json.dumps([_row()]), encoding="utf-8")
    _, manifest_path = export_evidence(
        [source],
        tmp_path / "evidence",
        workflow_id="12345",
        commit_sha="abcde",
    )

    verified = verify_evidence(manifest_path, source_dir=tmp_path / "download")

    assert verified["verified_sources"] == 1


def test_verifier_rejects_ambiguous_nested_source_names(tmp_path: Path) -> None:
    source = tmp_path / "download" / "first" / "bench-results.json"
    source.parent.mkdir(parents=True)
    source.write_text(json.dumps([_row()]), encoding="utf-8")
    _, manifest_path = export_evidence(
        [source],
        tmp_path / "evidence",
        workflow_id="12345",
        commit_sha="abcde",
    )
    duplicate = tmp_path / "download" / "second" / source.name
    duplicate.parent.mkdir(parents=True)
    duplicate.write_bytes(source.read_bytes())

    with pytest.raises(ValueError, match="ambiguous raw source artifact"):
        verify_evidence(manifest_path, source_dir=tmp_path / "download")


@pytest.mark.parametrize(
    ("directory", "workflow_id", "tokens", "stop_reason"),
    [
        ("qwen-native-tools-30317439173", "30317439173", "123384", "max_turns"),
        ("qwen-native-tools-scoped-30317963475", "30317963475", "34892", "text_response"),
        ("qwen-native-tools-required-30318295306", "30318295306", "81648", "empty_response"),
    ],
)
def test_committed_qwen_native_tool_evidence_is_verifiable(
    directory: str,
    workflow_id: str,
    tokens: str,
    stop_reason: str,
) -> None:
    evidence_dir = _SCRIPTS_DIR.parent / "paper" / "data" / directory

    verified = verify_evidence(evidence_dir / "manifest.json")
    rows = list(csv.DictReader((evidence_dir / "cells.csv").open(encoding="utf-8")))

    assert verified["rows"] == 1
    assert rows[0]["workflow_id"] == workflow_id
    assert rows[0]["tokens"] == tokens
    assert rows[0]["stop_reason"] == stop_reason
    assert rows[0]["passed"] == "False"


def test_native_qwen_parser_censor_receipt_is_not_a_model_result() -> None:
    receipt_path = (
        _SCRIPTS_DIR.parent
        / "paper"
        / "data"
        / "qwen-native-parser-censored-30317300977"
        / "receipt.json"
    )
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))

    assert receipt["status"] == "censored_before_provisioning"
    assert receipt["endpoint_created"] is False
    assert receipt["model_request_sent"] is False
    assert receipt["endpoint_compute_cost_usd"] == 0.0
    assert receipt["attempted_tool_parser"] == "qwen3_xml"


@pytest.mark.parametrize("script", ["export_evidence.py", "compare_runs.py"])
def test_reproduction_scripts_run_directly_from_repository(script: str) -> None:
    completed = subprocess.run(
        [
            sys.executable,
            str(_SCRIPTS_DIR / "govern_bench" / script),
            "--help",
        ],
        cwd=_SCRIPTS_DIR.parent,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert "usage:" in completed.stdout
