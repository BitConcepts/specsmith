# Test Specification — specsmith

## Unit Tests

### Config

- **TEST-CFG-001**: ProjectConfig creates with minimal input (name + type)
  Covers: REQ-CFG-001
- **TEST-CFG-002**: ProjectConfig rejects invalid project type
  Covers: REQ-CFG-001
- **TEST-CFG-003**: package_name converts hyphens to underscores
  Covers: REQ-CFG-003
- **TEST-CFG-004**: All 20 project types have valid type_label and section_ref
  Covers: REQ-CFG-002

### Auditor

- **TEST-AUD-001**: Audit passes for a fully scaffolded project
  Covers: REQ-AUD-001
- **TEST-AUD-002**: Audit detects missing AGENTS.md
  Covers: REQ-AUD-001
- **TEST-AUD-003**: Audit detects oversized ledger
  Covers: REQ-AUD-004, REQ-AUD-005
- **TEST-AUD-004**: Audit checks governance bloat thresholds
  Covers: REQ-AUD-006
- **TEST-AUD-005**: Audit detects modular governance requirement when AGENTS.md large
  Covers: REQ-AUD-002, REQ-AUD-003

### Validator

- **TEST-VAL-001**: Validate passes for valid scaffold.yml
  Covers: REQ-VAL-001
- **TEST-VAL-002**: Validate detects broken AGENTS.md references
  Covers: REQ-VAL-002
- **TEST-VAL-003**: Validate detects duplicate requirement IDs
  Covers: REQ-VAL-003
- **TEST-VAL-004**: Validate checks architecture.md references requirements
  Covers: REQ-VAL-004

### Compressor

- **TEST-CMP-001**: Compress skips when ledger is below threshold
  Covers: REQ-CMP-003
- **TEST-CMP-002**: Compress archives old entries and creates ledger-archive.md
  Covers: REQ-CMP-001, REQ-CMP-002
- **TEST-CMP-003**: Compress preserves recent entries
  Covers: REQ-CMP-001

### Upgrader

- **TEST-UPG-001**: Upgrade skips when already at target version
  Covers: REQ-UPG-001
- **TEST-UPG-002**: Upgrade re-renders governance files and updates scaffold.yml
  Covers: REQ-UPG-002, REQ-UPG-003

## Integration Tests

### Scaffolder

- **TEST-SCF-001**: CLI Python scaffold creates expected file set
  Covers: REQ-SCF-001, REQ-SCF-002
- **TEST-SCF-002**: FPGA scaffold omits pyproject.toml
  Covers: REQ-SCF-002
- **TEST-SCF-003**: Library scaffold includes pyproject.toml without cli.py
  Covers: REQ-SCF-002
- **TEST-SCF-004**: .gitkeep files created in empty directories
  Covers: REQ-SCF-003
- **TEST-SCF-005**: scaffold.yml written after init
  Covers: REQ-SCF-005
- **TEST-SCF-006**: Warp integration files created when configured
  Covers: REQ-SCF-006, REQ-INT-001

### CLI

- **TEST-CLI-001**: `specsmith --version` outputs version string
  Covers: REQ-CLI-007
- **TEST-CLI-002**: `specsmith init --config` creates project from YAML
  Covers: REQ-CLI-001
- **TEST-CLI-003**: `specsmith audit` exits 0 on healthy project
  Covers: REQ-CLI-002
- **TEST-CLI-004**: `specsmith validate` exits 0 on valid project
  Covers: REQ-CLI-003

### Integrations

- **TEST-INT-001**: Warp adapter generates SKILL.md with project metadata
  Covers: REQ-INT-001
- **TEST-INT-002**: Claude Code adapter generates CLAUDE.md
  Covers: REQ-INT-002
- **TEST-INT-003**: Cursor adapter generates governance.mdc
  Covers: REQ-INT-003
- **TEST-INT-004**: Copilot adapter generates copilot-instructions.md
  Covers: REQ-INT-004
- **TEST-INT-005**: Adapter registry lists all available adapters
  Covers: REQ-INT-005

### Tool Registry

- **TEST-TLR-001**: Python CLI type has ruff, mypy, pytest, pip-audit, ruff format
  Covers: REQ-TLR-001
- **TEST-TLR-002**: Rust CLI type has clippy, cargo check, cargo test, cargo audit, cargo fmt
  Covers: REQ-TLR-001
- **TEST-TLR-003**: Go, web-frontend, FPGA, embedded, .NET types have correct tools
  Covers: REQ-TLR-001
