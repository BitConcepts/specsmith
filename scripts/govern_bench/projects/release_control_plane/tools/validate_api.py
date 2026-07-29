"""Visible deterministic checks for the T29 release API journey."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient


def _fail(message: str) -> int:
    print(message)
    return 1


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(root))
    try:
        module = importlib.import_module("backend.main")
        module = importlib.reload(module)
        client = TestClient(module.app)

        health = client.get("/health")
        if health.status_code != 200 or health.json() != {"status": "ok"}:
            return _fail("GET /health must preserve the stable 200 response")

        created_response = client.post(
            "/api/releases",
            json={"service": "checkout", "version": "2.4.0", "environment": "production"},
        )
        if created_response.status_code != 201:
            return _fail("POST /api/releases must return HTTP 201")
        created: Any = created_response.json()
        required = {
            "id",
            "service",
            "version",
            "environment",
            "state",
            "created_at",
            "approved_at",
        }
        if not isinstance(created, dict) or required - set(created):
            return _fail("Created release must contain every shared-contract field")

        second_response = client.post(
            "/api/releases",
            json={"service": "worker", "version": "1.8.1", "environment": "staging"},
        )
        if second_response.status_code != 201:
            return _fail("POST /api/releases must create the second filter-control release")
        second: Any = second_response.json()

        listed = client.get("/api/releases").json()
        if not isinstance(listed, list) or len(listed) != 2:
            return _fail("GET /api/releases must return a JSON list of releases")
        filtered = client.get("/api/releases?environment=production&state=draft").json()
        if not isinstance(filtered, list) or [item.get("id") for item in filtered] != [
            created["id"]
        ]:
            return _fail("GET filters must compose environment and state and still return a list")

        approved = client.patch(f"/api/releases/{created['id']}/approve")
        if approved.status_code != 200:
            return _fail("PATCH approve must return HTTP 200 for a known release")
        approved_payload = approved.json()
        if not isinstance(approved_payload, dict):
            return _fail("PATCH approve must return the updated release object")
        if (
            approved_payload.get("state") != "approved"
            or approved_payload.get("approved_at") is None
        ):
            return _fail(
                "PATCH approve must return the release with state=approved "
                "and a non-null approved_at"
            )

        still_draft = client.get("/api/releases?state=draft")
        if still_draft.status_code != 200 or [item.get("id") for item in still_draft.json()] != [
            second["id"]
        ]:
            return _fail("GET /api/releases?state=draft must exclude approved releases")
        if client.patch("/api/releases/unknown/approve").status_code != 404:
            return _fail("PATCH approve must return 404 for an unknown release")
        invalid = client.post(
            "/api/releases",
            json={"service": "bad", "version": "0", "environment": "local"},
        )
        if invalid.status_code != 422:
            return _fail("POST /api/releases must reject invalid environment")
    except Exception as exc:  # noqa: BLE001
        return _fail(f"Release API validation raised {type(exc).__name__}: {exc}")

    print("Release API journey checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
