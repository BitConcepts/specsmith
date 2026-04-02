# SPDX-License-Identifier: MIT
# Copyright (c) 2026 BitConcepts, LLC. All rights reserved.
"""Upgrader — update governance files to match a newer spec version."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import yaml
from jinja2 import Environment, PackageLoader, select_autoescape

from specsmith import __version__
from specsmith.config import ProjectConfig


@dataclass
class UpgradeResult:
    """Result of an upgrade operation."""

    updated_files: list[str] = field(default_factory=list)
    skipped_files: list[str] = field(default_factory=list)
    message: str = ""


# Governance templates that get regenerated on upgrade
_GOVERNANCE_TEMPLATES: list[tuple[str, str]] = [
    ("governance/rules.md.j2", "docs/governance/RULES.md"),
    ("governance/workflow.md.j2", "docs/governance/WORKFLOW.md"),
    ("governance/roles.md.j2", "docs/governance/ROLES.md"),
    ("governance/context-budget.md.j2", "docs/governance/CONTEXT-BUDGET.md"),
    ("governance/verification.md.j2", "docs/governance/VERIFICATION.md"),
    ("governance/drift-metrics.md.j2", "docs/governance/DRIFT-METRICS.md"),
]

# Migration: old lowercase filenames → new uppercase filenames
_LEGACY_RENAMES: list[tuple[str, str]] = [
    ("docs/governance/rules.md", "docs/governance/RULES.md"),
    ("docs/governance/workflow.md", "docs/governance/WORKFLOW.md"),
    ("docs/governance/roles.md", "docs/governance/ROLES.md"),
    ("docs/governance/context-budget.md", "docs/governance/CONTEXT-BUDGET.md"),
    ("docs/governance/verification.md", "docs/governance/VERIFICATION.md"),
    ("docs/governance/drift-metrics.md", "docs/governance/DRIFT-METRICS.md"),
    ("docs/architecture.md", "docs/ARCHITECTURE.md"),
    ("docs/workflow.md", "docs/WORKFLOW.md"),
]


def run_upgrade(
    root: Path,
    *,
    target_version: str | None = None,
) -> UpgradeResult:
    """Upgrade governance files to a newer spec version.

    Args:
        root: Project root directory.
        target_version: Target spec version. If None, uses the current specsmith version.

    Returns:
        UpgradeResult with details of the operation.
    """
    scaffold_path = root / "scaffold.yml"

    if not scaffold_path.exists():
        return UpgradeResult(
            message="No scaffold.yml found. Cannot determine project configuration for upgrade."
        )

    with open(scaffold_path) as f:
        raw = yaml.safe_load(f)

    try:
        config = ProjectConfig(**raw)
    except Exception as e:
        return UpgradeResult(message=f"Invalid scaffold.yml: {e}")

    new_version = target_version or __version__
    old_version = config.spec_version

    if old_version == new_version:
        return UpgradeResult(message=f"Already at spec version {new_version}. Nothing to upgrade.")

    # Update config
    config.spec_version = new_version

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

    result = UpgradeResult()

    # Migrate legacy lowercase filenames to uppercase
    _migrate_legacy_filenames(root, result)

    for template_name, output_rel in _GOVERNANCE_TEMPLATES:
        output_path = root / output_rel

        if not output_path.exists():
            result.skipped_files.append(output_rel)
            continue

        tmpl = env.get_template(template_name)
        content = tmpl.render(**ctx)
        output_path.write_text(content, encoding="utf-8")
        result.updated_files.append(output_rel)

    # Update scaffold.yml with new version
    raw["spec_version"] = new_version
    with open(scaffold_path, "w") as f:
        yaml.dump(raw, f, default_flow_style=False, sort_keys=False)
    result.updated_files.append("scaffold.yml")

    # Initialize credit tracking if not present
    specsmith_dir = root / ".specsmith"
    if not specsmith_dir.exists():
        from specsmith.credits import CreditBudget, save_budget

        save_budget(root, CreditBudget())
        result.updated_files.append(".specsmith/credit-budget.json")

    result.message = (
        f"Upgraded from {old_version} to {new_version}. "
        f"{len(result.updated_files)} files updated, {len(result.skipped_files)} skipped."
    )

    return result


def _migrate_legacy_filenames(root: Path, result: UpgradeResult) -> None:
    """Rename legacy lowercase governance files to uppercase.

    Handles both case-sensitive (Linux) and case-insensitive (Windows/macOS)
    filesystems. On case-insensitive FS, uses a two-step rename via a
    temporary name to avoid conflicts.
    """
    import shutil

    for old_rel, new_rel in _LEGACY_RENAMES:
        old_path = root / old_rel
        new_path = root / new_rel
        if not old_path.exists():
            continue
        if old_path == new_path:
            continue  # Already correct
        # Case-insensitive FS: old and new resolve to the same inode.
        # Use a temp name to force the rename.
        if new_path.exists() and old_path.samefile(new_path):
            tmp_path = old_path.with_suffix(".md.migrating")
            shutil.move(str(old_path), str(tmp_path))
            shutil.move(str(tmp_path), str(new_path))
        elif not new_path.exists():
            new_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(old_path), str(new_path))
        else:
            continue  # Both exist as truly separate files — skip
        result.updated_files.append(f"{old_rel} → {new_rel}")
