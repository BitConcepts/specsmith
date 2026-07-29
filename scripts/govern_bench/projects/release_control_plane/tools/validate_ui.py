"""Visible structural checks for the T29 release operator journey."""

from __future__ import annotations

from pathlib import Path


def _fail(message: str) -> int:
    print(message)
    return 1


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    app = (root / "ui" / "src" / "App.tsx").read_text(encoding="utf-8").casefold()
    api = (root / "ui" / "src" / "api.ts").read_text(encoding="utf-8").casefold()
    browser = (
        (root / "ui" / "tests" / "release-control.spec.ts").read_text(encoding="utf-8").casefold()
    )

    for term in ("loading", "error", "empty", "environment", "state", "approve"):
        if term not in app:
            return _fail(f"React operator flow is missing {term}")
    if "usestate" not in app or "useeffect" not in app:
        return _fail("React operator flow must load state with hooks")
    if "<label" not in app and "aria-label" not in app:
        return _fail("Release filters must have accessible labels")
    if 'role="alert"' not in app and 'role="status"' not in app:
        return _fail("Loading or error feedback must expose an accessible role")

    for term in (
        "/api/releases",
        "urlsearchparams",
        'set("environment"',
        'set("state"',
        "encodeuricomponent",
        'method: "patch"',
    ):
        if term not in api:
            return _fail(f"TypeScript release client is missing {term}")

    for term in ("page.route", "selectoption", "approve", "toBeVisible".casefold()):
        if term.casefold() not in browser:
            return _fail(f"Playwright release journey is missing {term}")
    if "test.skip" in browser:
        return _fail("Playwright release journey must not remain skipped")

    print("Release UI journey checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
