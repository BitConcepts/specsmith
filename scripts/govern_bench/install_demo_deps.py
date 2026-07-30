"""install_demo_deps.py — install demo-project dependencies for the grader.

The benchmark's coding tasks run pytest inside copies of the demo projects under
scripts/govern_bench/projects/*/. Those projects declare their own runtime and
test dependencies (e.g. fastapi, httpx). CI installs only specsmith + a provider
SDK, so without this step pytest import-fails on every coding task and the grader
silently records tests_passed=False — making governed and ungoverned runs look
identically broken. This installs each demo project's runtime + optional
("test", etc.) dependency groups, without installing the demo itself as a package.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - exercised by the Python 3.10 CI jobs
    import tomli as tomllib

_PROJECTS = Path(__file__).with_name("projects")


def collect_requirements(projects_dir: Path) -> list[str]:
    """Return de-duplicated runtime and test deps across all benchmark projects."""
    reqs: list[str] = []
    for pyproject in sorted(projects_dir.glob("*/pyproject.toml")):
        data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
        project = data.get("project", {})
        reqs.extend(project.get("dependencies", []) or [])
        for deps in (project.get("optional-dependencies") or {}).values():
            reqs.extend(deps or [])
        # PEP 735 dependency groups are used by pinned upstream repositories.
        # Only the test group belongs in the benchmark grader environment.
        reqs.extend((data.get("dependency-groups") or {}).get("tests", []) or [])
    return sorted(set(reqs))


def main() -> int:
    # os.path.realpath is the CodeQL-recognised path sanitizer.
    projects_dir = Path(os.path.realpath(str(_PROJECTS)))
    if not projects_dir.is_dir():
        print(f"No demo projects directory found: {projects_dir}", file=sys.stderr)
        return 1

    reqs = collect_requirements(projects_dir)
    if not reqs:
        print("No demo-project dependencies declared; nothing to install.")
        return 0

    print("Installing demo-project dependencies:")
    for req in reqs:
        print(f"  - {req}")
    subprocess.check_call([sys.executable, "-m", "pip", "install", *reqs])
    return 0


if __name__ == "__main__":
    sys.exit(main())
