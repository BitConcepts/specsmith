# Requirements — specsmith

## CLI

- **REQ-CLI-001**: `specsmith init` scaffolds a governed project from interactive prompts or YAML config
- **REQ-CLI-002**: `specsmith audit` runs health and drift checks against a governed project
- **REQ-CLI-003**: `specsmith validate` checks governance file consistency (req ↔ test ↔ arch)
- **REQ-CLI-004**: `specsmith compress` archives old ledger entries when LEDGER.md exceeds threshold
- **REQ-CLI-005**: `specsmith upgrade` regenerates governance files for a newer spec version
- **REQ-CLI-006**: All commands accept `--project-dir` to target a specific project root
- **REQ-CLI-007**: `specsmith --version` displays the current version
- **REQ-CLI-008**: `specsmith import` detects an existing project and generates governance overlay
- **REQ-CLI-009**: `specsmith init --guided` runs interactive architecture definition session
- **REQ-CLI-010**: `specsmith status` shows CI status, alerts, and PRs from VCS platform CLI
- **REQ-CLI-011**: `specsmith diff` compares governance files against spec templates
- **REQ-CLI-012**: `specsmith export` generates compliance report with REQ coverage matrix, audit summary, tool status
- **REQ-CLI-013**: `specsmith import --guided` runs architecture definition after import detection

## Scaffolding

- **REQ-SCF-001**: Scaffolder generates all governance files (AGENTS.md, LEDGER.md, modular docs)
- **REQ-SCF-002**: Scaffolder generates project-type-specific files (pyproject.toml for Python, etc.)
- **REQ-SCF-003**: Scaffolder creates .gitkeep files in expected empty directories
- **REQ-SCF-004**: Scaffolder optionally runs `git init` in the target directory
- **REQ-SCF-005**: Scaffolder saves scaffold.yml config for re-runs and upgrades
- **REQ-SCF-006**: Scaffolder generates agent integration files based on config.integrations list

## Configuration

- **REQ-CFG-001**: ProjectConfig validates scaffold.yml input with pydantic
- **REQ-CFG-002**: ProjectConfig supports 30 project types covering Python, Rust, Go, C/C++, JS/TS, .NET, mobile, DevOps, data/ML, microservices, documents, business, legal, and project management
- **REQ-CFG-003**: ProjectConfig derives package_name from project name (hyphen → underscore)
- **REQ-CFG-004**: ProjectConfig supports verification_tools overrides per tool category
- **REQ-CFG-005**: ProjectConfig stores detected_build_system and detected_test_framework from import

## Audit

- **REQ-AUD-001**: Audit checks for required governance files (AGENTS.md, LEDGER.md)
- **REQ-AUD-002**: Audit checks modular governance files when AGENTS.md exceeds 200 lines
- **REQ-AUD-003**: Audit checks REQ ↔ TEST coverage consistency
- **REQ-AUD-004**: Audit checks ledger size against threshold (default 500 lines)
- **REQ-AUD-005**: Audit checks open TODO count in ledger
- **REQ-AUD-006**: Audit checks governance file sizes against bloat thresholds
- **REQ-AUD-007**: Audit checks CI config references expected verification tools for project type
- **REQ-AUD-008**: `audit --fix` generates missing CI configs from tool registry

## Validation

- **REQ-VAL-001**: Validate checks scaffold.yml structure and required fields
- **REQ-VAL-002**: Validate checks AGENTS.md local file references resolve
- **REQ-VAL-003**: Validate checks requirement ID uniqueness
- **REQ-VAL-004**: Validate checks architecture.md references requirements

## Compression

- **REQ-CMP-001**: Compress archives entries older than keep_recent threshold
- **REQ-CMP-002**: Compress writes archived entries to docs/ledger-archive.md
- **REQ-CMP-003**: Compress only runs when ledger exceeds line threshold

## Upgrade

- **REQ-UPG-001**: Upgrade reads scaffold.yml for current config
- **REQ-UPG-002**: Upgrade re-renders governance templates with new spec version
- **REQ-UPG-003**: Upgrade updates scaffold.yml with new spec version

## Integrations

- **REQ-INT-001**: Warp adapter generates .warp/skills/SKILL.md
- **REQ-INT-002**: Claude Code adapter generates CLAUDE.md
- **REQ-INT-003**: Cursor adapter generates .cursor/rules/governance.mdc
- **REQ-INT-004**: Copilot adapter generates .github/copilot-instructions.md
- **REQ-INT-005**: Adapter registry allows listing and instantiating adapters by name

## Tool Registry

- **REQ-TLR-001**: Tool registry maps each project type to lint, typecheck, test, security, build, format, and compliance tools
- **REQ-TLR-002**: Tool registry provides CI metadata per language (GitHub Actions setup, Docker images, cache keys)
- **REQ-TLR-003**: Tool registry supports user overrides via verification_tools config field
- **REQ-TLR-004**: Format tools have CI check-mode equivalents (e.g., ruff format → ruff format --check)

