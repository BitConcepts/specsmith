# Ledger — specsmith

## Session 2026-04-01 — Initial CLI implementation

**Status:** Complete
**Scope:** Full CLI tool with 5 commands, 4 agent adapters, CI/CD, tests

### Proposal
Build specsmith CLI tool with: init (scaffold generation), audit (health checks),
validate (consistency), compress (ledger archival), upgrade (spec version migration).
Add agent integration adapters for Warp, Claude Code, Cursor, and Copilot.

Estimated cost: high

### Changes
- `src/specsmith/cli.py` — click CLI with init, audit, validate, compress, upgrade
- `src/specsmith/scaffolder.py` — Jinja2 template renderer with project type logic
- `src/specsmith/config.py` — pydantic ProjectConfig with 8 project types
- `src/specsmith/auditor.py` — governance file checks, REQ↔TEST coverage, ledger health
- `src/specsmith/validator.py` — scaffold.yml, AGENTS.md refs, REQ uniqueness
- `src/specsmith/compressor.py` — ledger archival with configurable thresholds
- `src/specsmith/upgrader.py` — governance template re-rendering on version bump
- `src/specsmith/integrations/` — base adapter + Warp, Claude Code, Cursor, Copilot
- `src/specsmith/templates/` — 30+ Jinja2 templates for governed scaffolds
- `.github/workflows/ci.yml` — lint + typecheck + test matrix + security audit
- `.github/workflows/release.yml` — tag-triggered build → GitHub Release
- `docs/REQUIREMENTS.md` — 37 formal requirements
- `docs/TEST_SPEC.md` — 30 test specifications

### Verification
- 36 tests passing (pytest)
- ruff lint: clean
- ruff format: clean
- mypy strict: clean
- CI: lint ✓, security ✓, typecheck pending (fix pushed)

### Open TODOs
- [x] Add VCS platform integrations (GitHub/GitLab/Bitbucket CLI)
- [x] Add Gemini, Windsurf, Aider agent adapters
- [x] Expand CLI runner test coverage
- [x] Self-host governance (this file)

## Session 2026-04-02 — v0.2.0→v0.2.2 release cycle

**Status:** Complete
**Scope:** Major feature release + two patch releases

### Changes
- **v0.2.0**: Uppercase governance filenames, community templates (#42), AI credit tracking (#50/#51), architect command (#49), self-update, multi-language detection, dynamic versioning, VCS commands, ledger/req/test CLIs, plugin scaffold
- **v0.2.1**: Process abort/PID tracking (exec/ps/abort commands), language-specific templates (#41 — Rust, Go, JS/TS), RTD integration (#38), release workflow templates (#44), PyPI integration (#36), template refactor (#45), upgrade --full sync mechanism
- **v0.2.2**: Auto-fix AGENTS.md references on lowercase→uppercase migration, alternate path detection (docs/LEDGER.md, docs/architecture/**), case-insensitive architecture check, CI-gated dev releases

### Issues closed
- #36, #38, #41, #42, #44, #45 (closed), #55, #56 (filed)
- Created v0.3.0 milestone, assigned 6 remaining issues

### Verification
- 115 tests passing (pytest, 3 OS × 3 Python)
- ruff check + format: clean (src/ + tests/)
- mypy strict: clean
- CI: 19/19 checks pass on all PRs before merge
- CodeQL: 0 open alerts
- Dependabot: 0 open alerts

### Open TODOs
- [ ] #55: Fix governance table rendering on RTD (double pipe)
- [ ] #56: Document 15+ missing CLI commands in RTD
- [ ] #52: Credit budget cap enforcement
- [ ] #37: Secure API key management
- [ ] #10: USPTO/MCP patent integration
- [ ] #17: Multi-project workspace management
