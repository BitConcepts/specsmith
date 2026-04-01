# SPDX-License-Identifier: MIT
# Copyright (c) 2026 BitConcepts, LLC. All rights reserved.
"""Importer — detect project structure and generate governance overlay."""

from __future__ import annotations

import subprocess
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from specsmith.config import Platform, ProjectConfig, ProjectType

# File extension → language mapping
_EXT_LANG: dict[str, str] = {
    ".py": "python",
    ".rs": "rust",
    ".go": "go",
    ".c": "c",
    ".cpp": "cpp",
    ".h": "h",
    ".hpp": "hpp",
    ".cs": "csharp",
    ".js": "javascript",
    ".ts": "typescript",
    ".jsx": "jsx",
    ".tsx": "tsx",
    ".java": "java",
    ".kt": "kotlin",
    ".swift": "swift",
    ".dart": "dart",
    ".vhd": "vhdl",
    ".vhdl": "vhdl",
    ".v": "verilog",
    ".sv": "systemverilog",
    ".tf": "terraform",
    ".yml": "yaml",
    ".yaml": "yaml",
    ".bb": "bitbake",
    ".bbappend": "bitbake",
    ".proto": "protobuf",
    ".graphql": "graphql",
    ".gql": "graphql",
    ".tex": "latex",
    ".bib": "bibtex",
    ".md": "markdown",
    ".rst": "restructuredtext",
}

# Build system detection: file → build system name
_BUILD_SYSTEMS: dict[str, str] = {
    "pyproject.toml": "pyproject",
    "setup.py": "setuptools",
    "Cargo.toml": "cargo",
    "go.mod": "go-modules",
    "CMakeLists.txt": "cmake",
    "Makefile": "make",
    "package.json": "npm",
    "pom.xml": "maven",
    "build.gradle": "gradle",
    "meson.build": "meson",
    "bitbake": "bitbake",
    "pubspec.yaml": "flutter",
    "*.csproj": "dotnet",
    "*.sln": "dotnet",
}

# Test framework detection: file/dir → framework
_TEST_INDICATORS: dict[str, str] = {
    "pytest.ini": "pytest",
    "conftest.py": "pytest",
    "tests/": "pytest",
    "test/": "generic",
    "Cargo.toml": "cargo-test",
    "jest.config.js": "jest",
    "jest.config.ts": "jest",
    "vitest.config.ts": "vitest",
    "vitest.config.js": "vitest",
}

# CI detection: path → platform
_CI_INDICATORS: dict[str, str] = {
    ".github/workflows": "github",
    ".gitlab-ci.yml": "gitlab",
    "bitbucket-pipelines.yml": "bitbucket",
    "Jenkinsfile": "jenkins",
    ".circleci": "circleci",
    ".travis.yml": "travis",
}


@dataclass
class DetectionResult:
    """Results from analyzing an existing project."""

    root: Path
    languages: dict[str, int] = field(default_factory=dict)
    primary_language: str = ""
    build_system: str = ""
    test_framework: str = ""
    vcs_platform: str = ""
    has_git: bool = False
    git_remote: str = ""
    existing_governance: list[str] = field(default_factory=list)
    existing_ci: str = ""
    inferred_type: ProjectType | None = None
    file_count: int = 0
    modules: list[str] = field(default_factory=list)
    test_files: list[str] = field(default_factory=list)
    entry_points: list[str] = field(default_factory=list)