- **TEST-TLR-004**: All 30 project types have at least one tool registered
  Covers: REQ-TLR-001, REQ-CFG-002
- **TEST-TLR-005**: get_tools() returns defaults from registry
  Covers: REQ-TLR-001
- **TEST-TLR-006**: get_tools() respects verification_tools overrides
  Covers: REQ-TLR-003, REQ-CFG-004
- **TEST-TLR-007**: Format check commands convert correctly (ruff, cargo fmt, prettier)
  Covers: REQ-TLR-004
- **TEST-TLR-008**: All languages in LANG_CI_META have docker_image
  Covers: REQ-TLR-002

### Importer

- **TEST-IMP-001**: Detects Python project (language, build system, test framework, type)
  Covers: REQ-IMP-001, REQ-IMP-002, REQ-IMP-003, REQ-IMP-006
- **TEST-IMP-002**: Detects Rust project
  Covers: REQ-IMP-001, REQ-IMP-002, REQ-IMP-006
- **TEST-IMP-003**: Detects JS web project
  Covers: REQ-IMP-001, REQ-IMP-002, REQ-IMP-006
- **TEST-IMP-004**: Detects entry points and test files
  Covers: REQ-IMP-005
- **TEST-IMP-005**: Detects GitHub CI and governance files
  Covers: REQ-IMP-004, REQ-IMP-005
- **TEST-IMP-006**: Empty directory returns safe defaults
  Covers: REQ-IMP-006
- **TEST-IMP-007**: generate_import_config produces correct ProjectConfig
  Covers: REQ-IMP-006, REQ-CFG-005
- **TEST-IMP-008**: Overlay creates all 5 governance files
  Covers: REQ-IMP-007
- **TEST-IMP-009**: Overlay skips existing files without --force
  Covers: REQ-IMP-008
- **TEST-IMP-010**: Overlay force-overwrites existing files
  Covers: REQ-IMP-008

### VCS Platforms (Tool-Aware CI)

- **TEST-VCS-001**: GitHub CI for Python has ruff, mypy, pytest, pip-audit
  Covers: REQ-VCS-001
- **TEST-VCS-002**: GitHub CI for Rust has cargo clippy, cargo test, rust-toolchain
  Covers: REQ-VCS-001, REQ-VCS-002
- **TEST-VCS-003**: GitHub CI for Go has golangci-lint, go test, setup-go
  Covers: REQ-VCS-001, REQ-VCS-002
- **TEST-VCS-004**: GitHub CI for FPGA has vsg, ghdl
  Covers: REQ-VCS-001, REQ-VCS-002
- **TEST-VCS-005**: Dependabot config uses correct ecosystem (pip, cargo, gomod)
  Covers: REQ-VCS-003
- **TEST-VCS-006**: GitLab CI for Rust uses rust:latest image and cargo commands
  Covers: REQ-VCS-001
- **TEST-VCS-007**: Bitbucket pipelines for Python has python:3.12-slim image
  Covers: REQ-VCS-001

### Sandbox — Import Workflow

- **TEST-SBX-001**: Full import of realistic Python CLI project (detection, overlay, audit)
  Covers: REQ-CLI-008, REQ-IMP-001, REQ-IMP-002, REQ-IMP-003, REQ-IMP-006, REQ-IMP-007
- **TEST-SBX-002**: Import skip behavior (no overwrite without --force)
  Covers: REQ-IMP-008
- **TEST-SBX-003**: Import force overwrites existing files
  Covers: REQ-IMP-008
- **TEST-SBX-004**: Import idempotent restart
  Covers: REQ-IMP-007

### Sandbox — New Project Workflow

- **TEST-SBX-005**: Full scaffold from config with all commands (audit/validate/compress/upgrade/diff)
  Covers: REQ-CLI-001, REQ-CLI-002, REQ-CLI-003, REQ-CLI-004, REQ-CLI-005, REQ-CLI-006, REQ-CLI-011, REQ-SCF-001, REQ-SCF-002, REQ-SCF-004, REQ-SCF-005, REQ-SCF-006, REQ-TPL-001, REQ-TPL-004
- **TEST-SBX-006**: Scaffold idempotent restart
  Covers: REQ-SCF-001
- **TEST-SBX-007**: Auditor tool verification on scaffolded project
  Covers: REQ-AUD-007, REQ-AUD-008

### Sandbox — Import with Existing Docs

- **TEST-SBX-013**: Import preserves existing REQUIREMENTS.md, TEST_SPEC.md, architecture docs
  Covers: REQ-IMP-008
- **TEST-SBX-014**: Import with --force overwrites existing docs
  Covers: REQ-IMP-008

