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
  Covers: REQ-AUD-004
- **TEST-AUD-004**: Audit checks governance bloat thresholds
  Covers: REQ-AUD-006

### Validator

- **TEST-VAL-001**: Validate passes for valid scaffold.yml
  Covers: REQ-VAL-001
- **TEST-VAL-002**: Validate detects broken AGENTS.md references
  Covers: REQ-VAL-002
- **TEST-VAL-003**: Validate detects duplicate requirement IDs
  Covers: REQ-VAL-003

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
- **TEST-TLR-004**: All 20 project types have at least one tool registered
  Covers: REQ-TLR-001
- **TEST-TLR-005**: get_tools() returns defaults from registry
  Covers: REQ-TLR-001
- **TEST-TLR-006**: get_tools() respects verification_tools overrides
  Covers: REQ-TLR-003
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
  Covers: REQ-IMP-006
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
