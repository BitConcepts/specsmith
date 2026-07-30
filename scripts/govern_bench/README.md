# govern_bench — GovernanceBench (specsmith)

GovernanceBench measures how governance/scaffolding changes **cost, quality, and safety**
across coding-agent workflows.

> Status: the current GPT-5.6 Sol screen is split across complete matched runs
> `29963772623` and `29963515885` at commit `f474bb6`. Across eight tasks and
> five repetitions per cell, Cursor rules passed 34/40 at 33.8k TPCA;
> Specsmith FULL passed 40/40 at 9.0k TPCA.

Managed Qwen runs are diagnostic-only. Hosted Qwen3-Coder-30B atomic-patch
workflows `30317439173`, `30317963475`, and `30318295306` all failed T28.
Scoping reduced failure tokens from 123,384 to 34,892, while required tool
choice regressed to 81,648 and exposed a repeated action-batch loop. No row is
promotion evidence.

Workflow `30317300977` first pinned a dedicated FP8 vLLM route with
`--enable-auto-tool-choice --tool-call-parser qwen3_xml`, bounded deployment,
request, and cell deadlines, zero provider retries, an exact tool probe, and
cleanup, but was censored by missing endpoint-write permission. After that
permission was corrected, workflows `30358919239` and `30359943752` proved the
literal parser and clean deletion. Atomic, scoped, and globally required-tool
T28/FULL cells all failed at 34,146, 53,451, and 181,884 tokens. The native
parser is therefore compatible, but none of these controller policies is ready
for repetition or a substitution claim.

Trace-derived milestone-packet workflows `30367659754`, `30369089983`, and
`30370203101` also remained incorrect. Packet-only and one-turn-adaptive cells
used 108,021 and 112,933 tokens. Independent-validator authority plus
repair-only atomic patches reduced the failed diagnostic to 18,646 tokens and
five turns, but completed only one of four milestones. Requiring subsequent
repeated repairs regressed to 98,679 tokens. The controller now records
milestone yield and stops an identical single-action no-op after one recovery;
no additional paid repetition is admitted.

The native Responses family screen is now complete. Sol passed T28/FULL at n=1 in
workflow `30412677765` using 18,474 tokens and $0.2590. Terra then passed at
n=1 in `30412913235` and earned the matched n=5 screen `30413249488`: 5/5
correct, 17,213 mean tokens, $0.1176 mean cost, five turns, all four milestones,
and no deterministic audit weakness. Luna's initial workflow `30414435928`
failed at 72,880 tokens and 20 turns because fourteen `write_milestone` calls
carried non-string content. Provider-strict schemas then made `30415300896`
correct at 18,798 tokens and five turns. Its n=5 screen `30415451446` remained
5/5 correct, but averaged 31,685 tokens, 6.2 turns, and only 40% first-pass
completion. These are route-screening results, not a release claim. Terra must
expand to n=10 before this route supports release-quality claims.

All native cells retain the validator-authority, milestone-packet, repair-only
atomic-patch controller, low reasoning effort, low text verbosity, bounded
requests, zero provider retries, and a two-step live tool/continuation probe.
History compaction invalidates `previous_response_id` continuation and forces a
full auditable request. Authoritative packet paths are excluded from optional
generic preload context so a file body cannot be duplicated or retained after
the active milestone advances. Fixed milestone and atomic-patch slots are
provider-strict: every slot is present, unused slots are null, and used content
must be text. The isolated v3 admission `30416984775` stayed correct at 19,288
tokens and five turns with one provider-visible schema hash, but regressed 10%
above the release anchor and was blocked from repetition. Its trace showed
strict fixed/null slots adding input overhead on every turn. Structured v4
replaced those eight slots with one bounded strict `{path, content}` array and
passed admission `30417839826`, n=5 screen `30418033123`, and independent n=10
confirmation `30418513274`. The final ten rows were 10/10 correct and
first-pass at 17,907 mean TPCA, five turns, 1.77% CV, and one schema hash per
row. The audit reports no correctness or efficiency blocker.

