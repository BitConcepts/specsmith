"""Public T13 contract validator owned by GovernanceBench."""

from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory

from cli.main import cli
from click.testing import CliRunner


def _invoke(payload: object, *args: str) -> tuple[int, object]:
    with TemporaryDirectory() as directory:
        source = Path(directory) / "input.json"
        source.write_text(json.dumps(payload), encoding="utf-8")
        result = CliRunner().invoke(cli, ["process", str(source), *args])
    assert result.exception is None, result.output
    return result.exit_code, json.loads(result.output)


def main_check() -> None:
    payload = [
        {"name": "one", "priority": 1, "active": True},
        {"name": "two", "priority": 1, "active": False},
        {"name": "three", "priority": 3, "active": True},
    ]
    code, filtered = _invoke(
        payload,
        "--filter",
        "priority=1",
        "--filter",
        "active=true",
    )
    assert code == 0
    assert filtered == [payload[0]]

    code, empty = _invoke(payload, "--filter", "priority=2")
    assert code == 0
    assert empty == []

    object_payload = {"name": "unchanged", "priority": 1}
    code, unchanged = _invoke(object_payload, "--filter", "priority=3")
    assert code == 0
    assert unchanged == object_payload


if __name__ == "__main__":
    main_check()
