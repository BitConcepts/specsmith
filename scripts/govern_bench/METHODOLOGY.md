# GovernanceBench Statistical Methodology

This document defines the statistical design, aggregation rules, and reporting guardrails for
GovernanceBench.

> Publication status: the current repeated-run evidence and its limitations are
> published in `docs/site/efficiency-benchmark.md`. New claims remain unpublished
> until their raw artifacts pass the completeness and comparability gates below.

## 1) Objective

Quantify governance/scaffolding impact on:

1. correctness and safety outcomes,
2. token/cost efficiency,
3. reliability/consistency across repeated runs,
4. economic accessibility across model tiers.

## 2) Experimental Design

Each benchmark observation is a run over the Cartesian product:

- task (`T*`),
- governance condition (`12` executable conditions),
- model/provider pair,
- repetition index (`rep`).

Recommended repetitions:

- minimum analytical run: `n_reps = 5` per cell,
- publication-grade run: `n_reps = 10` per cell.

Cells with fewer repetitions should be reported as provisional.

### 2.1 Locked promotion profiles

Paid runs use versioned profiles so task selection, conditions, and repetition
counts cannot drift between experiments:

| Profile | Cells per model | Purpose |
|---|---:|---|
| `admission` | T28/FULL × 1 | Cheap one-cell model/tool-route admission |
| `controller-admission` | T1/T10/T11/T13/T28/FULL × 1 | Admit a controller or tool-schema change |
| `release-controls` | T10/T13/T28 × Cursor/FULL × 10 | Mandatory release regression controls |
| `broad-release` | 8 tasks × Cursor/FULL × 10 | One same-commit aggregate release claim |
| `substitution-screen` | T1/T10/T13/T28 × raw/FULL × 5 | Fair model-capability substitution screen |
| `substitution-release` | 8 tasks × raw/FULL × 10 | Release-grade lower-tier/frontier 2×2 claim |
| `publication-matched` | T28/T29/T30 × raw/Cursor/FULL × 10 | Frozen synthetic-plus-upstream publication grid |
| `publication-open-admission` | T30/FULL × 1 | Frozen 20B–35B real-repository admission |
| `publication-open-screen` | T30/FULL × 5 | Repeated screen after admission |
| `publication-open-release` | T30/FULL × 10 | Confirmation after a passing screen |
| `publication-real-repository-recovery` | T30 × raw/Cursor/FULL × 10 | Corrected frozen T30 recovery after V1 invalidation |
| `literature-v9-ablation` | T28/T29/T30/FULL × 1 | Isolated causal admission for each v9 controller feature |
| `literature-v9-screen` | T28/T29/T30/FULL × 5 | Combined-v9 screen after every feature admission |
| `literature-v9-release` | T28/T29/T30/FULL × 10 | Independent combined-v9 confirmation |

The promotion funnel is `n=1 admission → n=5 screening → n=10 release
replication`. A failed admission is repaired or rejected; it is not made
publishable by spending on more repetitions. Locked-profile task, condition,
or repetition overrides fail closed.

Publication protocol `GB-PREPRINT-2026-07-30-V1` is byte-hashed before paid
inference. Publication profiles additionally fail closed on model/provider
route drift. Raw rows retain the protocol ID and SHA-256; compact evidence
manifests retain the unique protocol identities represented by their sources.

V1 T30 is invalidated because its hidden license assertion was impossible for
the canonical pinned file and its horizon classification weakened FULL
completion. Corrected protocol `GB-PREPRINT-2026-07-30-V2` was separately
frozen before rerunning T30. An invalidated stratum is never pooled with its
replacement. Independently valid tasks from a multi-task artifact may be
selected before completeness validation; every selected cell must still be
complete, unique, and repetition-balanced. Provider-censored cells prohibit
analysis of their selected stratum and remain explicit expenditure.

