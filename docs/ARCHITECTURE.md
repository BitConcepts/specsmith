# Architecture — specsmith

## Overview

specsmith is an Applied Epistemic Engineering (AEE) toolkit targeting Windows, Linux, macOS. It scaffolds epistemically-governed projects, stress-tests requirements as BeliefArtifacts, runs cryptographically-sealed trace vaults, and orchestrates AI agents under formal AEE governance. Supports 33 project types (see REQ-CFG-002).

## Components

### CLI (`cli.py`)
Entry point. Click-based command group with 50+ commands (see REQ-CLI-001 through REQ-CLI-013). Includes: scaffold/governance commands, AEE commands (`stress-test`, `epistemic-audit`, `belief-graph`, `trace`, `integrate`), agentic client (`run`, `agent`), and extended commands (`auth`, `workspace`, `watch`, `patent`).

### Config (`config.py`)
Pydantic model validating scaffold.yml (see REQ-CFG-001). 33 project types enum (see REQ-CFG-002), platform enum, type labels, section refs. AEE fields: `enable_epistemic`, `epistemic_threshold`, `enable_trace_vault`.

### Scaffolder (`scaffolder.py`)
Jinja2 template renderer (see REQ-SCF-001 through REQ-SCF-006). Generates governance files, project structure, scripts. Delegates to VCS platforms and agent integrations. Epistemic governance templates for AEE project types (see REQ-SCF-EPI-001).

### Tool Registry (`tools.py`)
Data structure mapping 33 project types to verification tools (see REQ-TLR-001 through REQ-TLR-004). CI metadata per language (see REQ-TLR-002).

### Importer (`importer.py`)
Detection engine: walks directories, detects language/build/test/CI/governance (see REQ-IMP-001 through REQ-IMP-006). Infers ProjectType. Generates overlay files with cross-linked TEST/REQ stubs (see REQ-IMP-007).

### Exporter (`exporter.py`)
Generates compliance reports: REQ coverage matrix, audit summary, tool status, governance inventory (see REQ-EXP-001 through REQ-EXP-005).

### Auditor (`auditor.py`)
Health checks: file existence, REQ↔TEST coverage (see REQ-AUD-001 through REQ-AUD-008), ledger health, governance size, tool configuration, trace chain integrity.

### VCS Platforms (`vcs/`)
GitHub, GitLab, Bitbucket integrations (see REQ-VCS-001 through REQ-VCS-004). Tool-aware CI config generation, dependency management, status checks.

### Agent Integrations (`integrations/`)
7 adapters: Warp, Claude Code, Cursor, Copilot, Gemini, Windsurf, Aider (see REQ-INT-001 through REQ-INT-005).

## Epistemic Layer (`src/epistemic/` + `src/specsmith/agent/`)

### `epistemic` package (standalone library, zero deps)
Co-installed with specsmith. Canonical location for all AEE machinery.
- **`belief.py`** — `BeliefArtifact` dataclass (propositions, boundary, confidence, status, failure_modes, evidence)
- **`stress_tester.py`** — `StressTester` applies 8 adversarial challenge categories; emits `FailureMode` records; detects Logic Knots
- **`failure_graph.py`** — `FailureModeGraph` directed graph; `equilibrium_check()` and `logic_knot_detect()`; Mermaid rendering
- **`recovery.py`** — `RecoveryOperator` emits bounded `RecoveryProposal` objects; never auto-applies; ranked by severity
- **`certainty.py`** — `CertaintyEngine` scores C = base × coverage × freshness; weakest-link propagation through inferential links
- **`session.py`** — `AEESession` facade: `add_belief`, `accept`, `add_evidence`, `run`, `save`, `load`, `seal`
- **`trace.py`** — `TraceVault` SHA-256 append-only chain; STP-inspired decision sealing

### `specsmith.epistemic` (compatibility shim)
Re-exports all symbols from `epistemic`. Allows `from specsmith.epistemic import BeliefArtifact` for backward compat.

### Crypto Audit Chain (`ledger.py`)
`CryptoAuditChain` stores SHA-256 hashes per ledger entry in `.specsmith/ledger-chain.txt`. Each hash chains to the previous, making the ledger tamper-evident.

