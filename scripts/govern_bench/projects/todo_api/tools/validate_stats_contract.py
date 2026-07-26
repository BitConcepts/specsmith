"""Public T10 contract validator owned by GovernanceBench."""

from __future__ import annotations

from fastapi.testclient import TestClient

import app.main as main


def _reset() -> None:
    main._TODO_STORE.clear()
    main._NEXT_ID = 1


def main_check() -> None:
    client = TestClient(main.app)
    _reset()

    empty = client.get("/todos/stats")
    assert empty.status_code == 200, (
        f"GET /todos/stats must return HTTP 200, got {empty.status_code}: {empty.text}"
    )
    assert empty.json() == {
        "total": 0,
        "completed": 0,
        "pending": 0,
        "by_priority": {"1": 0, "2": 0, "3": 0},
    }

    created = [
        client.post("/todos", json={"title": "low", "priority": 1}).json(),
        client.post("/todos", json={"title": "high-a", "priority": 3}).json(),
        client.post("/todos", json={"title": "high-b", "priority": 3}).json(),
    ]
    patched = client.patch(f"/todos/{created[1]['id']}", json={"completed": True})
    assert patched.status_code == 200, patched.text

    stats = client.get("/todos/stats")
    assert stats.status_code == 200, (
        f"GET /todos/stats must return HTTP 200, got {stats.status_code}: {stats.text}"
    )
    assert stats.json() == {
        "total": 3,
        "completed": 1,
        "pending": 2,
        "by_priority": {"1": 1, "2": 0, "3": 2},
    }
    _reset()


if __name__ == "__main__":
    main_check()
