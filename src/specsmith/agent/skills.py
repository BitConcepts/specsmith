# SPDX-License-Identifier: MIT
# Copyright (c) 2026 BitConcepts, LLC. All rights reserved.
"""Skills loader — reads SKILL.md files and injects them into agent context.

Inspired by ECC's skills system: skills are reusable workflow bundles that
agents read and follow. They provide structured guidance for specific tasks
(TDD, code review, verification loops, epistemic audits, etc.).

Skills are loaded from (in priority order):
  1. .warp/skills/*.md (Warp/Oz native)
  2. .claude/skills/*.md (Claude Code)
  3. src/specsmith/agent/profiles/*.md (built-in specsmith profiles)
  4. Any *.md files matching SKILL.md naming convention

Skills are injected as additional system context when relevant.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Skill:
    """A loaded skill definition."""

    name: str
    description: str
    content: str
    source_path: str
    tags: list[str] = field(default_factory=list)
    domain: str = ""  # e.g., "testing", "governance", "epistemic", "vcs"


def load_skills(project_root: Path) -> list[Skill]:
    """Load all skills from the project and built-in profiles.

    Returns skills sorted by domain priority:
    epistemic > governance > verification > testing > vcs
    """
    skills: list[Skill] = []
    seen_names: set[str] = set()

    # Search locations (priority order)
    search_dirs = [
        project_root / ".warp" / "skills",
        project_root / ".claude" / "skills",
        project_root / ".agents" / "skills",
        _builtin_profiles_dir(),
    ]

    for search_dir in search_dirs:
        if not search_dir.exists():
            continue
        for skill_file in sorted(search_dir.rglob("SKILL.md")):
            skill = _parse_skill_file(skill_file)
            if skill and skill.name not in seen_names:
                skills.append(skill)
                seen_names.add(skill.name)
        # Also load bare .md files in the skills dir
        for md_file in sorted(search_dir.glob("*.md")):
            if md_file.name != "SKILL.md":
                skill = _parse_skill_file(md_file)
                if skill and skill.name not in seen_names:
                    skills.append(skill)
                    seen_names.add(skill.name)

    return _prioritize_skills(skills)


def get_skill_by_name(skills: list[Skill], name: str) -> Skill | None:
    """Find a skill by name (case-insensitive)."""
    name_lower = name.lower()
    return next(
        (s for s in skills if s.name.lower() == name_lower or name_lower in s.name.lower()),
        None,
    )


def format_skills_context(skills: list[Skill], max_tokens: int = 3000) -> str:
    """Format skills for injection into the system prompt.

    Truncates to avoid consuming too much context (ECC lesson:
    context window is precious — disable what you don't need).
    """
    if not skills:
        return ""

    lines = ["## Available Skills\n"]
    total_chars = len(lines[0])

    for skill in skills:
        entry = f"### {skill.name}\n{skill.description}\n"
        if total_chars + len(entry) > max_tokens * 4:  # ~4 chars per token
            lines.append(f"_... {len(skills) - len(lines) + 1} more skills not shown_\n")
            break
        lines.append(entry)
        total_chars += len(entry)

    return "\n".join(lines)


def _parse_skill_file(path: Path) -> Skill | None:
    """Parse a skill file and return a Skill object."""
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None

    # Try to extract name from frontmatter
    name = ""
    description = ""
    tags: list[str] = []
    domain = ""

    # YAML frontmatter: ---\nname: ...\n---
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if fm_match:
        fm = fm_match.group(1)
        name_m = re.search(r"^name:\s*(.+)$", fm, re.MULTILINE)
        desc_m = re.search(r"^description:\s*(.+)$", fm, re.MULTILINE)
        tags_m = re.search(r"^tags:\s*\[(.+)\]", fm, re.MULTILINE)
        domain_m = re.search(r"^domain:\s*(.+)$", fm, re.MULTILINE)

        if name_m:
            name = name_m.group(1).strip().strip("\"'")
        if desc_m:
            description = desc_m.group(1).strip().strip("\"'")
        if tags_m:
            tags = [t.strip().strip("\"'") for t in tags_m.group(1).split(",")]
        if domain_m:
            domain = domain_m.group(1).strip()

    # Fall back to first heading
    if not name:
        h1 = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        name = h1.group(1).strip() if h1 else path.stem.replace("-", " ").replace("_", " ").title()

    # Fall back to first non-heading paragraph for description
    if not description:
        paras = re.split(r"\n\n+", content)
        for para in paras[1:3]:
            cleaned = para.strip().lstrip("#").strip()
            if cleaned and len(cleaned) > 10:
                description = cleaned[:200]
                break

    # Infer domain from name and content
    if not domain:
        content_lower = content.lower()
        if any(w in content_lower for w in ["epistemic", "belief", "aee", "stress-test"]):
            domain = "epistemic"
        elif any(w in content_lower for w in ["governance", "ledger", "audit", "proposal"]):
            domain = "governance"
        elif any(w in content_lower for w in ["verification", "verify", "build", "lint"]):
            domain = "verification"
        elif any(w in content_lower for w in ["tdd", "test", "coverage", "pytest"]):
            domain = "testing"
        elif any(w in content_lower for w in ["commit", "push", "branch", "pr ", "pull request"]):
            domain = "vcs"
        else:
            domain = "general"

    return Skill(
        name=name,
        description=description,
        content=content,
        source_path=str(path),
        tags=tags,
        domain=domain,
    )


def _builtin_profiles_dir() -> Path:
    """Return the path to built-in agent profiles."""
    return Path(__file__).parent / "profiles"


_DOMAIN_PRIORITY = {
    "epistemic": 0,
    "governance": 1,
    "verification": 2,
    "testing": 3,
    "vcs": 4,
    "general": 5,
}


def _prioritize_skills(skills: list[Skill]) -> list[Skill]:
    return sorted(skills, key=lambda s: _DOMAIN_PRIORITY.get(s.domain, 99))