Fresh-repository T29 then exposed a public/hidden empty-state mismatch and an
audit parser that misattributed `import "./styles.css"` as the repair target.
Versioned v5 aligns the structural empty-state rule, validates focus,
disabled-action, and responsive CSS at milestone three on a CSS-only boundary,
and fail-closes after two unchanged repair streaks. Admission `30453721376`
passed first-pass at 17,407 tokens. The earned n=5 `30454018932` passed 5/5 at
18,055 mean TPCA, $0.1199 mean cost, 5.2 turns, 80% first-pass, and zero loop
recoveries. Independent n=10 `30457360342` passed 10/10 at 20,100 mean TPCA,
$0.1277 mean cost, 5.7 turns, and 9.8% CV, but first-pass fell to 30%. Six
rows repaired a missing Playwright visibility assertion and one repaired an
invalid model-authored pytest assertion. The audit selects
`optimize_and_rerun`, so this is exact-route, synthetic release-sized evidence
rather than a clean promotion or real-repository claim. Observed patch receipts
attribute the recurring hotspot to `ui/tests/release-control.spec.ts` in 6/10
rows. Versioned v6 makes that existing visibility criterion explicit in
milestone three. Admission `30545048843` passed first-pass at 17,373 tokens;
n=5 `30545401727` passed 5/5 at 18,734.4 TPCA, 60% first-pass, and zero UI
repairs. Two milestone-one Python toolchain repairs remained. V7 makes those
constraints explicit: admission `30546766992`, n=5 `30546999004`, and n=10
`30547516220` all passed every row first-pass. The n=10 confirmation used
17,589.9 TPCA, $0.120940 mean cost, five turns, and 1.62% sample CV; the audit
selects `publish_or_expand`.

The subsequent open-model hybrid experiment is negative evidence. Versioned
`scalar-parallel-hybrid-v1` combined the best Qwen scalar-parallel construction
interface with milestone packets, controller-owned validation, v7 invariants,
and exact-patch recovery. In workflow `30552076420`, Qwen3.6-27B stopped after
one milestone at 20,195 tokens when a 4,096-token completion truncated and the
route returned two empty continuations; Qwen3.6-35B-A3B/DeepInfra timed out
before its first completion. Identical retry `30552754670` timed out in the
35B live probe. V2 changed only Qwen3.6's per-turn allowance to 8,192 tokens.
Workflow `30553392304` then advanced 27B through nine files and eight turns
before a provider timeout at 38,704 tokens. The alternate 35B Scaleway route
completed the Python and Go milestones before a 504 at 11,526 tokens. Both
rows are incomplete infrastructure-affected artifacts, not correctness or
TPCA results; neither earns n=5 and no small-model replacement claim follows.

The final native Qwen3.6-35B-A3B-FP8 lane ran on A100/vLLM `0.24.0` with the
`qwen3_coder` tool parser, `qwen3` reasoning parser, and 65,536-token context.
Both workflows passed exact native tool probes and cleaned up their endpoints.
Generic required-tool workflow `30566266722` failed after 1/4 milestones and
30,287 tokens. Exact named-tool recovery in `30567968596` reached 3/4
milestones but failed at 105,087 tokens and 20 turns after deterministic
sanitation removed 96 duplicate actions. Both are valid failed rows; no n=5
replication is admitted.

---

## Quick Start

```bash
# Install dependencies
pip install pyyaml

# List all tasks and conditions
python -m govern_bench.run_bench --list

# Dry-run (deterministic dummy data, useful for CI and report plumbing)
python -m govern_bench.run_bench --dry-run --reps 5

# Admit a model cheaply before any repeated spend
python -m govern_bench.run_bench --profile admission \
  --provider openai --model gpt-5.6-sol

# Admit the native Responses tool route without changing controller policy
BENCH_CONTROLLER_EXPERIMENT=scalar-milestone-packet-authority \
python -m govern_bench.run_bench --profile admission \
  --provider openai-responses --model gpt-5.6-sol

# Admit controller/tool-schema changes on the affected paths
python -m govern_bench.run_bench --profile controller-admission \
  --provider openai --model gpt-5.6-sol

# Run governance-gate tasks only (T6 + T7)
python -m govern_bench.run_bench --task T6 --task T7 --dry-run

# Real benchmark run (provider/model wiring required)
python -m govern_bench.run_bench --reps 5 --model claude-sonnet-4-5

# Long-horizon product slice; raw JSON automatically creates results.audit.json
python -m govern_bench.run_bench --task T28 --reps 1 \
  --json-output results.json --output long-horizon.md

# Correlate product weaknesses with project governance health
specsmith audit --project-dir . --benchmark-results results.json \
  --report combined-audit.json
```

