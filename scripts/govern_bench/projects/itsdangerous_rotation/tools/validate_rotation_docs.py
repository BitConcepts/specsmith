"""Public documentation and provenance validator for the T30 task."""

from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PINNED_COMMIT = "672971d66a2ef9f85151e53283113f33d642dabd"
PINNED_LICENSE_SHA256 = (
    "63af09891b6be8ad1a4252ed43af0f4efba7fc948e228367bed7f3c5ae0b09d7"
)


def main() -> int:
    provenance = (ROOT / "UPSTREAM.md").read_text(encoding="utf-8")
    license_digest = hashlib.sha256((ROOT / "LICENSE.txt").read_bytes()).hexdigest()
    docs = (ROOT / "docs" / "serializer.rst").read_text(encoding="utf-8").casefold()

    assert PINNED_COMMIT in provenance
    assert license_digest == PINNED_LICENSE_SHA256
    assert "loads_with_reissue" in docs
    assert "newest" in docs and "older" in docs
    assert "return_timestamp" in docs
    assert "reissue" in docs
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
