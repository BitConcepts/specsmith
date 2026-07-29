"""Visible deterministic checks for the T29 shared release contract."""

from __future__ import annotations

import json
from pathlib import Path


def _allows_null(schema: dict) -> bool:
    value_type = schema.get("type")
    return value_type == "null" or (isinstance(value_type, list) and "null" in value_type)


def _fail(message: str) -> int:
    print(message)
    return 1


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    schema = json.loads((root / "contracts" / "release.schema.json").read_text(encoding="utf-8"))
    fields = {
        "id",
        "service",
        "version",
        "environment",
        "state",
        "created_at",
        "approved_at",
    }
    if set(schema.get("properties", {})) != fields:
        return _fail("Release schema must declare exactly the seven shared fields")
    if set(schema.get("required", [])) != fields:
        return _fail("Every shared release field must be required")
    if schema.get("additionalProperties") is not False:
        return _fail("Release schema must reject additional properties")
    if set(schema["properties"]["environment"].get("enum", [])) != {
        "staging",
        "production",
    }:
        return _fail("Environment enum must be staging or production")
    if set(schema["properties"]["state"].get("enum", [])) != {
        "draft",
        "approved",
        "paused",
    }:
        return _fail("State enum must be draft, approved, or paused")
    if not _allows_null(schema["properties"]["approved_at"]):
        return _fail("approved_at must allow null")

    backend = (root / "backend" / "main.py").read_text(encoding="utf-8")
    worker = (root / "worker" / "main.go").read_text(encoding="utf-8")
    client = (root / "ui" / "src" / "api.ts").read_text(encoding="utf-8")
    for field in fields:
        if field not in backend:
            return _fail(f"Python API is missing shared field {field}")
        if f'json:"{field}"' not in worker:
            return _fail(f"Go worker is missing shared JSON field {field}")
        if field not in client:
            return _fail(f"TypeScript client is missing shared field {field}")

    print("Shared release contract checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