Model-substitution release claims use a paired hierarchical bootstrap with
10,000 deterministic resamples. The fixed-suite interval resamples repetitions
within each task. The task-cluster interval also resamples task IDs and is the
required basis for claims that extend beyond the exact suite. Correctness uses
Wilson-based difference bounds and a predeclared five-percentage-point
non-inferiority margin. Token superiority requires the upper 95% TPCA-ratio
bound to remain below one.

### 2.2 Literature-driven v9 controller protocol

`LITERATURE_V9_PROTOCOL.yml` was written before paid v9 inference. It fixes the
frozen v8 reference, v9 candidate, T28/T29/T30 fixture set, FULL condition,
promotion ladder, failure accounting, and these causal cells:

- role/symbol/dependency retrieval without raw-source preload;
- five recent tool pairs plus lossless content-addressed evidence;
- deterministic gate, compiled-patch, or milestone lane selection;
- execution-signature early stop;
- early stop plus one focused critical replay; and
- the combined controller.

Critical replay depends on early stopping and is therefore tested as the pair
`early-stop,critical-replay`. A cascade is a separate routing experiment: the
first model emits a milestone handoff and a stronger model resumes the same
fixture and partial diff. The hidden oracle executes exactly once, after the
final route. Feature provenance, context pruning, evidence references, failed
token mass, and handoff state are part of every raw row. A favorable n=1 point
estimate cannot skip the n=5 and n=10 gates.

The six Sol admissions (`30634194223`, `30634194232`, `30634195926`,
`30634196894`, `30634197427`, `30634199163`) retain all negative rows. Only
the lane cell passed all three tasks. Rolling five-pair context and terminal
early-stop regressed T30, so neither was promoted. The prospective
`LITERATURE_V9_1_PROTOCOL.yml` freezes the evidence-informed repair before its
paid runs: compaction occurs only after a validated milestone, and an
escalation signal cannot terminate the current route unless a configured
stronger route can receive the same-tree handoff.

## 3) Core Metrics

### 3.1 Primary metric

`tokens_per_correct_answer = mean_total_tokens / pass_rate`

where:

- `mean_total_tokens` is the average input plus output tokens within a slice,
- `pass_rate` is fraction of passing runs in that slice.

If `pass_rate = 0`, the metric is non-finite and should be represented as null/non-finite
in leaderboard exports.

### 3.2 Secondary metrics

- `pass_rate`
- `cost_of_pass = estimated_mean_api_cost_usd / pass_rate`
- `quality_score`
- `input_tokens`, `output_tokens`, `api_cost_usd`
- `cached_input_tokens`, `cache_write_tokens` (when reported by the provider)
- `rework_turns`, `governance_turns`, `wall_clock_s`
- `failed_token_share`, `milestone_escalation_rate`
- `working_context_peak_chars`, `working_context_pruned_chars`, `evidence_ref_count`
- governance-specific behavior rates for ambiguity/safety tasks

## 4) Interval Estimation and Derived Statistics

### 4.1 Pass-rate confidence interval

Use a 95% Wilson score interval:

- `ci_pass_rate_low`
- `ci_pass_rate_high`

Wilson intervals are preferred over normal approximations for bounded Bernoulli outcomes,
especially for small sample sizes.

### 4.2 Cost-of-pass confidence interval

Use non-parametric bootstrap with 1,000 resamples over runs within each slice:

- recompute `cost_of_pass` per resample,
- report 2.5th and 97.5th percentiles as:
  - `ci_cop_low`
  - `ci_cop_high`

### 4.3 First-pass and consistency

- `first_pass_rate = P(rework_turns == 1)`
- `consistency_score = 1 - stdev(passed_bool)` (or equivalent bounded stability proxy)

Higher values indicate more predictable scaffold behavior.

### 4.4 Scaffold lift

For each `(task, model)`:

`scaffold_lift(condition) = pass_rate(condition) - pass_rate(UNGOVERNED)`

Lift should only be computed when both rates are defined on matched slices.

### 4.5 Democratization score

For a selected nano model and frontier baseline:

