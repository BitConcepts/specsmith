# Requirements — specsmith

<!-- Existing requirements are tracked in the AEE governance files. This file
     is extended below with requirements for the planned architecture roadmap
     as of the April 2026 research and planning session. -->

## OPS — Typed Execution Layer

- **REQ-OPS-001**: All tool handlers MUST use a typed `ProjectOperations` class for file, git/VCS, and search operations. Direct raw shell string assembly in tool handlers is prohibited.
- **REQ-OPS-002**: `ProjectOperations` MUST expose file operations (`read_file`, `write_file`, `list_dir`, `glob`, `search`) implemented via Python `pathlib`/`stdlib` — no subprocess calls.
- **REQ-OPS-003**: `ProjectOperations` MUST expose git/VCS operations (`status`, `log`, `diff`, `add`, `commit`, `push`, `create_branch`, `create_pr`) returning structured result objects.
- **REQ-OPS-004**: All `ProjectOperations` methods MUST return a typed result containing at minimum `exit_code`, `stdout`, `stderr`, and `elapsed_ms`.
- **REQ-OPS-005**: The existing `executor.py` `run_tracked()` function MUST be preserved as a narrow fallback for commands that have no Python equivalent. It MUST NOT be used for routine file, git, or search actions.
- **REQ-OPS-006**: `ProjectOperations` MUST be cross-platform (Windows, Linux, macOS) without platform-specific code branches in call sites.

## CMD — Harness Commands

- **REQ-CMD-001**: The `commands/` package MUST implement all priority harness slash commands available inside `specsmith run`.
- **REQ-CMD-002**: Session management commands MUST include: `/model <name>`, `/provider <name>`, `/tier <fast|balanced|powerful>`, `/status`, `/save`, `/clear`, `/compact`, `/export`.
- **REQ-CMD-003**: Multi-agent commands MUST include: `/spawn <type> <prompt>`, `/team <name>`, `/team-status`, `/worktree`.
- **REQ-CMD-004**: Continuous learning commands MUST include: `/learn [pattern]`, `/learn-eval`, `/instinct-status`, `/instinct-import <file>`, `/instinct-export <file>`.
- **REQ-CMD-005**: Evaluation commands MUST include: `/eval define <feature>`, `/eval run [--trials k]`, `/eval report`, `/eval compare <run1> <run2>`.
- **REQ-CMD-006**: Orchestration commands MUST include: `/multi-plan`, `/multi-execute`, `/route <task>`.
- **REQ-CMD-007**: Hook control commands MUST include: `/hooks-enable <name>`, `/hooks-disable <name>`, `/hook-profile <profile>`.
- **REQ-CMD-008**: MCP commands MUST include: `/mcp-list`, `/mcp-add <server>`, `/mcp-configure <server>`.
- **REQ-CMD-009**: Security commands MUST include: `/security-scan`, `/audit-prompt`.

## MAS — Multi-Agent Spawning

- **REQ-MAS-001**: The runner MUST provide an `AgentTool` (TaskTool) as a native LLM-callable tool that spawns subagent instances. The tool MUST accept: `subagent_type`, `description`, `prompt`, `model`, `run_in_background`, `isolation`, `cwd`.
- **REQ-MAS-002**: Subagent spawning MUST support two coordination modes: hub-and-spoke (parent receives distilled summary; workers cannot communicate) and agent-teams (peer-to-peer via filesystem mailbox).
- **REQ-MAS-003**: The filesystem mailbox for agent teams MUST be stored at `.specsmith/teams/{team}/mailbox/{agent}.json`. No message broker or WebSocket is required between agents.
- **REQ-MAS-004**: When `isolation=worktree`, the spawner MUST create a git worktree at `.specsmith/worktrees/{agent_id}/` to prevent file conflicts during parallel code generation.
- **REQ-MAS-005**: Subagents MUST NOT be able to spawn further subagents (no recursive nesting).
- **REQ-MAS-006**: The parent agent MUST receive a distilled summary message from each subagent on completion, not the full conversation transcript.
- **REQ-MAS-007**: Agent team mode MUST be gated behind a feature flag (`SPECSMITH_AGENT_TEAMS=1`) and display a cost estimate (~7x token multiplier) in the spawn confirmation.

## ORC — Orchestrator Meta-Agent

- **REQ-ORC-001**: specsmith MUST provide an orchestrator meta-agent whose sole purpose is task classification, routing, and optimization — not task execution.
- **REQ-ORC-002**: The orchestrator MUST default to a small local Ollama model (e.g. `qwen2.5:7b` or `llama3.2:3b`) so orchestration itself incurs zero cloud API cost.
- **REQ-ORC-003**: The orchestrator MUST maintain an agent registry with fields: `type`, `model`, `provider`, `cost_tier`, `capabilities`, `avg_latency_ms`, `confidence`.
- **REQ-ORC-004**: The orchestrator MUST classify each incoming task using heuristics and emit exactly one structured next-action: `{action: call_agent|call_tool|ask_user|finish, agent_type, model, rationale}`.
- **REQ-ORC-005**: The orchestrator MUST route cheap/simple tasks to Ollama workers and complex/critical tasks to cloud providers based on cost-tier classification.
- **REQ-ORC-006**: The orchestrator MUST run a post-session self-evaluation to update routing thresholds based on observed latency and quality.