Each raw-result audit contains a deterministic `next_experiment` decision.
Only `repeat_screen` advances an n=1 diagnostic to five repetitions; correctness
or efficiency findings select a focused repair/optimization rerun, and malformed
or synthetic evidence is rejected.

For a weaker-governed versus stronger-ungoverned experiment, run both models
through the locked `substitution-screen` profile. It produces the complete
raw/FULL 2×2 grid on identical tasks at n=5. Never compare a smaller FULL slice
with an unrelated frontier baseline: without both counterfactual cells, model
capability and governance lift are confounded.

Promote a positive screen through `substitution-release`. It expands the same
2×2 design to all eight versioned tasks at n=10. The comparison report emits
paired fixed-suite and task-cluster bootstrap intervals, applies a five-point
correctness non-inferiority margin, and withholds release claims unless the
upper 95% TPCA-ratio bound is below one.

The paid-run profiles are:

- `admission`: T28/FULL, n=1;
- `controller-admission`: T1/T10/T11/T13/T28/FULL, n=1;
- `release-controls`: T10/T13/T28, Cursor/FULL, n=10;
- `broad-release`: T1/T2/T6/T7/T10/T11/T13/T28, Cursor/FULL, n=10;
- `substitution-screen`: T1/T10/T13/T28, raw/FULL, n=5.
- `substitution-release`: T1/T2/T6/T7/T10/T11/T13/T28, raw/FULL, n=10.

Controller experiments are versioned separately from the task profile through
`BENCH_CONTROLLER_EXPERIMENT` or the workflow's `experiment` input:

- `control`: published composite reads/writes with automatic tool choice;
- `required-tools`: unchanged schema with a required executable tool action;
- `scalar-parallel`: remove nested composite payloads and request parallel
  `write_file` calls;
- `scalar-parallel-required`: combine the prior two changes;
- `scalar-parallel-compact`: also evict completed boundary bodies and
  consolidate write receipts while retaining required tool choice;
- `scalar-parallel-compact-auto`: isolate the same context compaction with
  automatic tool choice;
- `scalar-parallel-write-only`: remove reads during governed implementation
  because the controller already supplies each active boundary's current
  content;
- `scalar-parallel-validator-authority`: prioritize requirement-linked
  independent validator failures over supplementary tests authored by the
  same model run, and expose one repair boundary at a time;
- `scalar-milestone-packet*`: compile only the active milestone's public
  criteria, allowed paths, and current content; compact completed packets and
  record milestone yield. Authority variants isolate independent evidence and
  atomic repair. These are diagnostic cells, not promoted defaults.

Run each causal variant as one `admission` cell on the same commit. Advance a
variant only when the independent oracle passes and correct-answer token cost
materially improves; do not pool cells across controller commits.

Profile task, condition, and repetition counts are locked. Use `custom` only
for explicitly diagnostic work.

---

## Benchmark Scope

### 12 governance conditions

GovernanceBench compares 12 conditions spanning ungoverned baselines, context-only tool
styles, and specsmith governance workflows.