`democratization_score = CoP(nano + best_scaffold) / CoP(frontier + UNGOVERNED)`

Interpretation:

- `< 1.0` means nano+scaffold is cheaper per pass than frontier baseline.
- `= 1.0` parity.
- `> 1.0` no democratization advantage.

This comparison requires the complete matched 2×2 counterfactual grid:

- weaker model + `UNGOVERNED`,
- weaker model + `SPECSMITH_FULL`,
- stronger model + `UNGOVERNED`,
- stronger model + `SPECSMITH_FULL`.

All four slices must use identical tasks and repetition counts. The headline
comparison is weaker+FULL versus stronger+UNGOVERNED, but the other two cells
are required to distinguish governance lift from task/model variance. A
smaller governed model is a viable substitute only when it preserves or
improves correctness and improves at least one efficiency measure such as
tokens per correct answer or cost per pass. Under five repetitions is
diagnostic only.

## 5) Pareto Frontier

To summarize efficiency-quality tradeoffs, compute the Pareto frontier over points:

- x-axis: `cost_of_pass` (lower is better),
- y-axis: `quality_score` (higher is better),
- point key: `(model, condition, task_suite)`.

A point is Pareto-optimal if no other point has both lower/equal CoP and higher/equal quality
with at least one strict improvement.

## 6) Reporting Rules

All benchmark reports should include:

1. model/provider matrix used,
2. repetition count per slice,
3. confidence intervals for key metrics,
4. explicit treatment of non-finite CoP values,
5. raw run artifact references.

Runs below five repetitions per matched slice are diagnostic only and must not
produce superiority claims. Five repetitions support screening observations;
ten support release-quality publication. Comparative claims additionally
require complete identical cell sets and must preserve or improve correctness,
not merely reduce tokens or estimated cost.

Do not publish absolute performance claims without confidence intervals.
Do not publish comparative claims when intervals overlap substantially without caveats.

## 7) Reproducibility Requirements

- Use fixed benchmark definitions from versioned task/condition files.
- Start runs from clean project fixtures/worktrees.
- Inject evaluator-only acceptance tests only after the agent finishes. A
  standard coding task without a hidden oracle is not scoreable and must fail
  closed. Run project lint, project tests, and task-specific public validators
  before injection, then run the independent oracle exactly once in isolation.
  Passing requires every applicable check.
- For standard coding tasks, require `SPECSMITH_FULL` to pass `ruff check .`
  and `pytest` after its latest write before accepting `done`. Failed checks
  trigger measured repair turns. Do not apply this gate to comparison
  conditions, and never expose the hidden oracle during repair.
- The FULL controller may run one Ruff default-safe-fix pass after a failed
  completion check and once before final scoring after later writes. It must
  rerun lint, record the repair receipt, never enable unsafe fixes, and never
  use evaluator output to select a repair.
- Agent-loop equilibrium uses public completion evidence only. Never install or
  run the hidden oracle inside the model loop; it cannot trigger a repair turn.
- Give FULL one compact, stable five-tool schema for the entire run:
  `read_files`, `write_files`, `read_file`, `write_file`, and `done`.
  Controller phases may suspend a capability, but must not mutate the advertised
  schema. Record the schema hash in usage and transcript evidence so cache
  discontinuities fail the efficiency audit.
- Preload only versioned requirement-linked files. T1 receives its
  implementation/public-test boundary; T10 also receives the imported Todo
  model and dependency manifest proven necessary by admission traces. T11
  receives the exact file set repeated in every n=10 first action, excluding
  public-validator implementation. T13 remains retrieval-driven because its
  proposed preload regressed in controller admission. T28 receives only its
  active milestone. Do not expose repository-wide context or evaluator
  evidence.
- Long-horizon milestone maps and requirement-linked change boundaries are
  versioned task metadata, not evaluator evidence. Report only the next
  incomplete boundary and replace stale progress messages. Diagnostic
  milestone-packet cells compile the active milestone's public criteria,
  allowed write paths, validator names, and bounded current content into one
  executable work packet. Raw and compact evidence record completed/total
  milestones and tokens per completed milestone.