### Agentic Client (`src/specsmith/agent/`)
- **`core.py`** — `Message`, `Tool`, `CompletionResponse`, `ModelTier`, `BaseProvider` protocol
- **`providers/`** — Anthropic, OpenAI (+ Ollama via compat), Gemini, Ollama (stdlib-only). All optional extras.
- **`tools.py`** — 20 specsmith commands as native LLM-callable tools with epistemic contracts
- **`hooks.py`** — `HookRegistry` with Pre/PostTool, SessionStart, SessionEnd. Built-in H13 check.
- **`skills.py`** — SKILL.md loader with domain priority order
- **`runner.py`** — REPL loop, tool execution, streaming, session state, model routing
- **`profiles/`** — Built-in skill profiles: planner, verifier, epistemic-auditor

## GUI Workbench (`src/specsmith/gui/`)

PySide6 (Qt6) desktop application launched via `specsmith gui` (see REQ-GUI-001 through REQ-GUI-013).

- **`app.py`** — `QApplication` bootstrap, dark AEE theme (deep-navy/teal/amber), `launch()` entry point
- **`main_window.py`** — `MainWindow`: `QTabWidget` with new-session dialog, global status bar, menu bar
- **`session_tab.py`** — per-tab widget: assembles chat view, input bar, token meter, tool panel, provider bar
- **`worker.py`** — `GUIAgentRunner(AgentRunner)` overrides `_print`/`_call_provider`/`_execute_tool_calls` to emit Qt signals; `AgentWorker(QThread)` runs agent turns off the UI thread
- **`theme.py`** — QSS stylesheet: `#0d1117` background, teal accents, amber warnings
- **`widgets/chat_view.py`** — `QTextBrowser` with HTML message rendering per role
- **`widgets/input_bar.py`** — `QPlainTextEdit` + Send/File/URL buttons + drag-drop accept
- **`widgets/token_meter.py`** — `QProgressBar` (green→yellow→red at 70%/90%) + cost label
- **`widgets/tool_panel.py`** — collapsible sidebar with `QToolButton`s per specsmith tool
- **`widgets/provider_bar.py`** — `QComboBox` for provider and model selection
- **`widgets/update_checker.py`** — `QThread` that checks PyPI on startup and silently upgrades

## Verification Tools

**Lint:** ruff check
**Typecheck:** mypy
**Test:** pytest
**Security:** pip-audit
**Format:** ruff format

---

## Planned Architecture Evolution (April 2026 Roadmap)

The following components are planned based on the comprehensive gap analysis and research session of April 10, 2026. They are documented here as architectural commitments before implementation begins. See `docs/REQUIREMENTS.md` for formal requirements.

### Phase 1 — Core Harness Depth

#### `src/specsmith/operations.py` — Typed Project Operations
A `ProjectOperations` class providing typed, cross-platform file, git, and search operations. All tool handlers in `agent/tools.py` will be refactored to use this class instead of raw shell strings.
- File ops via `pathlib`/`stdlib` (no subprocess): `read_file`, `write_file`, `list_dir`, `glob`, `search`
- Git ops via structured wrappers: `status`, `log`, `diff`, `add`, `commit`, `push`, `create_branch`, `create_pr`
- All methods return `OperationResult(exit_code, stdout, stderr, elapsed_ms, metadata)`
- `executor.py`'s `run_tracked()` retained as narrow escape hatch only

#### `src/specsmith/commands/` — Harness Commands Surface
Populates the currently empty `commands/__init__.py` with the full harness slash command set. Commands are registered as REPL meta-commands in `AgentRunner._handle_meta_command()`. Priority set: `/model`, `/tier`, `/spawn`, `/learn`, `/instinct-status`, `/eval define`, `/eval run`, `/hooks-enable`, `/hooks-disable`, `/mcp-list`, `/security-scan`.

#### `src/specsmith/instinct.py` — Continuous Learning / Instinct System
Persists reusable session patterns as instincts at `.specsmith/instincts.json`.
- `Instinct` dataclass: `{id, trigger_pattern, content, confidence, project_scope, created, last_used, use_count}`
- `InstinctRegistry`: load/save/search/promote/demote instincts
- Session-end hook (`SESSION_END`) calls `InstinctExtractor` to analyze transcript and LEDGER.md for candidate patterns
- `/learn` promotes a candidate; confidence updated on each application
- Import/export to `.md` format for cross-project sharing