| ID | Condition | Expected Overhead Turns | Family |
|----|-----------|-------------------------|--------|
| `UNGOVERNED` | Raw agent with task prompt only | 0 | Baseline |
| `CONTEXT_ONLY` | Static `CLAUDE.md` / `AGENTS.md` injection | 0 | Context-only |
| `BMAD_STYLE` | BMAD blueprint/milestone scaffolding | 1 | External scaffold |
| `OPENSPEC_STYLE` | OpenSpec-style requirements injection | 0 | External scaffold |
| `SPECSMITH_LIGHT` | `specsmith preflight` gate only | 1 | specsmith |
| `SPECSMITH_FULL` | Full session (`audit → preflight → verify → save`) | 3 | specsmith |
| `CURSOR_RULES` | Cursor `.cursor/rules/*.mdc` style | 0 | Tool-native |
| `COPILOT_INSTRUCTIONS` | GitHub Copilot instructions style | 0 | Tool-native |
| `CODEX_AGENTS_MD` | Codex CLI `AGENTS.md` style | 0 | Tool-native |
| `CLINE_RULES` | Cline `.clinerules` style | 0 | Tool-native |
| `AGILE_TDD` | Test-first (RED→GREEN→REFACTOR) protocol | 1 | Process scaffold |
| `AIDER_CONVENTIONS` | Aider `CONVENTIONS.md` style | 0 | Tool-native |

The former `SPECSMITH_DISPATCH` condition is excluded from the executable
matrix because it simulated dispatch rather than running an equivalent agent
capability. Historical reports label it explicitly and do not carry it into new
comparative claims.

### Multi-domain task suites

Current and planned suites are intentionally cross-discipline to evaluate governance beyond
code-only benchmarks.

| Suite | Task IDs | Domain(s) | Status |
|------|----------|-----------|--------|
| Core suite | `T1`–`T13` | `todo_api`, `cli_tool` | Available |
| Wave 1 expansion | `T14`–`T22` | `todo_api`, `data_pipeline`, `verilog_module`, `patent_draft` | Definitions available; hidden oracles pending |
| Shell hardening suite | `T23`–`T27` | `shell_scripts` | Definitions available; hidden oracles pending |
| Long-horizon product | `T28` | Python API, Go worker, React UI, Playwright, shared schema | Available with hidden oracle |
| Fresh polyglot replication | `T29` | Independent release-control API, Go worker, React UI, schema | Available with hidden oracle |
| Pinned upstream maintenance | `T30` | Pallets ItsDangerous at commit `672971d…`, Python and RST | Available with hidden oracle and file-hash manifest |
| Wave 2 expansion | TBD | `ee_schematic`, `business_requirements`, `regulatory_doc`, `fpga_constraints` | Planned |

Task availability does not imply empirical coverage. Claims must identify the exact
tasks included in the matched run.

The frozen preprint-readiness contract is
`PREPRINT_PROTOCOL_2026_07.yml` (`GB-PREPRINT-2026-07-30-V1`). Its
`publication-matched` profile runs T28, T29, and T30 under raw, Cursor-style,
and Specsmith FULL conditions at n=10. Open routes use separate locked
admission, n=5, and n=10 profiles and advance only after the prior gate passes.
Raw rows and compact manifests carry the protocol digest.

The frozen T30 open-model admission is complete. Qwen3.6-27B, Qwen3-32B, and
Qwen3-Coder-30B produced complete failed cells; GPT-OSS-20B, GLM-4.7-Flash,
and Qwen3.6-35B were censored by their pinned provider routes. No candidate
passed both public and hidden correctness, so no n=5 or n=10 profile was run.
`paper/data/publication-open-admission-status.json` records complete,
censored, superseded-infrastructure, promotion, and expenditure outcomes.

V1 workflow `30578319069` later exposed an impossible T30 hidden invariant:
the byte-identical Pallets license did not contain the literal SPDX label used
by the oracle. Its T30 stratum is invalidated rather than scored. The separately
frozen `GB-PREPRINT-2026-07-30-V2` protocol reruns only corrected T30 under
`publication-real-repository-recovery`; it verifies the license by its pinned
digest, exercises timed and documentation contracts publicly, and requires
every declared milestone boundary before FULL completion.

The current publication-eligible screen is `T1`, `T2`, `T6`, `T7`, `T10`,
`T11`, `T13`, and `T28`. Its coding tasks have evaluator-only acceptance tests that
are injected after the agent stops. A standard task without an oracle fails
closed; clean fixtures and no-op responses cannot count as correct.
Project Ruff and pytest checks run before injection; the oracle then runs once
in its own pytest invocation and is removed before diff construction.

