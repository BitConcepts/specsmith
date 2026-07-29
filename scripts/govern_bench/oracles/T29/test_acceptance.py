from __future__ import annotations

import importlib
import json
import shutil
import subprocess
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parent.parent


def _allows_null(schema: dict) -> bool:
    value_type = schema.get("type")
    if value_type == "null" or (isinstance(value_type, list) and "null" in value_type):
        return True
    if schema.get("const", object()) is None or None in schema.get("enum", []):
        return True
    return any(
        _allows_null(option)
        for keyword in ("anyOf", "oneOf")
        for option in schema.get(keyword, [])
        if isinstance(option, dict)
    )


def test_release_schema_is_complete_and_strict() -> None:
    schema = json.loads((ROOT / "contracts" / "release.schema.json").read_text(encoding="utf-8"))
    fields = {
        "id",
        "service",
        "version",
        "environment",
        "state",
        "created_at",
        "approved_at",
    }
    assert set(schema["properties"]) == fields
    assert set(schema["required"]) == fields
    assert schema.get("additionalProperties") is False
    assert set(schema["properties"]["environment"]["enum"]) == {
        "staging",
        "production",
    }
    assert set(schema["properties"]["state"]["enum"]) == {
        "draft",
        "approved",
        "paused",
    }
    assert _allows_null(schema["properties"]["approved_at"])


def test_python_release_create_filter_and_approval_flow() -> None:
    import backend.main as backend

    backend = importlib.reload(backend)
    client = TestClient(backend.app)
    production = client.post(
        "/api/releases",
        json={"service": "billing", "version": "4.2.0", "environment": "production"},
    )
    assert production.status_code == 201, production.text
    created = production.json()
    assert created["state"] == "draft"
    assert created["service"] == "billing"
    assert created["environment"] == "production"
    assert created["approved_at"] is None
    assert created["id"] and created["created_at"]

    staging = client.post(
        "/api/releases",
        json={"service": "worker", "version": "1.9.0", "environment": "staging"},
    )
    assert staging.status_code == 201
    filtered = client.get("/api/releases?environment=production&state=draft")
    assert filtered.status_code == 200
    assert [item["id"] for item in filtered.json()] == [created["id"]]

    approved = client.patch(f"/api/releases/{created['id']}/approve")
    assert approved.status_code == 200
    assert approved.json()["state"] == "approved"
    assert approved.json()["approved_at"]
    assert client.get("/api/releases?state=draft").json()[0]["service"] == "worker"
    assert client.patch("/api/releases/not-found/approve").status_code == 404
    assert (
        client.post(
            "/api/releases",
            json={"service": "bad", "version": "0", "environment": "desktop"},
        ).status_code
        == 422
    )


def test_go_plan_normalizer_matches_contract_and_rejects_bad_plans() -> None:
    worker = ROOT / "worker"
    source = (worker / "main.go").read_text(encoding="utf-8")
    for json_name in (
        "id",
        "service",
        "version",
        "environment",
        "state",
        "created_at",
        "approved_at",
    ):
        assert f'json:"{json_name}"' in source
    assert "func NormalizePlan(raw []byte) (Release, error)" in source

    go = shutil.which("go")
    if go is None:
        return
    oracle_test = worker / "t29_oracle_test.go"
    oracle_test.write_text(
        """package main

import "testing"

func TestT29NormalizePlan(t *testing.T) {
    raw := []byte(`{"service":"edge","version":"3.1.4","environment":"production"}`)
    got, err := NormalizePlan(raw)
    if err != nil { t.Fatalf("valid plan rejected: %v", err) }
    if got.Service != "edge" || got.Version != "3.1.4" || got.Environment != "production" {
        t.Fatalf("wrong mapping: %#v", got)
    }
    if got.State != "draft" || got.ID == "" || got.CreatedAt == "" || got.ApprovedAt != nil {
        t.Fatalf("missing defaults: %#v", got)
    }
    badEnvironment := []byte(`{"service":"edge","version":"3.1.4","environment":"local"}`)
    if _, err := NormalizePlan(badEnvironment); err == nil {
        t.Fatal("invalid environment accepted")
    }
    missingVersion := []byte(`{"service":"edge","environment":"staging"}`)
    if _, err := NormalizePlan(missingVersion); err == nil {
        t.Fatal("missing version accepted")
    }
}
""",
        encoding="utf-8",
    )
    try:
        result = subprocess.run(
            [go, "test", "./..."],
            cwd=worker,
            capture_output=True,
            text=True,
            timeout=45,
            check=False,
        )
        assert result.returncode == 0, result.stdout + result.stderr
    finally:
        oracle_test.unlink(missing_ok=True)


def test_release_ui_has_accessible_flow_and_playwright_journey() -> None:
    app = (ROOT / "ui" / "src" / "App.tsx").read_text(encoding="utf-8").casefold()
    api = (ROOT / "ui" / "src" / "api.ts").read_text(encoding="utf-8").casefold()
    browser = (
        (ROOT / "ui" / "tests" / "release-control.spec.ts").read_text(encoding="utf-8").casefold()
    )

    for term in ("loading", "error", "environment", "state", "approve"):
        assert term in app
    assert "empty" in app or (
        "releases.length" in app
        and "=== 0" in app
        and ("no release" in app or "no matching release" in app)
    )
    assert "usestate" in app and "useeffect" in app
    assert "<label" in app or "aria-label" in app
    assert 'role="alert"' in app or 'role="status"' in app
    assert "/api/releases" in api
    assert 'set("environment"' in api and 'set("state"' in api
    assert "encodeuricomponent" in api
    assert "page.route" in browser and "selectoption" in browser
    assert "approve" in browser and "test.skip" not in browser


def test_release_architecture_records_cross_boundary_decisions() -> None:
    architecture = (ROOT / "docs" / "architecture.md").read_text(encoding="utf-8").casefold()
    concepts = (
        ("python", "fastapi"),
        ("go", "golang"),
        ("react",),
        ("schema", "contract"),
        ("flow",),
        ("memory", "in-memory"),
        ("failure", "error"),
    )
    assert len(architecture.split()) >= 100
    assert all(any(term in architecture for term in alternatives) for alternatives in concepts)