## Import

- **REQ-IMP-001**: Importer detects primary language from file extension counts
- **REQ-IMP-002**: Importer detects build system from marker files (pyproject.toml, Cargo.toml, etc.)
- **REQ-IMP-003**: Importer detects test framework from indicator files
- **REQ-IMP-004**: Importer detects existing CI and VCS platform
- **REQ-IMP-005**: Importer detects existing governance files and modules/entry points
- **REQ-IMP-006**: Importer infers correct ProjectType from detection results
- **REQ-IMP-007**: Overlay generation creates AGENTS.md, LEDGER.md, REQUIREMENTS.md, TEST_SPEC.md, architecture.md
- **REQ-IMP-008**: Overlay generation skips existing files unless --force is specified

## VCS Platforms

- **REQ-VCS-001**: GitHub, GitLab, and Bitbucket platforms generate tool-aware CI configs from the registry
- **REQ-VCS-002**: CI config generation supports all 30 project types with correct tool commands
- **REQ-VCS-003**: Dependabot/Renovate config uses correct package ecosystem per language
- **REQ-VCS-004**: Mixed-language projects (e.g., Python+JS) get multi-runtime CI setup

## Export

- **REQ-EXP-001**: Export generates project summary from scaffold.yml
- **REQ-EXP-002**: Export generates REQ↔TEST coverage matrix with percentage
- **REQ-EXP-003**: Export includes audit summary with pass/fail/fixable counts
- **REQ-EXP-004**: Export includes governance file inventory
- **REQ-EXP-005**: Export supports --output flag for file output

## Templates

- **REQ-TPL-001**: Governance templates include type-specific verification tool listings
- **REQ-TPL-002**: Requirements template generates domain-specific starters (patent, legal, business, API, research)
- **REQ-TPL-003**: Test spec template generates domain-specific test stubs
- **REQ-TPL-004**: Architecture template includes verification tools section

## Git VCS Commands

- **REQ-GIT-001**: specsmith commit generates message from last ledger entry
- **REQ-GIT-002**: specsmith commit refuses if LEDGER.md not updated since last commit
- **REQ-GIT-003**: specsmith commit runs audit as pre-commit validation
- **REQ-GIT-004**: specsmith push pushes current branch with safety checks
- **REQ-GIT-005**: specsmith push refuses direct push to main from feature branches
- **REQ-GIT-006**: specsmith branch create enforces naming and base branch per strategy
- **REQ-GIT-007**: specsmith branch list shows branches with strategy context
- **REQ-GIT-008**: specsmith pr generates PR with governance summary in description
- **REQ-GIT-009**: specsmith pr sets correct base branch per branching strategy
- **REQ-GIT-010**: specsmith sync pulls and warns on governance file conflicts

## Self-Update and Migration

- **REQ-UPD-001**: specsmith update checks PyPI for newer version and reports comparison
- **REQ-UPD-002**: specsmith update --yes installs latest version without confirmation
- **REQ-UPD-003**: specsmith update triggers migrate-project after successful update
- **REQ-UPD-004**: specsmith migrate-project compares scaffold.yml spec_version to installed version
- **REQ-UPD-005**: specsmith migrate-project regenerates governance templates for new version
- **REQ-UPD-006**: specsmith migrate-project reports deprecated features and breaking changes
- **REQ-UPD-007**: specsmith migrate-project --dry-run shows changes without writing
- **REQ-UPD-008**: Agent adapter files instruct agent to run update --check at session start
- **REQ-UPD-009**: specsmith migrate-project appends migration entry to LEDGER.md
- **REQ-UPD-010**: specsmith migrate-project preserves all existing REQs, TESTs, and ledger entries

## Workflow Logic

- **REQ-WFL-001**: Agent proposes commit after successful verification + ledger save
- **REQ-WFL-002**: Agent proposes push before session end if unpushed commits exist
- **REQ-WFL-003**: Agent refuses to work on main/develop directly for gitflow projects
- **REQ-WFL-004**: Agent proposes branch creation when starting a new task
- **REQ-WFL-005**: Agent proposes PR when feature branch TODOs are complete and audit passes
- **REQ-WFL-006**: Agent runs sync at session start before any work
- **REQ-WFL-007**: Agent runs update --check at session start and proposes update if outdated
- **REQ-WFL-008**: Agent checks current branch matches task type (feature vs hotfix vs release)
- **REQ-WFL-009**: specsmith commit --auto-push option to commit and push in one step
- **REQ-WFL-010**: specsmith session-end provides checklist (unpushed commits, open TODOs, dirty files)

## Cross-Platform

- **REQ-XPL-001**: All CLI commands work on Windows, Linux, and macOS
- **REQ-XPL-002**: Generated scripts include both .cmd and .sh variants