def detect_project(root: Path) -> DetectionResult:
    """Walk an existing project and detect its structure.

    Returns a DetectionResult with inferred configuration.
    """
    result = DetectionResult(root=root)

    # Walk directory tree
    lang_counter: Counter[str] = Counter()
    all_files: list[Path] = []
    skip_dirs = {
        ".git",
        ".venv",
        "venv",
        "node_modules",
        "__pycache__",
        ".work",
        "build",
        "dist",
        "target",
        ".tox",
        ".eggs",
    }

    for path in root.rglob("*"):
        if any(part in skip_dirs for part in path.parts):
            continue
        if path.is_file():
            all_files.append(path)
            ext = path.suffix.lower()
            lang = _EXT_LANG.get(ext)
            if lang:
                lang_counter[lang] += 1

    result.file_count = len(all_files)
    result.languages = dict(lang_counter.most_common())
    if lang_counter:
        result.primary_language = lang_counter.most_common(1)[0][0]

    # Build system
    for indicator, system in _BUILD_SYSTEMS.items():
        if indicator.startswith("*"):
            if any(f.name.endswith(indicator[1:]) for f in all_files):
                result.build_system = system
                break
        elif (root / indicator).exists():
            result.build_system = system
            break

    # Test framework
    for indicator, framework in _TEST_INDICATORS.items():
        if indicator.endswith("/"):
            if (root / indicator.rstrip("/")).is_dir():
                result.test_framework = framework
                break
        elif (root / indicator).exists():
            result.test_framework = framework
            break

    # CI detection
    for indicator, platform in _CI_INDICATORS.items():
        if (root / indicator).exists():
            result.existing_ci = platform
            result.vcs_platform = platform if platform in ("github", "gitlab", "bitbucket") else ""
            break

    # Git
    git_dir = root / ".git"
    result.has_git = git_dir.exists()
    if result.has_git:
        try:
            remote = subprocess.run(
                ["git", "-C", str(root), "remote", "get-url", "origin"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if remote.returncode == 0:
                result.git_remote = remote.stdout.strip()
                if "github.com" in result.git_remote:
                    result.vcs_platform = "github"
                elif "gitlab" in result.git_remote:
                    result.vcs_platform = "gitlab"
                elif "bitbucket" in result.git_remote:
                    result.vcs_platform = "bitbucket"
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

    # Existing governance
    for gov_file in (
        "AGENTS.md",
        "LEDGER.md",
        "CLAUDE.md",
        "GEMINI.md",
        "docs/REQUIREMENTS.md",
        "docs/TEST_SPEC.md",
        "docs/architecture.md",
    ):
        if (root / gov_file).exists():
            result.existing_governance.append(gov_file)

    # Detect modules (Python packages, Rust crates, Go packages, etc.)
    result.modules = _detect_modules(root, result.primary_language)

    # Detect test files
    result.test_files = _detect_test_files(root, all_files)

    # Detect entry points
    result.entry_points = _detect_entry_points(root, result.primary_language)

    # Infer project type
    result.inferred_type = _infer_type(result)

    return result


def _detect_modules(root: Path, language: str) -> list[str]:
    """Detect major modules/packages in the project."""
    modules: list[str] = []

    if language == "python":
        src = root / "src"
        if src.exists():
            for d in src.iterdir():
                if d.is_dir() and (d / "__init__.py").exists():
                    modules.append(d.name)
        else:
            for d in root.iterdir():
                if d.is_dir() and (d / "__init__.py").exists() and d.name != "tests":
                    modules.append(d.name)
    elif language == "rust":
        if (root / "src" / "lib.rs").exists():
            modules.append("lib")
        if (root / "src" / "main.rs").exists():
            modules.append("main")
    elif language == "go":
        for d in root.iterdir():
            if d.is_dir() and d.name not in ("vendor", ".git"):
                go_files = list(d.glob("*.go"))
                if go_files:
                    modules.append(d.name)
    elif language in ("javascript", "typescript"):
        src = root / "src"
        if src.exists():
            for d in src.iterdir():
                if d.is_dir():
                    modules.append(d.name)

    return sorted(modules)


def _detect_test_files(root: Path, all_files: list[Path]) -> list[str]:
    """Find test files."""
    test_patterns = ("test_", "_test.", ".test.", ".spec.", "tests/", "test/")
    tests: list[str] = []
    for f in all_files:
        rel = str(f.relative_to(root))
        if any(p in rel.lower() for p in test_patterns):
            tests.append(rel)
    return sorted(tests[:50])  # Cap at 50 for readability


def _detect_entry_points(root: Path, language: str) -> list[str]:
    """Find likely entry points."""
    entries: list[str] = []
    candidates = {
        "python": ["src/*/cli.py", "src/*/__main__.py", "manage.py", "app.py", "main.py"],
        "rust": ["src/main.rs"],
        "go": ["cmd/*/main.go", "main.go"],
        "javascript": ["src/index.js", "src/index.ts", "index.js", "server.js", "app.js"],
        "typescript": ["src/index.ts", "src/main.ts"],
    }
    for pattern in candidates.get(language, []):
        for match in root.glob(pattern):
            entries.append(str(match.relative_to(root)))
    return entries


def _infer_type(result: DetectionResult) -> ProjectType:
    """Infer the best ProjectType from detection results."""
    lang = result.primary_language
    build = result.build_system

    # Hardware types
    if lang in ("vhdl", "verilog", "systemverilog"):
        return ProjectType.FPGA_RTL
    if lang == "bitbake" or build == "bitbake":
        return ProjectType.YOCTO_BSP

    # Language-specific
    if lang == "rust":
        if "lib" in result.modules:
            return ProjectType.LIBRARY_RUST
        return ProjectType.CLI_RUST
    if lang == "go":
        return ProjectType.CLI_GO
    if lang in ("c", "cpp", "h", "hpp"):
        if build == "cmake":
            if any("lib" in m for m in result.modules):
                return ProjectType.LIBRARY_C
            return ProjectType.CLI_C
        return ProjectType.EMBEDDED_HARDWARE
    if lang == "csharp":
        return ProjectType.DOTNET_APP
    if lang in ("dart", "swift", "kotlin"):
        return ProjectType.MOBILE_APP
    if lang == "terraform":
        return ProjectType.DEVOPS_IAC
    if lang == "latex":
        return ProjectType.RESEARCH_PAPER
    if lang == "protobuf":
        return ProjectType.API_SPECIFICATION
    if lang == "graphql":
        return ProjectType.API_SPECIFICATION

    # JS/TS
    if lang in ("javascript", "typescript", "jsx", "tsx"):
        if build == "npm":
            pkg = result.root / "package.json"
            if pkg.exists():
                content = pkg.read_text(encoding="utf-8")
                if "react" in content or "vue" in content or "angular" in content:
                    # Check if there's also a server
                    if (result.root / "server").exists() or "express" in content:
                        return ProjectType.FULLSTACK_JS
                    return ProjectType.WEB_FRONTEND
        return ProjectType.FULLSTACK_JS

    # Python types
    if lang == "python":
        if build in ("pyproject", "setuptools"):
            # Check for CLI entry point
            if any("cli.py" in e for e in result.entry_points):
                return ProjectType.CLI_PYTHON
            # Check for web framework
            if (result.root / "manage.py").exists():
                return ProjectType.BACKEND_FRONTEND
            return ProjectType.LIBRARY_PYTHON
        # Check for ML indicators
        if any(
            (result.root / f).exists()
            for f in ("notebooks", "data", "models", "requirements-ml.txt")
        ):
            return ProjectType.DATA_ML
        return ProjectType.CLI_PYTHON

    return ProjectType.CLI_PYTHON  # Safe default


def generate_import_config(result: DetectionResult) -> ProjectConfig:
    """Generate a ProjectConfig from detection results."""
    return ProjectConfig(
        name=result.root.name,
        type=result.inferred_type or ProjectType.CLI_PYTHON,
        platforms=[Platform.WINDOWS, Platform.LINUX, Platform.MACOS],
        language=result.primary_language or "python",
        description=f"Imported project ({result.file_count} files detected)",
        git_init=False,  # Already has git
        vcs_platform=result.vcs_platform,
        detected_build_system=result.build_system,
        detected_test_framework=result.test_framework,
    )


def generate_overlay(
    result: DetectionResult,
    target: Path,
    *,
    force: bool = False,
) -> list[Path]:
    """Generate governance overlay files for an existing project."""
    from datetime import date

    created: list[Path] = []

    def _write(rel_path: str, content: str) -> None:
        path = target / rel_path
        if path.exists() and not force:
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        created.append(path)

    name = result.root.name
    lang = result.primary_language or "unknown"
    today = date.today().isoformat()
    ptype = result.inferred_type.value if result.inferred_type else "unknown"

    # AGENTS.md
    _write(
        "AGENTS.md",
        f"# {name} — Agent Governance\n\n"
        "This project was imported by specsmith. The governance files contain "
        "detected structure. Review and enrich with your agent.\n\n"
        "## Project Summary\n"
        f"- **Language**: {lang}\n"
        f"- **Build system**: {result.build_system or 'not detected'}\n"
        f"- **Test framework**: {result.test_framework or 'not detected'}\n"
        f"- **Files detected**: {result.file_count}\n"
        f"- **Modules**: {', '.join(result.modules) or 'none detected'}\n\n"
        "## Workflow Rules\n"
        "1. Read AGENTS.md fully before starting any task.\n"
        "2. Log all changes in LEDGER.md.\n"
        "3. Map changes to requirements in docs/REQUIREMENTS.md.\n"
        "4. Verify against docs/TEST_SPEC.md.\n",
    )

    # LEDGER.md
    _write(
        "LEDGER.md",
        "# Change Ledger\n\n"
        f"## {today} — specsmith import\n"
        f"- Imported project: {name}\n"
        f"- Detected type: {ptype}\n"
        f"- Language: {lang}\n"
        f"- Build system: {result.build_system}\n",
    )

    # docs/REQUIREMENTS.md
    reqs = "# Requirements\n\nRequirements auto-generated from project detection.\n\n"
    for module in result.modules:
        mu = module.upper().replace(" ", "-")
        reqs += (
            f"## REQ-{mu}-001\n"
            f"- **Component**: {module}\n"
            f"- **Status**: Draft\n"
            f"- **Description**: [Describe requirements for {module}]\n\n"
        )
    if result.build_system:
        reqs += (
            "## REQ-BUILD-001\n"
            f"- **Build system**: {result.build_system}\n"
            "- **Status**: Draft\n"
            f"- **Description**: Project builds successfully with {result.build_system}\n\n"
        )
    _write("docs/REQUIREMENTS.md", reqs)

    # docs/TEST_SPEC.md
    tests = "# Test Specification\n\nTests auto-generated from project detection.\n\n"
    for i, test_file in enumerate(result.test_files[:20], 1):
        tests += f"## TEST-{i:03d}\n- **File**: {test_file}\n- **Status**: Detected\n"
        for module in result.modules:
            if module in test_file:
                tests += f"- **Requirement**: REQ-{module.upper()}-001\n"
                break
        tests += "\n"
    _write("docs/TEST_SPEC.md", tests)

    # docs/architecture.md
    arch = (
        f"# Architecture — {name}\n\n"
        "Architecture auto-generated from project detection.\n\n"
        "## Overview\n"
        f"- **Language**: {lang}\n"
        f"- **Build system**: {result.build_system or 'not detected'}\n"
        f"- **Test framework**: {result.test_framework or 'not detected'}\n\n"
    )
    if result.modules:
        arch += "## Modules\n"
        for module in result.modules:
            arch += f"- **{module}**: [Describe module purpose]\n"
        arch += "\n"
    if result.entry_points:
        arch += "## Entry Points\n"
        for ep in result.entry_points:
            arch += f"- `{ep}`\n"
        arch += "\n"
    if result.languages:
        arch += "## Language Distribution\n"
        for lang_name, count in sorted(result.languages.items(), key=lambda x: -x[1]):
            arch += f"- {lang_name}: {count} files\n"
    _write("docs/architecture.md", arch)

    return created
