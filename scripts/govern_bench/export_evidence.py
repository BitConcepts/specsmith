"""Export a compact, reproducible, privacy-safe benchmark evidence bundle."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from govern_bench.metrics import model_tier

LEGACY_SCHEMA_VERSION = "governancebench-evidence-v1"
SCHEMA_VERSION = "governancebench-evidence-v2"
LEGACY_CELL_FIELDS = (
    "workflow_id",
    "commit_sha",
    "task",
    "category",
    "horizon",
    "condition",
    "rep",
    "model",
    "provider",
    "model_tier",
    "benchmark_profile",
    "passed",
    "acceptance_oracle_passed",
    "project_tests_passed",
    "input_tokens",
    "output_tokens",
    "cached_input_tokens",
    "cache_write_tokens",
    "tokens",
    "cost_usd",
    "rework_turns",
    "governance_turns",
    "llm_turns",
    "wall_clock_s",
    "stop_reason",
    "expected_file_count",
    "written_file_count",
    "language_count",
    "tool_schema_hashes",
)
CELL_FIELDS = (
    *LEGACY_CELL_FIELDS[:-2],
    "milestones_completed",
    "milestones_total",
    "tokens_per_completed_milestone",
    *LEGACY_CELL_FIELDS[-2:],
)
SCHEMA_FIELDS = {
    LEGACY_SCHEMA_VERSION: LEGACY_CELL_FIELDS,
    SCHEMA_VERSION: CELL_FIELDS,
}
EXCLUDED_FIELDS = (
    "agent_transcript",
    "final_diff",
    "governance_decision",
    "lint_output",
    "test_output",
    "verify_result",
)


def _digest_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _load_rows(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list) or not all(isinstance(row, dict) for row in payload):
        raise ValueError(f"{path}: expected a JSON array of benchmark rows")
    return payload


def _cell(
    row: dict[str, Any],
    *,
    workflow_id: str,
    commit_sha: str,
) -> dict[str, Any]:
    if row.get("dry_run") or row.get("skipped") or row.get("error"):
        raise ValueError("evidence export rejects dry-run, skipped, and errored cells")
    hashes = sorted(
        {
            str(call.get("tool_schema_hash"))
            for call in (row.get("call_usage") or [])
            if isinstance(call, dict) and call.get("tool_schema_hash")
        }
    )
    model = str(row.get("model") or "")
    return {
        "workflow_id": workflow_id,
        "commit_sha": commit_sha,
        "task": str(row.get("task") or ""),
        "category": str(row.get("category") or ""),
        "horizon": str(row.get("horizon") or ""),
        "condition": str(row.get("condition") or ""),
        "rep": int(row.get("rep") or 0),
        "model": model,
        "provider": str(row.get("provider") or ""),
        "model_tier": model_tier(model),
        "benchmark_profile": str(row.get("benchmark_profile") or ""),
        "passed": bool(row.get("passed")),
        "acceptance_oracle_passed": row.get("acceptance_oracle_passed"),
        "project_tests_passed": row.get("project_tests_passed"),
        "input_tokens": int(row.get("input_tokens") or 0),
        "output_tokens": int(row.get("output_tokens") or 0),
        "cached_input_tokens": int(row.get("cached_input_tokens") or 0),
        "cache_write_tokens": int(row.get("cache_write_tokens") or 0),
        "tokens": int(row.get("tokens") or 0),
        "cost_usd": float(row.get("cost_usd") or 0.0),
        "rework_turns": int(row.get("rework_turns") or 0),
        "governance_turns": int(row.get("governance_turns") or 0),
        "llm_turns": int(row.get("llm_turns") or 0),
        "wall_clock_s": float(row.get("wall_clock_s") or 0.0),
        "stop_reason": str(row.get("stop_reason") or ""),
        "expected_file_count": len(row.get("expected_files_changed") or []),
        "written_file_count": len(row.get("files_written") or []),
        "milestones_completed": int(row.get("milestones_completed") or 0),
        "milestones_total": int(row.get("milestones_total") or 0),
        "tokens_per_completed_milestone": row.get("tokens_per_completed_milestone"),
        "language_count": len(row.get("languages") or []),
        "tool_schema_hashes": ";".join(hashes),
    }


def export_evidence(
    inputs: list[Path],
    output_dir: Path,
    *,
    workflow_id: str,
    commit_sha: str,
) -> tuple[Path, Path]:
    """Write deterministic cell measurements and a provenance manifest."""
    if not workflow_id.strip() or not commit_sha.strip():
        raise ValueError("workflow_id and commit_sha are required")

    source_artifacts: list[dict[str, Any]] = []
    cells: list[dict[str, Any]] = []
    protocols: set[tuple[str, str]] = set()
    for path in sorted((item.resolve() for item in inputs), key=lambda item: item.name):
        raw = path.read_bytes()
        rows = _load_rows(path)
        protocols.update(
            (
                str(row.get("protocol_id") or ""),
                str(row.get("protocol_sha256") or ""),
            )
            for row in rows
            if row.get("protocol_id") or row.get("protocol_sha256")
        )
        source_artifacts.append(
            {
                "name": path.name,
                "sha256": _digest_bytes(raw),
                "rows": len(rows),
            }
        )
        cells.extend(_cell(row, workflow_id=workflow_id, commit_sha=commit_sha) for row in rows)

    cells.sort(
        key=lambda row: (
            row["model"],
            row["task"],
            row["condition"],
            row["rep"],
        )
    )
    identities = [(row["model"], row["task"], row["condition"], row["rep"]) for row in cells]
    if len(identities) != len(set(identities)):
        raise ValueError("duplicate model/task/condition/repetition cell")
    if not cells:
        raise ValueError("no benchmark cells supplied")

    output_dir.mkdir(parents=True, exist_ok=True)
    cells_path = output_dir / "cells.csv"
    with cells_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CELL_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(cells)

    canonical_cells = json.dumps(
        cells,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    manifest = {
        "schema": SCHEMA_VERSION,
        "workflow_id": workflow_id,
        "commit_sha": commit_sha,
        "row_count": len(cells),
        "cell_fields": list(CELL_FIELDS),
        "excluded_fields": list(EXCLUDED_FIELDS),
        "source_artifacts": source_artifacts,
        "protocols": [
            {"protocol_id": protocol_id, "protocol_sha256": digest}
            for protocol_id, digest in sorted(protocols)
        ],
        "cells_canonical_sha256": _digest_bytes(canonical_cells),
        "cells_csv_sha256": _digest_bytes(cells_path.read_bytes()),
    }
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return cells_path, manifest_path


def verify_evidence(manifest_path: Path, *, source_dir: Path | None = None) -> dict[str, Any]:
    """Verify one compact bundle and optional downloaded raw artifacts."""
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    schema = str(manifest.get("schema") or "")
    expected_fields = SCHEMA_FIELDS.get(schema)
    if expected_fields is None:
        raise ValueError("unsupported evidence manifest schema")
    cells_path = manifest_path.parent / "cells.csv"
    if not cells_path.is_file():
        raise ValueError("evidence bundle is missing cells.csv")
    if _digest_bytes(cells_path.read_bytes()) != manifest.get("cells_csv_sha256"):
        raise ValueError("cells.csv SHA-256 mismatch")
    with cells_path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != expected_fields:
            raise ValueError("cells.csv field schema mismatch")
        row_count = sum(1 for _row in reader)
    if row_count != int(manifest.get("row_count") or 0):
        raise ValueError("cells.csv row count mismatch")

    verified_sources = 0
    if source_dir is not None:
        if not source_dir.is_dir():
            raise ValueError(f"raw source directory does not exist: {source_dir}")
        for artifact in manifest.get("source_artifacts") or []:
            name = str(artifact.get("name") or "")
            if not name or Path(name).name != name:
                raise ValueError(f"invalid raw source artifact name: {name!r}")
            matches = sorted(path for path in source_dir.rglob(name) if path.is_file())
            if not matches:
                raise ValueError(f"missing raw source artifact: {name}")
            if len(matches) > 1:
                raise ValueError(
                    f"ambiguous raw source artifact {name}: found {len(matches)} matches"
                )
            path = matches[0]
            if _digest_bytes(path.read_bytes()) != artifact.get("sha256"):
                raise ValueError(f"raw source SHA-256 mismatch: {path.name}")
            verified_sources += 1
    return {
        "schema": schema,
        "rows": row_count,
        "cells_csv_sha256": manifest["cells_csv_sha256"],
        "verified_sources": verified_sources,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--input", type=Path, nargs="+")
    mode.add_argument("--verify-manifest", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--workflow-id")
    parser.add_argument("--commit-sha")
    parser.add_argument("--source-dir", type=Path)
    args = parser.parse_args()
    if args.verify_manifest is not None:
        verified = verify_evidence(
            args.verify_manifest,
            source_dir=args.source_dir,
        )
        print(json.dumps(verified, indent=2, sort_keys=True))
        return 0
    if args.output_dir is None or not args.workflow_id or not args.commit_sha:
        parser.error("--input requires --output-dir, --workflow-id, and --commit-sha")
    cells_path, manifest_path = export_evidence(
        args.input,
        args.output_dir,
        workflow_id=args.workflow_id,
        commit_sha=args.commit_sha,
    )
    print(f"Wrote {cells_path}")
    print(f"Wrote {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
