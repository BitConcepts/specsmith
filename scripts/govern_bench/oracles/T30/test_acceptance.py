from __future__ import annotations

import hashlib
from datetime import datetime
from pathlib import Path

import pytest
from itsdangerous import (
    BadSignature,
    Serializer,
    SignatureExpired,
    TimedSerializer,
    URLSafeSerializer,
    URLSafeTimedSerializer,
)

ROOT = Path(__file__).resolve().parents[1]


def test_current_old_and_fallback_signers_are_attributed() -> None:
    serializer = Serializer(
        ["old-secret", "new-secret"],
        fallback_signers=[{"digest_method": hashlib.sha512}],
    )

    current_value = serializer.dumps({"id": 1})
    old_value = Serializer("old-secret").dumps({"id": 2})
    fallback_value = Serializer(
        "new-secret", signer_kwargs={"digest_method": hashlib.sha512}
    ).dumps({"id": 3})

    assert serializer.loads_with_reissue(current_value) == ({"id": 1}, False)
    assert serializer.loads_with_reissue(old_value) == ({"id": 2}, True)
    assert serializer.loads_with_reissue(fallback_value) == ({"id": 3}, True)


def test_bad_signature_is_not_converted_to_a_rotation_result() -> None:
    serializer = Serializer(["old-secret", "new-secret"])

    with pytest.raises(BadSignature):
        serializer.loads_with_reissue("not-a-signed-value")


def test_timed_return_shapes_and_expiry(monkeypatch: pytest.MonkeyPatch) -> None:
    now = 1_700_000_000
    monkeypatch.setattr("time.time", lambda: now)
    current = TimedSerializer(["old-secret", "new-secret"])
    old = TimedSerializer("old-secret").dumps({"timed": True})
    new = current.dumps({"timed": True})

    assert current.loads_with_reissue(new) == ({"timed": True}, False)
    assert current.loads_with_reissue(old) == ({"timed": True}, True)

    payload, timestamp, needs_reissue = current.loads_with_reissue(old, return_timestamp=True)
    assert payload == {"timed": True}
    assert isinstance(timestamp, datetime)
    assert needs_reissue is True

    monkeypatch.setattr("time.time", lambda: now + 10)
    with pytest.raises(SignatureExpired):
        current.loads_with_reissue(old, max_age=5)


def test_url_safe_subclasses_inherit_rotation_diagnostics() -> None:
    plain = URLSafeSerializer(["old-secret", "new-secret"])
    timed = URLSafeTimedSerializer(["old-secret", "new-secret"])

    assert plain.loads_with_reissue(plain.dumps({"url": "safe"})) == (
        {"url": "safe"},
        False,
    )
    assert timed.loads_with_reissue(timed.dumps({"url": "timed"})) == (
        {"url": "timed"},
        False,
    )


def test_pinned_provenance_and_license_are_preserved() -> None:
    provenance = (ROOT / "UPSTREAM.md").read_text(encoding="utf-8")
    license_digest = hashlib.sha256((ROOT / "LICENSE.txt").read_bytes()).hexdigest()

    assert "672971d66a2ef9f85151e53283113f33d642dabd" in provenance
    assert license_digest == "63af09891b6be8ad1a4252ed43af0f4efba7fc948e228367bed7f3c5ae0b09d7"


def test_documentation_explains_reissue_contract() -> None:
    docs = (ROOT / "docs" / "serializer.rst").read_text(encoding="utf-8").casefold()

    assert "loads_with_reissue" in docs
    assert "newest" in docs and "older" in docs
    assert "return_timestamp" in docs