- Public task-specific validators may declare versioned repair boundaries.
  After a failure, report the authoritative failure plus only its linked files;
  suppress unchanged validator rereads. Keep hidden-oracle failures isolated.
- Disable pytest and Ruff caches during grading so generated cache files do not
  contaminate diffs, scope measurements, or subsequent validation.
- Record model identifiers, provider, run timestamp, and benchmark commit SHA.
- Record model-specific compatibility parameters. GPT-5.6 Chat Completions
  runs use `reasoning_effort=none` because that is the function-tool mode
  supported by the provider; every condition for that model uses the same mode.
- Treat OpenAI Responses as a distinct provider route, never an invisible
  switch beneath a Chat Completions label. Responses admissions default to
  low reasoning effort, low text verbosity, native flat function schemas,
  bounded requests, and stored per-cell continuation. Reuse
  `previous_response_id` only when the current normalized history has the exact
  expected prefix; controller compaction or rewriting resets state and sends a
  complete request. Record provider, API surface, reasoning effort, verbosity,
  cached tokens, normalized and provider-visible schema hashes, and tool choice
  for every call. Request strict argument enforcement only when every declared
  property is required and nested schemas satisfy the same constraint;
  optional atomic-patch fields remain locally fail-closed.
- Admit the Responses route only after a two-step live probe: the first response
  must emit the required native function call, and the same stored response must
  accept `function_call_output` and produce continuation text. A parser-only
  success does not establish a usable agent loop.
- The first Responses cell keeps the accepted controller fixed at
  `scalar-milestone-packet-authority`. Admit Sol on T28/FULL at n=1, then Terra
  only if Sol is correct. Do not attribute a difference to governance when
  model, reasoning effort, or controller policy changed in the same cell.
- Unless an experiment overrides them, use model-card sampling defaults for
  Qwen routes: Coder Next `temperature=1.0, top_p=0.95`; Coder 480B-A35B
  `0.7/0.8`; Qwen3.6 coding `0.6/0.95`. Record the exact hosted route because
  parser, template, quantization, and latency are part of the result.
- Dedicated Qwen3-Coder-30B FP8 admissions pin vLLM, `qwen3_xml`, hardware,
  context length, and model revision as experiment variables. Hosted
  structured-tool probes demonstrate route compatibility but must not be
  described as proof of a specific server-side parser when the provider does
  not disclose it.
- Bound endpoint deployment, each provider request, the full cell, and external
  workflow execution separately. Default to zero provider retries so a timeout
  is a visible censored observation rather than hidden duplicate spend.
- Hash identical single-action no-op arguments without retaining their bodies.
  Issue one recovery, then stop the second identical no-op as a repeated tool
  loop. Versioned repair-only tool-surface experiments remain diagnostic when
  they change the provider schema; promotion still requires one stable compact
  schema and a passing independent oracle.
- Current open-frontier admissions use their published coding/agent defaults:
  Kimi K2.7 Code and MiniMax-M3 `temperature=1.0, top_p=0.95`; GLM-5.2
  and DeepSeek-V4 Pro `1.0/1.0`. Provider routes remain pinned and priced
  separately.
- Preserve raw benchmark output JSON for auditability.
- Include every failed model run in token and cost denominators and report its
  absolute tokens, estimated dollars, and share of total expenditure.
- For a pinned upstream fixture, preserve repository URL, commit, license, and
  starter-file SHA-256 values. Public validators remain model-visible; the
  independent acceptance oracle is injected only after completion.

## 8) Limitations

- Provider pricing and model behavior can drift over time. Dollar cost is a
  secondary estimate based on the versioned pricing table; token efficiency is
  the provider-neutral primary measure.
- LLM judge components can add evaluator variance.
- Cross-domain comparability depends on validator quality per domain.

These limitations must be disclosed in external benchmark communication.