## FLG — Feature Flag System

- **REQ-FLG-001**: specsmith MUST implement a feature-flag system that controls which tool schemas are sent to the LLM. When a flag is off, the tool definition is not included in the LLM call; the model cannot call or hallucinate the gated tool.
- **REQ-FLG-002**: Feature flags MUST be configurable via environment variables (`SPECSMITH_FLAG_<NAME>=1`) and via `scaffold.yml` under `agent.flags`.
- **REQ-FLG-003**: The following capabilities MUST be flag-gated: agent teams, worktree isolation, KAIROS daemon mode, security scanner, MCP tools.

## LRN — Instinct / Continuous Learning System

- **REQ-LRN-001**: specsmith MUST implement an instinct persistence system in `src/specsmith/instinct.py` that stores reusable session patterns at `.specsmith/instincts.json`.
- **REQ-LRN-002**: Each instinct record MUST contain: `id`, `trigger_pattern`, `content`, `confidence` (0.0–1.0), `project_scope`, `created`, `last_used`, `use_count`.
- **REQ-LRN-003**: The `SESSION_END` hook MUST analyze the session transcript and LEDGER.md to extract candidate instincts for user review.
- **REQ-LRN-004**: The `/learn [pattern]` command MUST promote a pattern to an instinct with an initial confidence score.
- **REQ-LRN-005**: Instinct confidence MUST be updated (upward) each time an instinct is successfully applied, and (downward) when explicitly rejected.
- **REQ-LRN-006**: Instincts MUST be importable and exportable as `.md` files for sharing across projects.
- **REQ-LRN-007**: The `/instinct-status` command MUST display all active instincts sorted by confidence, with last-used date and use count.

## EDD — Eval Harness (Eval-Driven Development)

- **REQ-EDD-001**: specsmith MUST implement an eval harness in `src/specsmith/eval/` implementing Eval-Driven Development (EDD) principles.
- **REQ-EDD-002**: The eval model MUST define: `Task` (single test with success criteria), `Trial` (one agent run on a task), `Grader` (scoring logic), `Transcript` (full record of a trial), `Outcome` (final environment state).
- **REQ-EDD-003**: Tasks MUST be stored as Markdown files at `.specsmith/evals/{feature}.md` with YAML frontmatter.
- **REQ-EDD-004**: The harness MUST support three grader types: `CodeGrader` (deterministic: bash assertion, git-diff check, unit test), `ModelGrader` (LLM-as-judge with rubric), `HumanFlag` (flag for manual review).
- **REQ-EDD-005**: The harness MUST compute and report `pass@k` (at least one success in k trials) and `pass^k` (all k trials succeed) metrics.
- **REQ-EDD-006**: For coding agent tasks, the default grading strategy MUST be git-based outcome grading (`git status --porcelain` + test suite pass), NOT execution-path assertion.
- **REQ-EDD-007**: The `/eval run --trials k` command MUST run k independent trials of a task and report the pass@k / pass^k results.
- **REQ-EDD-008**: The harness MUST distinguish capability evals (start low, hill-climb) from regression evals (target ~100%, run on every change).

## MEM — Agent Memory Persistence

- **REQ-MEM-001**: specsmith MUST implement cross-session agent memory in `src/specsmith/memory.py`, persisting learnings at `.specsmith/agent-memory/{agent_id}/`.
- **REQ-MEM-002**: Agent memory MUST be structured JSON containing: accumulated patterns, preferred approaches, known project facts, and failure history.
- **REQ-MEM-003**: The `SESSION_START` hook MUST load relevant memories from the agent memory store and inject them into the system prompt context (token-budget-aware injection).
- **REQ-MEM-004**: The agent memory storage layout MUST be compatible with Theia AI's `~/.theia/agent-memory/` convention to enable future IDE integration.

## HRK — Hook Runtime Controls

- **REQ-HRK-001**: Hooks MUST be enable/disable-able at runtime via `/hooks-enable <name>` and `/hooks-disable <name>` commands without restarting the session.
- **REQ-HRK-002**: Hook profiles MUST be loadable via `/hook-profile <profile>` where profiles define which hooks are active and their configuration.
- **REQ-HRK-003**: The hook system MUST add the following new triggers: `SUBAGENT_START`, `SUBAGENT_STOP`, `CONTEXT_COMPACT`, `EVAL_PASS`, `EVAL_FAIL`.
- **REQ-HRK-004**: `SUBAGENT_START` MUST fire before any subagent is spawned, receiving the spawn parameters. A hook MAY block the spawn.
- **REQ-HRK-005**: `SUBAGENT_STOP` MUST fire when a subagent completes or is terminated, receiving the distilled summary.
- **REQ-HRK-006**: `CONTEXT_COMPACT` MUST fire before context trimming, allowing a hook to provide custom summarization logic.