#### `src/specsmith/eval/` — Eval Harness (EDD Framework)
Implements Eval-Driven Development as a first-class specsmith feature.
- `task.py`: `Task`, `Trial`, `Transcript`, `Outcome` dataclasses; stored as `.specsmith/evals/{feature}.md`
- `graders.py`: `CodeGrader` (git-diff + test pass), `ModelGrader` (LLM-as-judge rubric), `HumanFlag`
- `harness.py`: `EvalHarness` runs k independent trials, computes `pass@k` and `pass^k`
- `metrics.py`: `PassAtK`, `PassHatK` metric objects with statistical summaries
- Default grading strategy: git-based outcome (assert files changed + tests pass), not execution-path assertion

### Phase 2 — Multi-Agent Layer

#### `src/specsmith/agent/spawner.py` — AgentTool / Subagent Spawning
The single tool that spawns all subagent instances. Modeled on the Claude Code `AgentTool` architecture revealed by the March 2026 source map leak.
- `SpawnParams`: `{subagent_type, description, prompt, model, run_in_background, isolation, cwd}`
- `SubagentLifecycle`: manages spawn, wait-for-completion, collect summary, teardown
- Isolation modes: `none` (shared filesystem), `worktree` (dedicated git worktree at `.specsmith/worktrees/{id}/`)
- Fires `SUBAGENT_START` hook before spawn (may block); `SUBAGENT_STOP` hook on completion
- Subagents CANNOT spawn further subagents (prevents recursive nesting)

#### `src/specsmith/agent/teams.py` — Agent Team Coordination
Peer-to-peer multi-agent coordination via filesystem mailbox (no message broker required).
- Mailbox path: `.specsmith/teams/{team}/mailbox/{agent}.json`
- `TeamMailbox`: `send(agent, message)`, `receive(agent)`, `broadcast(team, message)`
- `TeamTaskList`: shared task list at `.specsmith/teams/{team}/tasks.json` with statuses and dependencies
- `SendMessage` tool: agent-callable tool for peer communication
- Gated behind `SPECSMITH_AGENT_TEAMS=1` feature flag; cost warning (~7x token multiplier) shown at team creation

