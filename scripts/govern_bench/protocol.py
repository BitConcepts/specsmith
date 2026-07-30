"""Frozen GovernanceBench preregistration identity and contract validation."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

import yaml

DEFAULT_PROTOCOL_PATH = Path(__file__).with_name("PREPRINT_PROTOCOL_2026_07.yml")
RECOVERY_PROTOCOL_PATH = Path(__file__).with_name("PREPRINT_PROTOCOL_2026_07_V2.yml")
PROTOCOL_PATH_BY_PROFILE = {
    "publication-real-repository-recovery": RECOVERY_PROTOCOL_PATH,
}


def load_protocol(path: Path = DEFAULT_PROTOCOL_PATH) -> dict[str, Any]:
    """Load and minimally validate the frozen publication protocol."""
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: protocol must be a YAML mapping")
    if payload.get("schema") != "governancebench-preregistration-v1":
        raise ValueError(f"{path}: unsupported protocol schema")
    if payload.get("status") != "frozen":
        raise ValueError(f"{path}: publication protocol must be frozen")
    if not str(payload.get("protocol_id") or "").strip():
        raise ValueError(f"{path}: protocol_id is required")
    return payload


def protocol_sha256(path: Path = DEFAULT_PROTOCOL_PATH) -> str:
    """Return the byte-exact SHA-256 identity of the preregistration."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_run_contract(
    *,
    profile: str,
    tasks: list[str],
    conditions: list[str],
    repetitions: int,
    provider: str,
    model: str,
    controller: str,
    path: Path | None = None,
) -> tuple[str, str]:
    """Fail closed unless a publication run matches its frozen contract."""
    path = path or PROTOCOL_PATH_BY_PROFILE.get(profile, DEFAULT_PROTOCOL_PATH)
    payload = load_protocol(path)
    contract = (payload.get("contracts") or {}).get(profile)
    if not isinstance(contract, dict):
        raise ValueError(f"{profile!r} is not registered in {path.name}")
    expected = {
        "tasks": list(contract.get("tasks") or []),
        "conditions": list(contract.get("conditions") or []),
        "repetitions": int(contract.get("repetitions") or 0),
    }
    actual = {
        "tasks": list(tasks),
        "conditions": list(conditions),
        "repetitions": repetitions,
    }
    if actual != expected:
        raise ValueError(
            f"{profile} does not match frozen protocol: expected {expected}, got {actual}"
        )
    routes = {
        (str(route.get("provider") or ""), str(route.get("model") or ""))
        for route in (contract.get("routes") or [])
        if isinstance(route, dict)
    }
    if (provider, model) not in routes:
        raise ValueError(
            f"{provider}/{model} is not a frozen route for {profile}; allowed={sorted(routes)}"
        )
    expected_controller = str((payload.get("controls") or {}).get("controller") or "")
    if controller != expected_controller:
        raise ValueError(
            f"{controller!r} is not the frozen controller for {profile}; "
            f"expected {expected_controller!r}"
        )
    return str(payload["protocol_id"]), protocol_sha256(path)