T28 declares a 20-turn task-specific ceiling. Other tasks keep the normal
bounded turn budget. Long-horizon results must be shown separately from the core
screen before any aggregate claim is made.

For standard coding tasks, `SPECSMITH_FULL` also blocks the agent's `done`
request until both `ruff check .` and `pytest` have passed after its latest
file write. T28 additionally requires fresh Go-test, shared-contract, and
deterministic UI-validator evidence, so a Python-only implementation cannot declare success. A failed check
sends the agent back through a repair turn; those turns and tokens remain part of
the measured cost. FULL may apply one Ruff default-safe-fix pass before returning
a lint-only failure; unsafe fixes are never enabled. FULL exposes one compact
five-tool schema for the entire run and records its hash so provider caching
cannot be disrupted by controller phase changes. Requirement-linked files are
preloaded only where versioned task metadata permits it. Failed task-specific
validators point to versioned repair files and discourage unchanged validator
rereads. Other conditions do not
receive this completion gate. Hidden acceptance tests remain evaluator-only
and run exactly once after the agent stops, so the gate cannot reveal the
benchmark answer. Final scoring reruns public task validators first and may
apply one FULL default-safe Ruff repair without another LLM turn.

---

## Provider Examples and Model Tiers

GovernanceBench is designed for multi-provider runs and tier-to-tier comparisons.

### Registry candidates

- **OpenAI Chat Completions**: `gpt-4o-mini`, `gpt-5.6-luna`,
  `gpt-5.6-terra`, `gpt-5.6-sol`
- **OpenAI Responses**: explicit `gpt-5.6-sol-responses`,
  `gpt-5.6-terra-responses`, and `gpt-5.6-luna-responses` registry lanes with
  native flat function schemas
- **Anthropic**: `claude-haiku-4-5`, `claude-sonnet-4-5`, `claude-opus-4-5`
- **Google**: `gemini-3.5-flash`, `gemini-3.1-pro`
- **Qwen diagnostics**: `Qwen3.6-35B-A3B:deepinfra`,
  `Qwen3-Coder-Next:novita`, `Qwen3-Coder-480B-A35B-Instruct:novita`
- **OpenAI-compatible endpoints** (vLLM/Ollama/proxy): open-source model hosting

### Model tier framing (examples)

| Tier | Price Band (input $/1M tokens, indicative) | Example Models |
|------|---------------------------------------------|----------------|
| Nano | `< $1` | `gpt-4.1-nano`, `gemini-3.5-flash`, `claude-haiku-4-5` |
| Mini | `$1–$4` blended | `gpt-5.6-luna`, `gpt-4.1-mini` |
| Mid | `$5–$15` blended | `gpt-5.6-terra`, `claude-sonnet-4-5`, `gemini-3.1-pro` |
| Frontier | `> $15` blended | `gpt-5.6-sol`, `claude-opus-4-5` |
| Open-source | Infra-dependent | `Qwen/Qwen3.6-35B-A3B`, `Llama-3.3-70B`, `gpt-oss-120b` |

Registry entries are candidates, not availability claims. The GitHub workflow
live-probes exact model access, billing, native tool calls, and post-tool
continuation before any paid matrix begins. Final model ids must be recorded in
run metadata and report headers.

Use the workflow's `probe_only` input for a low-cost credential/model check. It
makes one tiny tool-enabled request per OpenAI or Hugging Face model and does not
start benchmark cells. OpenAI-compatible endpoints are also supported when their
secret is configured. Other registry providers fail closed until an equivalent
endpoint probe is implemented; they are examples, not currently runnable CI
targets.

### Running open models without HuggingFace credits

The four open tiers can run through the HuggingFace Inference Providers router
(`groups=open`) **or** through any direct OpenAI-compatible host
(`groups=open-direct`), which avoids the HF credit pool entirely. The
`open-direct` registry entries default to OpenRouter slugs. To run them, set:

- repo **variable** `BENCH_OPENAI_BASE_URL` — base URL of the host (defaults to
  `https://openrouter.ai/api/v1` when unset)
- repo **secret** `BENCH_OPENAI_COMPAT_API_KEY` — that host's API key

