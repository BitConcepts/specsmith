# Long-Horizon Benchmark and Weakness Audit

GovernanceBench `T28` is a 20-turn product task spanning a Python/FastAPI API,
Go worker, TypeScript/React UI, Playwright journey, JSON Schema, CSS, public
tests, and architecture documentation. Its result is reported separately as
well as in the eight-task suite so cheap governance gates cannot hide
long-horizon cost.

Controller changes must now pass the locked `controller-admission` profile on
T1, T10, T11, T13, and T28 before a broad paid run. Benchmark audits also reject FULL
tool-schema discontinuity: controller phases may suspend reads, but the compact
advertised schema and its recorded hash must remain stable. This turns provider
cache stability into a deterministic, testable release property.

For model-capability substitution, the audit accepts conclusions only from a
matched 2×2 grid: weaker/raw, weaker/FULL, stronger/raw, and stronger/FULL on
the same tasks and repetition count. The smaller governed model must preserve
correctness and improve tokens per correct answer or cost per pass to count as
a viable substitute.

The first use of that gate produced two useful rejections. Qwen3.6/DeepInfra
passed T28 in
[workflow 30205541608](https://github.com/layer1labs/specsmith/actions/runs/30205541608)
at 67,701 tokens, but the audit selected `advance_candidate` because that is
3.87× the release Sol anchor. The Sol controller admission in
[workflow 30205537706](https://github.com/layer1labs/specsmith/actions/runs/30205537706)
passed all three cells, yet T10 expanded to 63,128 tokens and eleven turns.
Its trace showed that the controller supplied `app/main.py` and the public
test file, suspended all reads, then rejected requested reads of the Todo model
and dependency manifest. This is controller-caused rework, not useful
governance.

The audit now loads release-quality T1, T10, T13, and T28 anchors. A same-model
cell more than 10% above its task anchor yields
`controller_efficiency_regression` and `optimize_and_rerun`; a weaker candidate
above the frontier anchor still yields `advance_candidate`. A green workflow
therefore cannot silently promote a correct but inefficient controller.

The identical controller admission after repair,
[workflow 30206236593](https://github.com/layer1labs/specsmith/actions/runs/30206236593),
cleared the gate: T1/T10/T28 were 7,845, 9,305, and 17,818 tokens, all correct,
with two, two, and five turns. T1 and T10 are below their release anchors and
T28 remains within 1.8%. The only finding was n=1 undersampling.

The candidate admission in
[workflow 30206263461](https://github.com/layer1labs/specsmith/actions/runs/30206263461)
then separated two correct weaker models by efficiency: Luna was rejected at
43,112 tokens and eleven turns, while Terra advanced at 17,655 tokens and five
turns. This demonstrates why correctness alone is not an admission decision.

## Current broad audit

[Workflow 30206398622](https://github.com/layer1labs/specsmith/actions/runs/30206398622)
completed 160/160 valid rows at `36435f2`. FULL passed 80/80 overall and 60/60
coding cells. Cursor-style rules passed 70/80 overall and 60/60 coding cells.
The matched coding slice favors FULL by 47.3% TPCA with equal correctness.

There is no governed correctness blocker. The remaining efficiency findings
are narrower:

- T11 FULL was 23,472 TPCA versus Cursor-style at 20,116; every row reread the
  same files and then repaired.
- T13 FULL remained far below Cursor-style (14,424 versus 35,532 TPCA) but was
  34% above its prior release anchor.
- Cursor-style had one T11 turn-budget exhaustion and broad scope expansion.

T11 and T13 were added to controller admission. In
[workflow 30209142281](https://github.com/layer1labs/specsmith/actions/runs/30209142281),
T11's bounded non-evaluator context reduced the diagnostic from 23,472 tokens
and six turns to 11,210 tokens and two turns. T13's proposed preload regressed
from the broad-run 14,424-token mean to 16,190 tokens, so it was removed. This
is a trace-driven post-run decision; the immutable n=10 result is not
rewritten or pooled with it.

## Current broad audit and repair decision

[Workflow 30199359636](https://github.com/layer1labs/specsmith/actions/runs/30199359636)
completed 160/160 valid GPT-5.6 Sol rows: eight tasks, Cursor-style rules and
FULL, and ten repetitions per cell. The deterministic audit found five
high-severity weakness classes and selected `repair_and_rerun`, not publication.

| Coding slice | Correct | TPCA | Cost/pass | Mean turns |
|---|---:|---:|---:|---:|
| Cursor-style rules | 60/60 | 25,852 | $0.1498 | 6.02 |
| Specsmith FULL | 54/60 | 13,907 | $0.1371 | 4.47 |

FULL remains more token-efficient per correct result, but a lower pass rate is
a hard blocker. Six failures were concentrated in T10 and T13:

- **T10, 1/10 failed:** the implementation did not preserve submitted priority,
  so `by_priority` returned three low-priority items instead of one low and two
  high. Model-authored project tests passed; the evaluator-isolated oracle
  rejected the result.
- **T13, 5/10 failed:** seven rows needed first-pass repair. Pytest tracebacks
  named `tests/test_process.py`, causing the focused boundary to permit only
  that file even when Click reported that the implementation exposed
  `--filters` rather than `--filter`. One row exhausted 12 turns, one stopped
  on an explicit blocked narration, and three stopped with an oracle failure.

This is useful evidence against relying on n=5 point estimates: the preceding
screen passed every FULL cell, while the independent n=10 sample exposed a
systematic 30% T13 first-pass rate and about 15,901 extra tokens per repaired
row. The audit also retained medium Cursor-only scope expansion, one repeated
FULL tool loop, three repair outliers, and low-severity FULL cache
discontinuity.

The data-driven repair in commit `42bd7d8`:

1. adds controller-owned T10 and T13 contract validators derived from the
   already-public requirements;
2. maps each validator directly to its implementation file;
3. keeps every declared implementation/test path available after a generic
   pytest failure, because an asserting test filename does not locate the
   defect; and
4. preserves the hidden oracle and existing turn ceilings.

The identical T10/T13 matched n=10 confirmation,
[workflow 30201998763](https://github.com/layer1labs/specsmith/actions/runs/30201998763),
completed 40/40 valid and correct rows:

| Task / condition | Correct | TPCA | Cost/pass | Mean turns | Mean wall |
|---|---:|---:|---:|---:|---:|
| T10 Cursor-style | 10/10 | 25,139 | $0.1441 | 5.6 | 32.9s |
| T10 FULL | 10/10 | 13,842 | $0.1094 | 4.6 | 23.0s |
| T13 Cursor-style | 10/10 | 35,173 | $0.1290 | 9.5 | 29.1s |
| T13 FULL | 10/10 | 10,742 | $0.0820 | 4.8 | 27.3s |

FULL's T13 distribution stabilized at 9,021–12,068 tokens with 9.4% CV,
versus the pre-repair 8,848–47,040 range, five failures, and 67.9% CV. All ten
FULL rows passed the new contract on their first completion attempt. The audit
found no high or critical weakness and selected `publish_or_expand`. Remaining
findings are medium Cursor-only scope/context observations and low FULL cache
telemetry.

The targeted evidence proves the measured blocker is repaired. It is not
pooled into the earlier broad aggregate because task grids and commits differ.
A same-commit broad rerun is optional only if a single aggregate release claim
is required; it is not needed to justify another controller change.

## Current long-horizon release envelope

[Workflow 30179751802](https://github.com/layer1labs/specsmith/actions/runs/30179751802)
was the prior standalone T28 release screen. The newer T28 slice in
[workflow 30199359636](https://github.com/layer1labs/specsmith/actions/runs/30199359636)
also passed all ten public and evaluator-isolated cells.

| T28 screen | Correct | TPCA | Mean turns | Mean cost | Mean wall time |
|---|---:|---:|---:|---:|---:|
| Prior standalone FULL | 10/10 | 17,633.7 | 5.0 | $0.2204 | 57.5s |
| Current broad Cursor slice | 10/10 | 54,071.1 | 8.3 | $0.3143 | 78.0s |
| Current broad FULL slice | 10/10 | 17,501.7 | 5.0 | $0.2167 | 70.6s |

The new FULL T28 mean is 0.8% below the prior standalone n=10 result and its 1.97% CV remains
low. FULL reduced TPCA by 67.6%, cost/pass by 31.1%, turns by 39.8%, and wall
time by 9.4% versus the matched Cursor-style slice. This task-level envelope is
release-quality; it does not retroactively make the earlier broad aggregate
publication-eligible.

The preceding eight-task n=5 screen in
[workflow 30180171688](https://github.com/layer1labs/specsmith/actions/runs/30180171688)
contains 80/80 valid rows. FULL passed 40/40 at 8,034 TPCA; Cursor-style rules
passed 35/40 at 23,112 TPCA. The T28 slice passed 5/5 in both conditions at
17,362 FULL versus 52,381 Cursor-style TPCA.

At that commit, the optimization stopping decision was evidence-based: adding a micro-patch tool increased
FULL to 55,451 TPCA, while removing it and making lint and milestone invariants
explicit produced ten stable five-turn runs (1.1% TPCA CV). No open-model
diagnostic exposed another controller change that improved a correct result.
That n=5 audit's only FULL observation was low-severity prompt-cache
discontinuity. Stabilizing a larger advertised tool schema could lower billed
cache cost but would add counted input tokens and weaken the proven minimal-tool
surface, so it does not justify another optimization screen.

## Matched five-repetition screen

[Workflow 30045327768](https://github.com/layer1labs/specsmith/actions/runs/30045327768)
ran commit `5790d41971e027d2abd34973169c10a57e277eaa` with GPT-5.6 Sol,
Cursor rules, Specsmith FULL, and five matched repetitions. Every T28 cell
passed project checks and the evaluator-isolated oracle.

| Condition | Correct | Mean tokens | Tokens/correct | Mean turns | Mean wall time |
|---|---:|---:|---:|---:|---:|
| Cursor rules | 5/5 | 69.1k | 69.1k | 10.8 | 88.9s |
| Specsmith FULL | 5/5 | 32.0k | 32.0k | 11.4 | 86.6s |

With equal observed correctness, FULL used 53.6% fewer tokens per correct
answer, 26.0% lower measured provider cost, and 2.6% less wall time. The audit
found one medium Cursor-only scope-expansion finding and no FULL weakness; its
next action is `expand_release_sample`. The earlier `29963515885` screen remains
part of the versioned eight-task aggregate but is not combined with this newer
commit.

Four FULL repetitions needed the same deterministic backend repair and spent
one turn rereading the single failed file after its prior write body had been
compacted to a digest. That cost remains charged to this screen. The resulting
controller improvement now returns bounded current content when exactly one
requirement-linked file fails and removes read tools for the next turn, enabling
an immediate repair write. Ambiguous multi-file failures retain the safer
read-capable path.

## Prior optimized Sol envelope

[Workflow 30077217017](https://github.com/layer1labs/specsmith/actions/runs/30077217017)
verified that change at n=5 on commit `3d86308`. Every FULL cell passed public
checks and the isolated oracle.

| FULL screen | Correct | TPCA | Mean input | Mean turns | Mean cost |
|---|---:|---:|---:|---:|---:|
| Before focused handoff | 5/5 | 32,020 | 25,356 | 11.4 | $0.2640 |
| Focused handoff | 5/5 | 28,314 | 21,725 | 10.2 | $0.2519 |

The same-model reduction is 11.6% TPCA, 14.3% input tokens, 10.5% turns, and
4.6% measured cost. All three new repair traces skipped the former reread and
wrote the focused file immediately. The audit found no weakness and selected
`expand_release_sample`; 28,314 TPCA became the versioned T28 frontier envelope.

## July 24 feedback replay

The final n=5 Sol screen
[30093712102](https://github.com/layer1labs/specsmith/actions/runs/30093712102)
at commit `708d47b` passed every public and independent check.

| FULL screen | Correct | TPCA | Mean input | Mean turns | Mean cost |
|---|---:|---:|---:|---:|---:|
| Focused handoff | 5/5 | 28,314 | 21,725 | 10.2 | $0.2519 |
| Final learning replay | 5/5 | 26,499 | 20,204 | 9.8 | $0.2414 |

The unchanged release-quality screen
[30099279843](https://github.com/layer1labs/specsmith/actions/runs/30099279843)
then passed 10/10 at 30,316.8 TPCA, 23,634 mean input tokens, 10.3 turns,
$0.2767 mean cost, and 85.8 seconds. Its audit found no weakness and selected
`publish_or_expand`. The larger-sample mean is 14.4% above the n=5 learning
point estimate, with an observed 23,316–36,108 range and approximate 95%
t-interval of 27,573–33,061. That result replaced the smaller point estimate
at the time and is now superseded by the July 25 envelope above.

The measured weaknesses that produced the final revision came from open-model
traces, not another judge call:

- GLM narrated two explicit milestone writes. One recovery produced real files,
  so a second is allowed only after new expected-file write progress and the
  total remains capped at two.
- DeepSeek Pro passed public checks but the isolated oracle found a missing Go
  `id` default. The requirement now states non-empty `id` and `created_at`
  defaults and a controller-owned public validator enforces them without
  changing or exposing the oracle.
- MiniMax returned empty assistant continuations. The controller continued to
  fail closed; empty text is never converted into a fabricated action.

[Workflow 30093614453](https://github.com/layer1labs/specsmith/actions/runs/30093614453)
confirmed the repairs: GLM passed at 73,618 tokens and DeepSeek Pro at 84,409.
Their audits found no high/critical weakness but blocked n=5 because their TPCA
was 2.6× and 2.98× the then-current Sol envelope.

Kimi then tested the provider-fallback boundary. DeepInfra's requested n=5
[workflow 30092473534](https://github.com/layer1labs/specsmith/actions/runs/30092473534)
produced eight router 504 cells, so the incomplete artifact was rejected rather
than scored. Together failed a live probe with HTTP 403. Novita completed one
matched diagnostic in
[workflow 30096796977](https://github.com/layer1labs/specsmith/actions/runs/30096796977):
Cursor Rules failed at 108,137 tokens and 20 turns; FULL passed at 43,015 tokens
and 10 turns. Its audit reports Cursor turn-budget exhaustion and FULL reread
churn. Although governance cut tokens by 60.2% and recovered correctness, the
FULL result is 1.42× the release-sized Sol envelope and does not earn n=5.

## Feedback-loop example

Four GPT-OSS-120B diagnostics show how the audit drives bounded changes without
turning failures into a leaderboard win:

| Workflow | Smallest changed boundary | Result |
|---|---|---|
| [30077072490](https://github.com/layer1labs/specsmith/actions/runs/30077072490) | DeepInfra provider route | one valid tool call, then two empty continuations |
| [30077459159](https://github.com/layer1labs/specsmith/actions/runs/30077459159) | Novita provider route only | continuation worked; 20 serialized actions exposed an adaptive-state bug |
| [30077929145](https://github.com/layer1labs/specsmith/actions/runs/30077929145) | composite-read state separated from writes | 44,692 tokens and 17 turns, but `done` arguments arrived as text |
| [30078601832](https://github.com/layer1labs/specsmith/actions/runs/30078601832) | exact-schema completion recovery | stochastic trace never completed scope; 49,339 tokens, 20 turns, failed |

The first trace created `tool_continuation_failure`; the second led to
independent read/write adaptation; the third led to a narrow completion guard
that still requires complete write evidence and unchanged validators. The
fourth did not reproduce the prerequisite and was rejected. No further managed
GPT-OSS repetition or larger turn budget is justified.

## Qwen long-horizon diagnostic

[Workflow 29962883256](https://github.com/layer1labs/specsmith/actions/runs/29962883256)
tested three managed Hugging Face routes at one repetition. All six T28 cells
failed, so none has finite TPCA and none was promoted to a repeated screen.

| Route | Cursor T28 | FULL T28 | FULL tokens | Diagnostic |
|---|---:|---:|---:|---|
| Qwen3.6-35B-A3B / DeepInfra | fail | fail | 116.5k | all ten boundaries written, but repair remained serial and exhausted 20 turns |
| Qwen3-Coder-Next / Novita | fail | fail | 68.1k | lower input history, incomplete cross-boundary validation |
| Qwen3-Coder-480B-A35B / Novita | fail | fail | 55.4k | model size did not prevent milestone fragmentation |

The follow-up changed action shape, not the turn cap. In
[workflow 29966620911](https://github.com/layer1labs/specsmith/actions/runs/29966620911),
Qwen3.6/DeepInfra FULL passed T2 and T11 (2/3) at 100.7k TPCA versus Cursor's
T11-only 1/3 at 358.7k TPCA. FULL T28 still failed after 133.7k tokens and 20
turns. Its public validators passed, but the hidden oracle scored 3/5 because
the shared schema did not require `acknowledged_at` and the browser test did not
use semantic role locators. The trace also showed repeated reads of the public
UI validator after its failure instead of an edit.

The controller now keeps scalar tools valid while adding composite operations,
adds a visible deterministic shared-contract validator, and maps each failed
public validator to versioned requirement-linked files. The repair instruction
explicitly makes failure output authoritative and suppresses unchanged validator
rereads. The hidden oracle remains isolated. A native Qwen serving lane should
still use the model's `qwen3_coder` tool parser or Qwen's agent scaffold before
comparing model sizes again.

The targeted [T28 follow-up 29969671380](https://github.com/layer1labs/specsmith/actions/runs/29969671380)
confirmed that contract visibility worked but the managed route remained
inefficient. Later runs separated scaffold defects from route reliability:

- `30010219286` was correct at 180,895 tokens, but exhausted 20 turns and
  repeated 26 of 48 reads.
- `30011743699` reduced tokens to 136,360 after digest and repair controls, but
  failed the independent oracle.
- `30013020354` passed the oracle 5/5, yet its own tests coupled to a nonexistent
  private `_data` attribute and still failed after 151,666 tokens and 20 turns.

The resulting controller records model-owned writes and known absence as
epistemic evidence, withholds already-known reads at the next milestone, and
returns repair writes directly to deterministic validation. The public T28
contract now also enforces the starter Go package and safely composed UI query
parameters. These changes close observed governance gaps without changing the
turn cap or hidden oracle. The remaining finding is route/model reliability:
managed Qwen3.6 is not promoted, and the next Qwen test must change the native
tool-serving protocol.

The final scorer now reruns public task validators before installing the hidden
oracle, applies at most one FULL default-safe Ruff repair, and executes the
oracle exactly once after the model loop. Agent-loop equilibrium uses public
evidence only, so hidden results cannot cause another model repair turn.

## Completion and oracle boundaries

The clean starter cannot pass the hidden oracle without implementing:

- one shared incident field/enumeration contract;
- create, list/filter, and acknowledge API behavior;
- Go `NormalizeAlert` validation and normalization;
- loading, empty, error, filtering, and acknowledge UI states;
- accessible controls and a non-skipped Playwright journey;
- meaningful public boundary tests; and
- an architecture record covering end-to-end data flow.

For FULL, controller-owned Ruff, pytest, Go, and UI validators must pass after
the latest write. The evaluator then returns only an equilibrium decision, not
hidden test content, to a bounded repair loop. One Ruff default-safe-fix pass is
permitted before a lint-only failure is returned; unsafe fixes are never
enabled.

## Run and audit it

Start with one repetition:

```bash
python scripts/govern_bench/run_bench.py \
  --task T28 \
  --condition CURSOR_RULES \
  --condition SPECSMITH_FULL \
  --provider openai \
  --model gpt-5.6-sol \
  --reps 1 \
  --json-output bench-results-t28.json \
  --output bench-report-t28.md
```

The runner writes `bench-results-t28.audit.json`. Combine outcome findings with
repository health through Specsmith:

```bash
specsmith audit \
  --project-dir . \
  --benchmark-results bench-results-t28.json \
  --report benchmark-project-audit.json
```

High or critical benchmark weaknesses make the combined audit exit non-zero.
The JSON audit also includes `next_experiment`: a deterministic action,
readiness flag, rationale, evidence codes, and the exact task/condition slice.
It rejects incomplete artifacts, repairs correctness before cost, optimizes a
measured efficiency regression, advances a clean diagnostic to five
repetitions, and advances a clean screen to ten. A versioned, source-linked
frontier envelope prevents a correct but materially more expensive challenger
from earning five paid repetitions. Non-row JSON documents fail closed as
`reject_artifact`. This closes the feedback loop without asking another model
to judge its own work.

| Weakness | Meaning | First response |
|---|---|---|
| `incomplete_evidence` / `missing_cells` | A requested result is absent or errored. | Repair infrastructure and rerun the identical grid. |
| `uneven_repetitions` / `duplicate_cells` | Compared evidence is not one matched grid. | Reject and regenerate the artifact. |
| `turn_budget_exhausted` | Work reached the bounded cap. | Inspect action targets; do not raise the cap blindly. |
| `tool_call_serialization` | The route repeatedly emits one action per turn. | Use a compatible parser or bounded composite tools. |
| `broad_reread_churn` | Unchanged files dominate reads. | Replace bodies with version receipts and active evidence. |
| `milestone_fragmentation` | Several components changed without a completed boundary. | Stage the active milestone and batch independent files. |
| `premature_text_stop` | Narration stopped before a terminal action. | Permit one continuation; a second requires new write progress, then fail closed. |
| `tool_continuation_failure` | A route calls a tool, then emits two empty continuations. | Verify the native protocol, change only the serving route, and rerun once. |
| `acceptance_gap` | Public checks pass but the hidden oracle fails. | Add an immutable independent boundary test. |
| `governed_failure` | A Specsmith cell failed, even without a baseline row. | Repair the measured stop reason before repetition. |
| `scope_expansion` | Writes exceed declared requirement boundaries. | Verify necessity or constrain retrieval/edits. |
| `cursor_correctness_regression` | FULL passes less often on a task. | Repair correctness before claiming efficiency. |
| `cursor_efficiency_regression` | FULL TPCA exceeds Cursor by more than 10%. | Remove rereads, planning, or validator churn. |
| `verification_repair_outlier` | A row materially exceeds its cell's turn median. | Return only focused failure evidence and keep the repair bounded. |
| `context_dominance` | Input is at least ten times output. | Use stable prefixes, JIT retrieval, and compaction. |

## Improvement loop

1. Run a matched n=1 diagnostic.
2. Audit every correctness, efficiency, and completeness weakness.
3. Link a reproducible miss to a requirement and independent regression test.
4. Change the smallest controller, context, or serving boundary implicated by
   the trace.
5. Rerun the affected cells; promote only correct diagnostics to n=5.
6. Require n=10 before a release-quality statistical claim.

The audit is deterministic and spends no judge-model tokens. Raw transcripts,
content-free tool targets and argument hashes, diffs, validator output,
controller decisions, task metadata, and exact provider receipts remain the
engineering evidence.