## SRV — Service / Daemon

- **REQ-SRV-001**: specsmith MUST provide a `specsmith serve` command that starts a local daemon process owning session lifecycle, event streaming, retrieval, orchestrator state, and agent registry.
- **REQ-SRV-002**: The service MUST expose REST endpoints: `GET/POST /sessions`, `GET /agents`, `GET /instincts`, `GET /evals`, `POST /index`, `GET /health`.
- **REQ-SRV-003**: The service MUST expose a WebSocket endpoint at `/ws/session/{id}` for live session I/O and event streaming using the existing JSONL event schema.
- **REQ-SRV-004**: `AgentRunner._emit_event()` MUST be refactored to use an `EventSink` protocol. Concrete implementations: `StdoutSink` (current behavior), `WebSocketSink` (service mode).
- **REQ-SRV-005**: specsmith-vscode's `bridge.ts` MUST be updated to detect a running `specsmith serve` instance and prefer the WebSocket bridge over the subprocess JSONL bridge.

## RTR — Retrieval Upgrade

- **REQ-RTR-001**: `retrieval.py` MUST be upgraded from term-frequency keyword scoring to proper BM25 ranking using the `rank_bm25` Python package.
- **REQ-RTR-002**: The retrieval index MUST support file-watcher-based refresh using `watchdog` or polling so the index stays current without manual `specsmith index` calls.
- **REQ-RTR-003**: Retrieval results injected into the system prompt MUST be token-counted before injection using `TokenEstimator` to prevent context budget overruns.

## LPR — Local Provider Path

- **REQ-LPR-001**: The `specsmith run` CLI MUST accept a `--base-url` flag that overrides the API base URL for the OpenAI-compatible provider path.
- **REQ-LPR-002**: `scaffold.yml` MUST support an `agent.base_url` field that sets the base URL for local provider calls.
- **REQ-LPR-003**: The existing OpenAI provider's `base_url` support MUST be documented as the path for Jan, LM Studio, vLLM, and llama.cpp — no additional provider class is required.

## MCP — MCP Management

- **REQ-MCP-001**: specsmith MUST provide MCP server configuration templates that can be generated via `/mcp-add <server>` or `specsmith mcp add <server>`.
- **REQ-MCP-002**: The MCP server registry MUST list configured servers with status (running/stopped), their tool surfaces, and their configuration paths.
- **REQ-MCP-003**: MCP configuration MUST be storable in `scaffold.yml` under `agent.mcp_servers` for project-scoped MCP server definitions.

## SEC — Security Scan

- **REQ-SEC-001**: specsmith MUST provide a `/security-scan` command that runs a dedicated security analysis agent against the project.
- **REQ-SEC-002**: The security scan MUST check for: dependency vulnerabilities (via `pip-audit` or equivalent), OWASP-style code patterns (via `bandit` or equivalent), and exposed secrets in committed files.
- **REQ-SEC-003**: The `/audit-prompt` command MUST analyze a given prompt string for prompt injection vectors and adversarial instruction patterns.
- **REQ-SEC-004**: Security scan results MUST be structured (severity, file:line, description, remediation) and stored at `.specsmith/security-reports/`.

## IDE — Theia IDE Application

- **REQ-IDE-001**: A `specsmith-ide` application MUST be created as a new repository, scaffolded on Eclipse Theia with `@theia/ai-core`, `@theia/ai-chat`, and `@theia/ai-ide` as base packages.
- **REQ-IDE-002**: `specsmith-ide` MUST ship specsmith-specific Theia extensions: `@specsmith/ai-agents` (AEE orchestrator, epistemic-auditor, instinct-extraction, eval-designer chat agents), `@specsmith/epistemic-ui` (belief graph panel, H13 gate panel, ledger browser, instinct registry), `@specsmith/eval-ui` (eval suite browser, trial runner, pass@k dashboard), `@specsmith/service-client` (WebSocket connection to `specsmith serve`).
- **REQ-IDE-003**: `specsmith-ide` MUST connect to a running `specsmith serve` instance over WebSocket for all session I/O and event streaming.
- **REQ-IDE-004**: `specsmith-ide` MUST leverage Theia AI's existing MCP support, ShellExecutionTool, agent skills system, and configuration view rather than reimplementing them.
- **REQ-IDE-005**: `specsmith-ide` MUST be packageable as an Electron desktop application for Windows, Linux, and macOS.
