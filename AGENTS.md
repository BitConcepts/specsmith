# AGENTS.md — specsmith

## Identity
- **Project**: specsmith
- **Type**: CLI tool (Python) + AEE library — Spec Section 17.3
- **Spec version**: 0.3.0
- **Language**: Python 3.10+
- **Platforms**: Windows, Linux, macOS

## Purpose
Applied Epistemic Engineering toolkit for AI-assisted development. Treats belief systems
like code: codable, testable, deployable. Co-installs the `epistemic` standalone library.
Includes an AEE-integrated agentic client (`specsmith run`) supporting Claude, GPT, Gemini,
and local Ollama models.

## Quick Commands
- `pip install -e ".[dev]"` — dev install
- `pytest tests/ -v` — run tests
- `ruff check src/ tests/` — lint
- `ruff format src/ tests/` — format
- `mypy src/specsmith/` — typecheck
- `specsmith init` — scaffold a new project
- `specsmith audit` — health checks
- `specsmith validate` — governance consistency
- `specsmith stress-test` — AEE adversarial challenges
- `specsmith epistemic-audit` — full AEE pipeline
- `specsmith belief-graph` — belief artifact dependency graph
- `specsmith trace seal/verify/log` — cryptographic trace vault
- `specsmith run` — agentic REPL (requires provider)
- `specsmith run --base-url <url>` — run with custom local provider (Jan, LM Studio, vLLM)
- `specsmith serve` — start local daemon with REST + WebSocket API _(planned)_
- `specsmith agent providers` — check provider status

### Planned agentic REPL slash commands (Phase 1–2)
- `/model <name>` — switch model mid-session
- `/spawn <type> <prompt>` — spawn a subagent worker
- `/team <name>` — create a peer-to-peer agent team
- `/learn [pattern]` — promote a session pattern to an instinct
- `/instinct-status` — show active instincts with confidence scores
- `/eval define <feature>` — create an eval task definition
- `/eval run [--trials k]` — run eval trials and compute pass@k
- `/hooks-enable <name>` / `/hooks-disable <name>` — runtime hook control
- `/security-scan` — run OWASP-style security analysis
- `/mcp-list` — list configured MCP servers

## File Registry
- `src/specsmith/` — specsmith CLI package
- `src/epistemic/` — standalone AEE library (canonical location)
- `src/specsmith/epistemic/` — compatibility shim (re-exports from epistemic)
- `src/specsmith/agent/` — agentic client (providers, tools, runner, hooks, skills)
- `src/specsmith/agent/profiles/` — built-in agent profiles (planner, verifier, epistemic-auditor)
- `src/specsmith/templates/` — Jinja2 scaffold templates (incl. 4 new epistemic templates)
- `src/specsmith/integrations/` — agent platform adapters
- `src/specsmith/commands/` — harness slash command implementations _(planned)_
- `src/specsmith/operations.py` — typed ProjectOperations (file/git/search) _(planned)_
- `src/specsmith/instinct.py` — instinct persistence and continuous learning _(planned)_
- `src/specsmith/memory.py` — cross-session agent memory _(planned)_
- `src/specsmith/eval/` — EDD eval harness (Task/Trial/Grader/pass@k) _(planned)_
- `src/specsmith/server/` — specsmith serve daemon (REST + WebSocket) _(planned)_
- `src/specsmith/agent/spawner.py` — AgentTool subagent spawning _(planned)_
- `src/specsmith/agent/orchestrator.py` — orchestrator meta-agent on Ollama _(planned)_
- `src/specsmith/agent/teams.py` — agent team coordination via filesystem mailbox _(planned)_
- `src/specsmith/agent/flags.py` — feature flag system for tool schema gating _(planned)_
- `tests/` — test suite
- `docs/REQUIREMENTS.md` — formal requirements (extended April 2026)
- `docs/TEST_SPEC.md` — test specifications
- `docs/ARCHITECTURE.md` — architecture reference (extended April 2026)
- `docs/governance/` — modular governance docs
- `docs/AGENT-WORKFLOW-SPEC.md` — the specification itself
- `C:\Users\trist\Development\BitConcepts\everything-claude-code` — ECC reference (local clone)

## Governance
This project follows its own specification. See:
- [Agent Workflow Specification](docs/AGENT-WORKFLOW-SPEC.md) — the full spec (H1–H13, session lifecycle, proposal format, ledger format)
- [Epistemic Axioms](docs/governance/EPISTEMIC-AXIOMS.md) — AEE axioms applied to specsmith

Note: modular governance files are not generated for specsmith's own repo since
AGENTS.md is < 200 lines. Run `specsmith upgrade --full` to generate them if needed.

## Tech Stack
- CLI: click
- Templates: jinja2
- Config: pydantic + pyyaml
- Output: rich
- Lint: ruff
- Types: mypy (strict)
- Tests: pytest + pytest-cov
- CI: GitHub Actions (3 OS × 3 Python)
- Docs: Read the Docs (specsmith.readthedocs.io)
- Retrieval: rank_bm25 _(planned — upgrade from keyword scoring)_
- File watching: watchdog _(planned — index refresh)_
- Service: FastAPI or aiohttp + websockets _(planned — specsmith serve)_
- IDE: Eclipse Theia + @theia/ai-core _(planned — specsmith-ide repo)_

## Documentation Rule (H14 — Hard Rule)

The Read the Docs site (`docs/site/`) is the authoritative user manual.
Before committing ANY change, verify documentation is current:
1. Check if the change affects user-facing behavior, CLI commands, governance files, or configuration
2. If yes: update the relevant `docs/site/*.md` page(s) in the SAME commit
3. Update `README.md` if it affects the project summary
4. Update `CHANGELOG.md` under [Unreleased]
5. README.md links to RTD for details — do NOT duplicate RTD content in README
6. The VS Code extension docs live in `docs/site/vscode-extension.md` — update when GovernancePanel, SettingsPanel, SessionPanel, or HelpPanel change

This is a hard rule. Undocumented features are governance violations. Never commit code without checking for documentation gaps.
