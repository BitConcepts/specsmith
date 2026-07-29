"""Visible deterministic checks for the T28 incident API journey."""

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
            "/api/incidents",
            json={"title": "API down", "service": "api", "severity": "critical"},
        )
        if created_response.status_code != 201:
            return _fail("POST /api/incidents must return HTTP 201")
        created: Any = created_response.json()
        required = {
            "id",
            "title",
            "service",
            "severity",
            "status",
            "created_at",
            "acknowledged_at",
        }
        if not isinstance(created, dict) or required - set(created):
            return _fail("Created incident must contain every shared-contract field")

        second_response = client.post(
            "/api/incidents",
            json={"title": "Slow jobs", "service": "worker", "severity": "low"},
        )
        if second_response.status_code != 201:
            return _fail("POST /api/incidents must create the second filter-control incident")
        second: Any = second_response.json()
        listed = client.get("/api/incidents").json()
        if not isinstance(listed, list) or len(listed) != 2:
            return _fail("GET /api/incidents must return a JSON list of incidents")
        filtered = client.get("/api/incidents?severity=critical&status=open").json()
        if not isinstance(filtered, list) or [item.get("id") for item in filtered] != [
            created["id"]
        ]:
            return _fail("GET filters must compose severity and status and still return a list")

        acknowledged = client.patch(f"/api/incidents/{created['id']}/ack")
        if acknowledged.status_code != 200:
            return _fail("PATCH acknowledge must return HTTP 200 for a known incident")
        acknowledged_payload = acknowledged.json()
        if not isinstance(acknowledged_payload, dict):
            return _fail("PATCH acknowledge must return the updated incident object")
        if (
            acknowledged_payload.get("status") != "acknowledged"
            or acknowledged_payload.get("acknowledged_at") is None
        ):
            return _fail(
                "PATCH acknowledge must return the incident with status=acknowledged "
                "and a non-null acknowledged_at"
            )
        still_open = client.get("/api/incidents?status=open")
        if still_open.status_code != 200 or [item.get("id") for item in still_open.json()] != [
            second["id"]
        ]:
            return _fail("GET /api/incidents?status=open must exclude acknowledged incidents")
        if client.patch("/api/incidents/unknown/ack").status_code != 404:
            return _fail("PATCH acknowledge must return 404 for an unknown incident")
        invalid = client.post(
            "/api/incidents",
            json={"title": "Bad", "service": "api", "severity": "urgent"},
        )
        if invalid.status_code != 422:
            return _fail("POST /api/incidents must reject invalid severity")
    except Exception as exc:  # noqa: BLE001 - validator must fail with actionable evidence
        return _fail(f"Incident API validation raised {type(exc).__name__}: {exc}")

    print("Incident API journey checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