```bash
# Local example (OpenRouter):
export BENCH_OPENAI_BASE_URL=https://openrouter.ai/api/v1
export BENCH_OPENAI_COMPAT_API_KEY=sk-or-...
python -m govern_bench.run_bench \
  --provider openai-compat --model meta-llama/llama-3.1-8b-instruct \
  --task T1 --reps 1
```

Swap `BENCH_OPENAI_BASE_URL` and the `open-direct` model ids to target a
different OpenAI-compatible provider (DeepInfra, Together, Groq, etc.).

---

## Metrics and Statistical Methodology

### Primary metric

`tokens_per_correct_answer = mean_total_tokens / pass_rate`

Lower is better. This provider-neutral metric directly measures the stated goal:
the fewest tokens consumed for each correct answer. If `pass_rate == 0`, it is
non-finite.

### Core secondary metrics

- `pass_rate`
- `cost_of_pass = estimated_mean_api_cost_usd / pass_rate`
- `quality_score`
- `input_tokens`, `output_tokens`, `api_cost_usd`
- `cached_input_tokens`, `cache_write_tokens` when exposed by the provider
- `rework_turns` (implementation attempts, not individual validator commands),
  `governance_turns`, `wall_clock_s`
- governance-specific rates for clarification/safety tasks

### Statistical report fields

- 95% Wilson confidence interval for `pass_rate`
- 95% bootstrap confidence interval for `cost_of_pass` (1,000 resamples)
- `first_pass_rate` (the run passed with `rework_turns <= 1`; failed runs never
  count as first-pass successes)
- `consistency_score`
- `scaffold_lift` relative to `UNGOVERNED` for matched task/model
- `democratization_score` for nano+scaffold vs frontier+ungoverned comparisons
- CoP-quality Pareto frontier extraction

See `scripts/govern_bench/METHODOLOGY.md` for formulas and reporting rules.

---

## HF Submission Artifacts

GovernanceBench includes HF-oriented documentation and schema assets:

- `scripts/govern_bench/hf_card.md` — dataset card template/content
- `scripts/govern_bench/leaderboard_schema.json` — leaderboard JSON schema
- `scripts/govern_bench/METHODOLOGY.md` — standalone statistical methodology

Only complete empirical runs may be published as benchmark evidence. Partial or
provider-failed artifacts remain diagnostic and must not produce comparison claims.

### Result completeness contract

A real run is publishable only when every requested task/condition/repetition
cell is present exactly once and has no provider error or skipped status.
Cross-model reports additionally require identical cell sets for every model.
Provider failures remain diagnostic artifact rows, but the process exits nonzero
and the comparison generator rejects them instead of treating them as model
failures or zero-cost observations.

Coding cells additionally require all three gates: clean lint, project tests,
and the evaluator-only acceptance oracle. Pytest and Ruff caches are disabled so
validation artifacts do not pollute diffs or scope metrics.
Raw rows record project-test and hidden-oracle outcomes separately, preventing
the weakness audit from confusing a lint failure with an acceptance-boundary miss.

---

## File Structure

```
scripts/govern_bench/
├── README.md
├── METHODOLOGY.md                 ← standalone methodology (new)
├── hf_card.md                     ← HF dataset card (new)
├── leaderboard_schema.json        ← HF leaderboard schema (new)
├── __init__.py
├── compare_runs.py
├── conditions.py                  ← 12 executable condition definitions
├── harness.py
├── judge.py
├── metrics.py
├── oracles/                       ← evaluator-only post-agent acceptance tests
├── report.py
├── run_bench.py
├── tasks.py
├── tasks/
│   └── T1_*.yml ... T27_*.yml     ← available multi-domain suites
└── projects/
    ├── todo_api/                  ← current
    ├── cli_tool/                  ← current
    ├── data_pipeline/             ← available
    ├── verilog_module/            ← available
    ├── patent_draft/              ← available
    └── shell_scripts/             ← available
```

---

## Notes

- Do not publish comparative claims without run metadata, confidence intervals, and raw output
  artifacts.
- Keep generated benchmark results separate from source-controlled templates/docs.
