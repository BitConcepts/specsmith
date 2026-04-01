# Contributing to specsmith

## Bootstrap Notice

specsmith is **bootstrapping its own governance process**. The tool generates the Agentic AI Development Workflow for other projects, but specsmith itself is iteratively adopting that same workflow. Future versions will be developed using an older stable version of itself — the process will converge.

Until then, governance files in this repo (`AGENTS.md`, `LEDGER.md`, `docs/governance/`) represent the target state we are working toward, not a fully enforced process yet.

## Development Setup

```bash
git clone https://github.com/BitConcepts/specsmith.git
cd specsmith
pip install -e ".[dev]"
```

## Branching Strategy (gitflow)

- `main` — production-ready releases
- `develop` — integration branch for next release
- `feature/*` — branch from `develop`, merge back to `develop`
- `release/*` — branch from `develop`, merge to `main` + `develop`
- `hotfix/*` — branch from `main`, merge to `main` + `develop`

```bash
git checkout develop
git checkout -b feature/my-feature
# work, commit, push
gh pr create --base develop
```

## Running Checks

```bash
ruff check src/ tests/ && ruff format --check src/ tests/ && mypy src/specsmith/ && pytest tests/ -v
```

## Pre-commit

```bash
pre-commit install
```

## Code Standards

- SPDX headers on all `.py` files (`MIT`, `BitConcepts, LLC.`)
- Must pass `ruff check`, `ruff format --check`, `mypy --strict`
- All features require tests
- Windows scripts: `.cmd` only (no `.ps1`)
- Line length: 100

## Tool Registry

When adding a new project type:
1. Add the enum to `config.py` (`ProjectType`)
2. Add type label and section ref to `config.py` (`_TYPE_LABELS`, `_SECTION_REFS`)
3. Add directory structure to `scaffolder.py` (`_get_empty_dirs`)
4. Add tool entries to `tools.py` (`_TOOL_REGISTRY`)
5. Add CI metadata to `tools.py` (`LANG_CI_META`) if the language is new
6. Add type-specific rules to `templates/agents.md.j2`
7. Add tests for the new type

## Importing Existing Projects

`specsmith import` generates governance overlay for existing projects. The detection engine in `importer.py` handles:
- Language detection by file extension
- Build system detection (pyproject.toml, Cargo.toml, CMakeLists.txt, etc.)
- Test framework detection
- CI and VCS platform detection
- Module and entry point discovery

## Pull Requests

- Branch from `develop` (features) or `main` (hotfixes)
- All CI must pass (lint, typecheck, test × 9 matrix, security)
- Update `CHANGELOG.md` and docs if applicable
- One approval required

## Configurable Governance

Key tuning knobs in `scaffold.yml` for enterprise teams:

| Setting | Default | Description |
|---------|---------|-------------|
| `branching_strategy` | gitflow | gitflow, trunk-based, github-flow |
| `require_pr_reviews` | true | Require reviews before merge |
| `required_approvals` | 1 | Number of required approvals |
| `require_ci_pass` | true | CI must pass before merge |
| `allow_force_push` | false | Allow force push to protected branches |
| `use_remote_rules` | false | Accept existing remote branch rules |
| `vcs_platform` | github | github, gitlab, bitbucket |
