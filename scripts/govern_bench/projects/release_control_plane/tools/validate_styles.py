"""Visible CSS checks for the T29 release operator journey."""

from __future__ import annotations

from pathlib import Path


def _fail(message: str) -> int:
    print(message)
    return 1


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    styles = (root / "ui" / "src" / "styles.css").read_text(encoding="utf-8").casefold()

    if ":focus-visible" not in styles:
        return _fail("Release UI CSS must provide a visible :focus-visible state")
    if ":disabled" not in styles and "[disabled]" not in styles:
        return _fail("Release UI CSS must distinguish disabled approval actions")
    if "@media" not in styles:
        return _fail("Release UI CSS must provide a responsive small-screen layout")

    print("Release UI CSS checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
