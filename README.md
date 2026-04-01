# specsmith

[![CI](https://github.com/BitConcepts/specsmith/actions/workflows/ci.yml/badge.svg)](https://github.com/BitConcepts/specsmith/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Forge governed project scaffolds from the Agentic AI Development Workflow Specification.

> Intelligence proposes. Constraints decide. The ledger remembers.

---

## What is specsmith?

`specsmith` is a CLI tool that generates full project scaffolds with built-in AI agent governance. It creates the file structure, CI/CD pipelines, governance documents, and agent integration files that AI coding assistants need to work within a structured, auditable workflow.

Every scaffolded project follows the closed-loop workflow: **propose → check → execute → verify → record**.

## Install

```bash
pip install specsmith
```

From source:

```bash
git clone https://github.com/BitConcepts/specsmith.git
cd specsmith
pip install -e ".[dev]"
```

## Quick Start

```bash
# Interactive scaffold
specsmith init

# From config file
specsmith init --config scaffold.yml --no-git

# Health checks on an existing governed project
specsmith audit --project-dir ./my-project
specsmith validate --project-dir ./my-project

# Ledger maintenance
specsmith compress --project-dir ./my-project

# Upgrade governance to newer spec version
specsmith upgrade --spec-version 0.2.0 --project-dir ./my-project
```

## Commands

| Command | Description |
|---------|-------------|
| `specsmith init` | Scaffold a new governed project (interactive or YAML-driven) |
| `specsmith audit` | Drift detection and health checks (file existence, REQ↔TEST coverage, ledger health, context bloat) |
| `specsmith validate` | Governance consistency (scaffold.yml, AGENTS.md refs, REQ uniqueness, arch↔req linkage) |
| `specsmith compress` | Archive old ledger entries to `docs/ledger-archive.md` |
| `specsmith upgrade` | Re-render governance files for a new spec version |

## Project Types

| # | Type | Spec Section |
|---|------|-------------|
| 1 | Python backend + web frontend | 17.1 |
| 2 | Python backend + web frontend + tray | 17.2 |
| 3 | CLI tool (Python) | 17.3 |
| 4 | Library / SDK (Python) | 17.4 |
| 5 | Embedded / hardware | 17.5 |
| 6 | FPGA / RTL | 17.6 |
| 7 | Yocto / embedded Linux BSP | 17.7 |
| 8 | PCB / hardware design | 17.8 |

## Agent Integrations

specsmith generates agent-specific governance files so AI assistants understand your project's rules:

| Agent | Generated File |
|-------|---------------|
| **AGENTS.md** (cross-tool standard) | `AGENTS.md` (always) |
| Warp / Oz | `.warp/skills/SKILL.md` |
| Claude Code | `CLAUDE.md` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Cursor | `.cursor/rules/governance.mdc` |
| Gemini CLI | `GEMINI.md` |
| Windsurf | `.windsurfrules` |
| Aider | `.aider.conf.yml` |

## VCS Platform Support

| Platform | CLI | CI Config | Dependency Mgmt | Security |
|----------|-----|-----------|-----------------|----------|
| **GitHub** | `gh` | GitHub Actions | Dependabot | pip-audit in CI |
| **GitLab** | `glab` | `.gitlab-ci.yml` | Renovate | pip-audit in CI |
| **Bitbucket** | `bb` | Bitbucket Pipelines | Renovate | pip-audit in CI |

## Branching Strategy

Configure one of three branching strategies per project:

- **gitflow** (default) — `main` + `develop` + feature/release/hotfix branches
- **trunk-based** — single `main` with short-lived feature branches
- **github-flow** — `main` + feature branches with PR-based workflow

Branch protection (required reviews, CI checks, no force push) is configurable.

## Configuration

Projects are configured via `scaffold.yml`:

```yaml
name: my-project
type: cli-python
platforms: [windows, linux, macos]
language: python
vcs_platform: github
branching_strategy: gitflow
require_pr_reviews: true
required_approvals: 1
require_ci_pass: true
integrations: [agents-md, warp, claude-code]
```

## Specification

See [`AGENT-WORKFLOW-SPEC.md`](AGENT-WORKFLOW-SPEC.md) for the complete workflow specification.

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for setup and guidelines.

## Security

See [SECURITY.md](SECURITY.md) for vulnerability reporting.

## License

MIT — Copyright (c) 2026 BitConcepts, LLC. See [LICENSE](LICENSE).