#### `src/specsmith/agent/orchestrator.py` — Orchestrator Meta-Agent
Meta-agent whose sole purpose is orchestration and cost optimization. Runs on a small local Ollama model.
- `AgentRegistry`: `{type, model, provider, cost_tier, capabilities, avg_latency_ms, confidence}` per agent type
- `TaskClassifier`: heuristic keyword + length scoring (extends `optimizer.py`'s `ModelRouter`)
- Emits one structured next-action per turn: `{action, agent_type, model, rationale}`
- Routes cheap tasks to Ollama workers; complex tasks to cloud providers
- Post-session self-evaluation updates routing confidence thresholds

#### `src/specsmith/agent/flags.py` — Feature Flag System
Controls tool schema visibility. When a flag is off, the tool definition is not sent to the LLM — the model cannot call or hallucinate gated tools.
- `FeatureFlags`: loaded from env vars (`SPECSMITH_FLAG_<NAME>=1`) and `scaffold.yml` `agent.flags`
- `filter_tools_by_flags(tools, flags)`: removes gated tool schemas before LLM call
- Gated capabilities: `AGENT_TEAMS`, `WORKTREE_ISOLATION`, `KAIROS_DAEMON`, `SECURITY_SCANNER`, `MCP_TOOLS`

#### `src/specsmith/memory.py` — Agent Memory Persistence
Cross-session agent learning storage.
- Persists at `.specsmith/agent-memory/{agent_id}/memory.json`
- Fields: `accumulated_patterns`, `preferred_approaches`, `known_project_facts`, `failure_history`
- `SESSION_START` hook loads relevant memories and injects into system prompt (token-budget-aware)
- Compatible with Theia AI's `~/.theia/agent-memory/` convention

#### New Hook Triggers
Added to `HookTrigger` enum in `agent/hooks.py`:
- `SUBAGENT_START` — before subagent spawn (can block)
- `SUBAGENT_STOP` — on subagent completion with summary
- `CONTEXT_COMPACT` — before context trimming (custom summarization hook)
- `EVAL_PASS` / `EVAL_FAIL` — after each eval trial

### Phase 3 — Service + IDE

#### `src/specsmith/server/` — Daemon Service
`specsmith serve` starts a local HTTP+WebSocket server.
- `server/__init__.py`: FastAPI or aiohttp app bootstrap
- `server/routes.py`: REST endpoints `/sessions`, `/agents`, `/instincts`, `/evals`, `/index`, `/health`
- `server/ws.py`: WebSocket handler at `/ws/session/{id}`
- `EventSink` protocol: `StdoutSink` (current), `WebSocketSink` (service mode)
- `AgentRunner._emit_event()` refactored to use `EventSink`

#### `specsmith-ide/` — Theia-Based IDE (new repo)
Built on Eclipse Theia 1.68+ with `@theia/ai-core`, `@theia/ai-chat`, `@theia/ai-ide`.
Specsmith-specific Theia extensions:
- `@specsmith/ai-agents`: AEE orchestrator, epistemic-auditor, instinct-extraction, eval-designer — as Theia chat agents with `AbstractStreamParsingChatAgent`
- `@specsmith/epistemic-ui`: belief graph panel (Mermaid rendering), H13 gate workflow panel, ledger browser, instinct registry panel
- `@specsmith/eval-ui`: eval suite browser, trial runner, pass@k / pass^k dashboard
- `@specsmith/service-client`: WebSocket client to `specsmith serve`
Theia provides natively: LLM communication, agent framework, SKILL.md skills system, MCP support, ShellExecutionTool, AI configuration view, agent memory directories. These are NOT reimplemented.

### Multi-Agent Coordination Patterns

Three tiers, modeled on the Claude Code architecture:

**Tier 1 — Subagent (hub-and-spoke):**
- Parent spawns read-only research workers via `AgentTool`
- Workers return distilled summary; parent never sees full exploration context
- Workers cannot communicate with siblings
- Cost: ~3x. Best for: codebase exploration, parallel research, context isolation

**Tier 2 — Agent Teams (peer-to-peer):**
- Persistent teammates with independent context windows and full tool access
- Communicate via filesystem mailbox (simple, debuggable, no infrastructure)
- Shared task list with statuses and dependencies
- Cost: ~7x. Best for: full-stack features with cross-layer interdependencies
- Requires `SPECSMITH_AGENT_TEAMS=1` flag

**Tier 3 — Orchestrator-worker:**
- Orchestrator meta-agent on Ollama classifies tasks and routes to workers
- Explicit model selection per worker (Ollama for cheap, cloud for complex)
- Near-zero orchestration cost
- Best for: automated multi-step pipelines with cost optimization

### Eval Harness Design Principles

- **EDD (Eval-Driven Development)**: define evals BEFORE writing code. Evals are the unit tests of AI development.
- **Grade outcomes, not paths**: assert that the git working tree changed correctly and tests pass, not that the agent used a specific sequence of tool calls.
- **pass@k vs pass^k**: pass@k (any success in k trials) measures capability ceiling; pass^k (all k succeed) measures reliability floor. Choose based on deployment context.
- **Three grader types**: CodeGrader (deterministic, fast, cheap), ModelGrader (LLM-as-judge, flexible), HumanFlag (gold standard, for calibration).
- **Capability vs regression**: capability evals start with low pass rates and hill-climb; regression evals target ~100% and run on every change.

### Architecture Invariants

- Orchestrator MUST run on local Ollama — never spend cloud credits on routing
- Subagents MUST be read-only (research) workers — implementation stays in the parent session
- Filesystem mailbox for all agent communication — no message brokers
- Feature flags MUST remove tool schemas from LLM calls — not just block execution
- EventSink abstraction MUST preserve existing JSONL event schema — only transport changes
- All `ProjectOperations` calls MUST be cross-platform — no platform branches in call sites
- Instinct extraction MUST be user-reviewed before promotion — never auto-apply instincts
- Eval grading MUST measure outcomes (git state + test results) — not execution paths
