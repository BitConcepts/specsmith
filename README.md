# specsmith

[![CI](https://github.com/BitConcepts/specsmith/actions/workflows/ci.yml/badge.svg)](https://github.com/BitConcepts/specsmith/actions/workflows/ci.yml)
[![Docs](https://readthedocs.org/projects/specsmith/badge/?version=stable)](https://specsmith.readthedocs.io/en/stable/)
[![PyPI Stable](https://img.shields.io/pypi/v/specsmith?label=stable&style=flat&color=blue&cacheSeconds=60)](https://pypi.org/project/specsmith/)
[![PyPI Dev](https://img.shields.io/pypi/v/specsmith?include_prereleases&label=dev&style=flat&color=orange&cacheSeconds=60)](https://pypi.org/project/specsmith/#history)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**Governed project scaffolds for AI-assisted development.**

> Intelligence proposes. Constraints decide. The ledger remembers.

---

## The Problem

AI coding agents are powerful but unstructured. Without governance, they skip verification, lose context between sessions, and produce inconsistent results. specsmith generates the governance layer — the rules, verification tools, CI pipelines, and documentation — that makes AI-assisted development auditable and repeatable.

## What specsmith Does

**For new projects:** `specsmith init` generates a complete project scaffold with governance files, CI/CD, verification tools, and agent integration files tailored to your project type.

**For existing projects:** `specsmith import` detects your project's language, build system, and test framework, then generates governance overlay files without modifying your source code. Existing files are preserved.

**For ongoing governance:** `specsmith audit` checks health, `specsmith export` generates compliance reports, `specsmith doctor` verifies your tools are installed.

Every governed project follows the closed-loop workflow: **propose → check → execute → verify → record**.

## Install

```bash
pip install specsmith
```

## Quick Start

```bash
# Install
pip install specsmith

# New project (interactive)
specsmith init

# Adopt an existing project
specsmith import --project-dir ./my-project

# Check governance health
specsmith audit --project-dir ./my-project

# Generate architecture docs interactively
specsmith architect --project-dir ./my-project

# Start an AI agent session (universal pattern)
# From any governed repo root:
/agent AGENTS.md
```

### Starting an AI Agent Session

The universal pattern for any specsmith-governed project:

```
/agent AGENTS.md
```

This works in Warp, Claude Code, Cursor, and any agent that reads markdown context files. The agent loads AGENTS.md (the governance hub), reads LEDGER.md for session state, and picks up from the last recorded action.

## 30 Project Types

**Software:** Python, Rust, Go, C/C++, .NET, JS/TS, mobile, monorepo, microservices, DevOps/IaC, data/ML, browser extensions.

**Hardware:** FPGA/RTL, Yocto BSP, PCB design, embedded systems.

**Documents:** Technical specifications, user manuals, research papers, API specifications, requirements management.

**Business/Legal:** Business plans, patent applications, legal/compliance frameworks.

Each type gets: tool-aware CI (correct lint/test/security/build tools), domain-specific directory structure, governance rules in AGENTS.md, and pre-populated requirements and test stubs.

## 40+ CLI Commands

| Command | Purpose |
|---------|---------|
| `init` | Scaffold a new governed project |
| `import` | Adopt an existing project (merge mode) |
| `audit` | Drift detection and health checks (`--fix` to auto-repair) |
| `architect` | Interactive architecture generation |
| `validate` | Governance consistency + H11 blocking-loop detection |
| `compress` | Archive old ledger entries |
| `upgrade` | Update governance to new spec version |
| `status` | CI/PR/alert status from VCS platform |
| `diff` | Compare governance against templates |
| `export` | Compliance report with REQ↔TEST coverage |
| `doctor` | Check if verification tools are installed |
| `self-update` | Update specsmith (channel-aware) |
| `credits` | AI credit tracking, analysis, budgets, and rate-limit pacing |
| `exec` / `ps` / `abort` | Tracked process execution with PID tracking and timeout |
| `commit` / `push` / `sync` | Governance-aware VCS operations |
| `branch` / `pr` | Strategy-aware branching and PR creation |
| `ledger` | Structured ledger add/list/stats |
| `req` | Requirements list/add/trace/gaps/orphans |
| `session-end` | End-of-session checklist |

## 7 Agent Integrations

AGENTS.md (cross-platform standard), Warp/Oz, Claude Code, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Aider.

## 3 VCS Platforms

GitHub Actions, GitLab CI, Bitbucket Pipelines — all with tool-aware CI generated from the verification tool registry. Dependabot/Renovate configured per language ecosystem.

## Governance Rules (H1–H12)

specsmith-governed projects enforce 12 hard rules. Two were added in v0.2.3 for agentic workflows:

- **H11** — Every loop or blocking wait in agent-written scripts must have a deadline, a fallback exit, and a diagnostic message on timeout. `specsmith validate` enforces this automatically.
- **H12** — On Windows, multi-step automation goes into a `.cmd` file, not inline shell invocations or `.ps1` files.

See [Governance Model](https://specsmith.readthedocs.io/en/stable/governance/) for the full rule set.

## Proactive Rate Limit Pacing

specsmith ships a rolling-window scheduler that paces AI provider requests before dispatch:

- Built-in RPM/TPM profiles for OpenAI, Anthropic, and Google models (including wildcard fallbacks)
- Pre-dispatch budget check: sleeps until the 60-second window refills instead of overshooting
- Parses OpenAI-style `"Please try again in 10.793s"` messages and obeys them
- Adaptive concurrency: halved after a 429, gradually restored after consecutive successes
- Local overrides always take precedence over built-in defaults

```bash
specsmith credits limits defaults          # list built-in profiles
specsmith credits limits defaults --install  # merge into project config
specsmith credits limits status --provider openai --model gpt-5.4
```

See [Rate Limit Pacing](https://specsmith.readthedocs.io/en/stable/rate-limits/) for full details.

## Documentation

**[specsmith.readthedocs.io](https://specsmith.readthedocs.io)** — Full user manual with tutorials, command reference, project type details, tool registry, governance model, rate-limit pacing, troubleshooting.

## Links

- [PyPI](https://pypi.org/project/specsmith/)
- [Documentation](https://specsmith.readthedocs.io)
- [Changelog](CHANGELOG.md)
- [Contributing](CONTRIBUTING.md)
- [Specification](docs/AGENT-WORKFLOW-SPEC.md)
- [Security](SECURITY.md)

## License

MIT — Copyright (c) 2026 BitConcepts, LLC.
