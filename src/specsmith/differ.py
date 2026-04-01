# SPDX-License-Identifier: MIT
# Copyright (c) 2026 BitConcepts, LLC. All rights reserved.
"""Differ — compare governance files against spec templates."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import yaml
from jinja2 import Environment, PackageLoader, select_autoescape

from specsmith.config import ProjectConfig

_GOVERNANCE_FILES: list[tuple[str, str]] = [
    ("governance/rules.md.j2", "docs/governance/rules.md"),
    ("governance/workflow.md.j2", "docs/governance/workflow.md"),
    ("governance/roles.md.j2", "docs/governance/roles.md"),
    ("governance/context-budget.md.j2", "docs/governance/context-budget.md"),
    ("governance/verification.md.j2", "docs/governance/verification.md"),
    ("governance/drift-metrics.md.j2", "docs/governance/drift-metrics.md"),
]


def run_diff(root: Path) -> list[tuple[str, str]]:
    """Compare governance files against what templates would generate.

    Returns list of (relative_path, status) where status is 'match', 'differs', or 'missing'.
    """
    scaffold_path = root / "scaffold.yml"
    if not scaffold_path.exists():
        return [("scaffold.yml", "missing")]

    with open(scaffold_path) as f:
        raw = yaml.safe_load(f)

    try:
        config = ProjectConfig(**raw)
    except Exception:
        return [("scaffold.yml", "invalid")]

    env = Environment(
        loader=PackageLoader("specsmith", "templates"),
        autoescape=select_autoescape([]),
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )

    from specsmith.tools import get_tools

    ctx = {
        "project": config,
        "today": date.today().isoformat(),
        "package_name": config.package_name,
        "tools": get_tools(config),
    }

    results: list[tuple[str, str]] = []

    for template_name, output_rel in _GOVERNANCE_FILES:
        output_path = root / output_rel
        if not output_path.exists():
            results.append((output_rel, "missing"))
            continue

        tmpl = env.get_template(template_name)
        expected = tmpl.render(**ctx)
        actual = output_path.read_text(encoding="utf-8")

        if _normalize(actual) == _normalize(expected):
            results.append((output_rel, "match"))
        else:
            results.append((output_rel, "differs"))

    return results


def _normalize(text: str) -> str:
    """Normalize whitespace for comparison."""
    return "\n".join(line.rstrip() for line in text.strip().splitlines())
