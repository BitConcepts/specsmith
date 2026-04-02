# SPDX-License-Identifier: MIT
# Copyright (c) 2026 BitConcepts, LLC. All rights reserved.
"""Tests for specsmith validator."""

from __future__ import annotations

from pathlib import Path

from specsmith.validator import run_validate


class TestValidateScaffoldYml:
    def test_no_scaffold_yml(self, tmp_path: Path) -> None:
        report = run_validate(tmp_path)
        # Should pass (gracefully skip)
        assert report.valid

    def test_valid_scaffold_yml(self, tmp_path: Path) -> None:
        (tmp_path / "scaffold.yml").write_text("name: test\ntype: cli-python\n", encoding="utf-8")
        report = run_validate(tmp_path)
        results = [r for r in report.results if r.name == "scaffold-yml"]
        assert results[0].passed

    def test_invalid_scaffold_yml(self, tmp_path: Path) -> None:
        (tmp_path / "scaffold.yml").write_text("just a string\n", encoding="utf-8")
        report = run_validate(tmp_path)
        results = [r for r in report.results if r.name == "scaffold-yml"]
        assert not results[0].passed


class TestValidateAgentsRefs:
    def test_broken_ref(self, tmp_path: Path) -> None:
        (tmp_path / "AGENTS.md").write_text(
            "See [rules](docs/governance/RULES.md) for details.\n",
            encoding="utf-8",
        )
        report = run_validate(tmp_path)
        failed = [r for r in report.results if not r.passed]
        assert any("RULES.md" in r.message for r in failed)

    def test_valid_refs(self, tmp_path: Path) -> None:
        (tmp_path / "docs" / "governance").mkdir(parents=True)
        (tmp_path / "docs" / "governance" / "RULES.md").write_text("# Rules\n", encoding="utf-8")
        (tmp_path / "AGENTS.md").write_text(
            "See [rules](docs/governance/RULES.md).\n",
            encoding="utf-8",
        )
        report = run_validate(tmp_path)
        assert report.valid


class TestValidateReqUnique:
    def test_duplicate_req_ids(self, tmp_path: Path) -> None:
        docs = tmp_path / "docs"
        docs.mkdir()
        (docs / "REQUIREMENTS.md").write_text(
            "REQ-CLI-001: first\nREQ-CLI-001: duplicate\n", encoding="utf-8"
        )
        report = run_validate(tmp_path)
        unique_results = [r for r in report.results if r.name == "req-unique"]
        assert len(unique_results) == 1
        assert not unique_results[0].passed