### Sandbox — Non-Python Types

- **TEST-SBX-008**: Patent application scaffold with domain directories, requirements, tests, tools
  Covers: REQ-CFG-002, REQ-TPL-002, REQ-TPL-003
- **TEST-SBX-009**: Rust CLI scaffold with cargo CI, dependabot, and governance rules
  Covers: REQ-CFG-002, REQ-VCS-001, REQ-VCS-002
- **TEST-SBX-010**: Config inheritance (extends field) merges org defaults with child
  Covers: REQ-CFG-001, REQ-VCS-004
- **TEST-SBX-011**: Export command generates compliance report with tools and audit
  Covers: REQ-EXP-001, REQ-EXP-002, REQ-EXP-003, REQ-EXP-004
- **TEST-SBX-012**: Export to file with --output flag
  Covers: REQ-EXP-005

### Git VCS Commands

- **TEST-GIT-001**: commit generates message from ledger entry
  Covers: REQ-GIT-001
- **TEST-GIT-002**: commit refuses when ledger is stale
  Covers: REQ-GIT-002
- **TEST-GIT-003**: commit runs audit before committing
  Covers: REQ-GIT-003
- **TEST-GIT-004**: push sends to correct remote
  Covers: REQ-GIT-004
- **TEST-GIT-005**: push blocks direct-to-main from feature branch
  Covers: REQ-GIT-005
- **TEST-GIT-006**: branch create uses develop as base for gitflow
  Covers: REQ-GIT-006
- **TEST-GIT-007**: branch list annotates strategy context
  Covers: REQ-GIT-007
- **TEST-GIT-008**: pr includes ledger summary and audit in description
  Covers: REQ-GIT-008
- **TEST-GIT-009**: pr targets develop for features, main for hotfixes
  Covers: REQ-GIT-009
- **TEST-GIT-010**: sync warns on upstream governance changes
  Covers: REQ-GIT-010

### Self-Update and Migration

- **TEST-UPD-001**: update --check reports version comparison without installing
  Covers: REQ-UPD-001
- **TEST-UPD-002**: update detects when already at latest version
  Covers: REQ-UPD-001
- **TEST-UPD-003**: migrate-project detects spec_version mismatch
  Covers: REQ-UPD-004
- **TEST-UPD-004**: migrate-project regenerates governance templates
  Covers: REQ-UPD-005
- **TEST-UPD-005**: migrate-project --dry-run shows changes without writing
  Covers: REQ-UPD-007
- **TEST-UPD-006**: migrate-project preserves REQUIREMENTS.md and TEST_SPEC.md
  Covers: REQ-UPD-010
- **TEST-UPD-007**: migrate-project appends entry to LEDGER.md
  Covers: REQ-UPD-009
- **TEST-UPD-008**: agent adapters include update check instruction
  Covers: REQ-UPD-008

### Workflow Logic

- **TEST-WFL-001**: agent adapter includes post-save commit proposal logic
  Covers: REQ-WFL-001
- **TEST-WFL-002**: agent adapter includes session-end push reminder
  Covers: REQ-WFL-002
- **TEST-WFL-003**: agent adapter includes branch-check for gitflow
  Covers: REQ-WFL-003
- **TEST-WFL-004**: agent adapter includes branch proposal for new tasks
  Covers: REQ-WFL-004
- **TEST-WFL-005**: agent adapter includes PR proposal when feature complete
  Covers: REQ-WFL-005
- **TEST-WFL-006**: agent adapter includes sync-first in session start
  Covers: REQ-WFL-006
- **TEST-WFL-007**: commit --auto-push commits and pushes in sequence
  Covers: REQ-WFL-009
- **TEST-WFL-008**: session-end checklist reports unpushed commits and dirty files
  Covers: REQ-WFL-010

### Cross-Platform (CI Matrix)

- **TEST-XPL-001**: CI matrix runs tests on Windows, Linux, macOS with Python 3.10, 3.12, 3.13
  Covers: REQ-XPL-001, REQ-XPL-002

### CLI Commands (Additional Coverage)

- **TEST-CLI-005**: `specsmith init --guided` generates REQ/TEST stubs interactively
  Covers: REQ-CLI-009
- **TEST-CLI-006**: `specsmith status` runs VCS platform status check
  Covers: REQ-CLI-010
- **TEST-CLI-007**: `specsmith export` generates compliance report
  Covers: REQ-CLI-012
- **TEST-CLI-008**: `specsmith import --guided` runs architecture after import
  Covers: REQ-CLI-013
