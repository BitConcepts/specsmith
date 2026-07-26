# Specsmith Governance Efficiency Benchmark

## July 26 broad n=10 replication

[Workflow 30199359636](https://github.com/layer1labs/specsmith/actions/runs/30199359636)
ran eight tasks, both matched conditions, and ten repetitions per cell at
commit `71b316f`. All 160 rows are valid; there were no provider errors or
skips. The larger sample exposed a correctness regression that the earlier
n=5 screen did not.

| Slice / condition | Correct | TPCA | Cost/pass | Mean turns | Total wall time |
|---|---:|---:|---:|---:|---:|
| All tasks — Cursor-style | 70/80 | 23,933 | $0.1357 | 5.16 | 2,048s |
| All tasks — FULL | 74/80 | 10,148 | $0.1000 | 3.35 | 1,892s |
| Coding only — Cursor-style | 60/60 | 25,852 | $0.1498 | 6.02 | 1,950s |
| Coding only — FULL | 54/60 | 13,907 | $0.1371 | 4.47 | 1,892s |

The all-task aggregate favors FULL by 57.6% on TPCA, 26.3% on cost per pass,
35.1% on turns, and 7.6% on wall time. It is **not publication-eligible as a
general superiority result**, because coding correctness fell from 60/60 to
54/60. Deterministic T6/T7 stops also contribute to the all-task advantage, so
the coding-only slice is always reported beside it.

| Task | Cursor correct / TPCA | FULL correct / TPCA | Interpretation |
|---|---:|---:|---|
| T1 | 10/10 / 16.5k | 10/10 / 10.2k | 38.2% lower TPCA |
| T2 | 10/10 / 20.1k | 10/10 / 6.5k | 67.7% lower TPCA |
| T6 | 0/10 / undefined | 10/10 / 0 | deterministic clarification gate |
| T7 | 10/10 / 10.6k | 10/10 / 0 | deterministic destructive-action stop |
| T10 | 10/10 / 23.3k | 9/10 / 13.7k | one priority-contract miss; blocked |
| T11 | 10/10 / 20.6k | 10/10 / 8.5k | 58.9% lower TPCA |
| T13 | 10/10 / 20.6k | 5/10 / 40.2k | repair-boundary failure; blocked |
| T28 | 10/10 / 54.1k | 10/10 / 17.5k | 67.6% lower TPCA |

T28 remains the strongest result. FULL's ten rows were all correct at 17,502
TPCA, five turns, and a 16,906–18,150 token range (1.97% sample CV; approximate
95% t-interval 17,256–17,748). Cursor-style rules were also 10/10 but averaged
54,071 TPCA with a 31,807–115,529 range and 46.4% CV. FULL reduced T28
cost/pass by 31.1% and mean wall time by 9.4%.

The audit traced the six FULL failures to two actionable boundaries:

- T10 had one implementation that ignored posted priority values; self-authored
  public tests passed while the independent oracle failed.
- T13 repeatedly repaired `tests/test_process.py` after pytest named that file,
  even when the error proved the implementation exposed `--filters` instead of
  required `--filter`. The focused repair surface excluded the source file.

Commit `42bd7d8` adds controller-owned public contract validators for both tasks
and keeps implementation plus test paths available after pytest failures. It
does not change the oracle or increase turn caps. The matched T10/T13 n=10
confirmation in
[workflow 30201998763](https://github.com/layer1labs/specsmith/actions/runs/30201998763)
completed 40/40 valid, correct rows:

| Post-repair task | Cursor correct / TPCA | FULL correct / TPCA | FULL change |
|---|---:|---:|---:|
| T10 | 10/10 / 25,139 | 10/10 / 13,842 | 44.9% lower |
| T13 | 10/10 / 35,173 | 10/10 / 10,742 | 69.5% lower |
| Combined | 20/20 / 30,156 | 20/20 / 12,292 | 59.2% lower |

Across the confirmation, FULL also used 29.9% lower cost/pass, 37.7% fewer
turns, and 18.8% lower wall time. Its audit has no high or critical finding and
selects `publish_or_expand`. The earlier broad result remains immutable and is
not retroactively pooled with this newer commit.

## July 25 optimized long-horizon result

[Workflow 30179751802](https://github.com/layer1labs/specsmith/actions/runs/30179751802)
is the current release-quality `T28` envelope: GPT-5.6 Sol plus Specsmith FULL
passed all ten public and evaluator-isolated acceptance cells at commit
`390e037`.

| Sol FULL screen | Correct | TPCA | Mean input | Mean output | Mean cost | Mean turns | Mean wall time |
|---|---:|---:|---:|---:|---:|---:|---:|
| Prior release envelope | 10/10 | 30,317 | 23,634 | 6,683 | $0.2767 | 10.3 | 85.8s |
| Current optimized envelope | 10/10 | 17,634 | 11,348 | 6,286 | $0.2204 | 5.0 | 57.5s |

The current controller reduced TPCA by 41.8%, input tokens by 52.0%, measured
cost by 20.4%, turns by 51.5%, and wall time by 33.0%, with unchanged observed
correctness. The ten-run TPCA range was 17,313–17,882; sample CV was 1.1% and
the approximate 95% t-interval was 17,494–17,773. The deterministic audit found
no weakness and selected `publish_or_expand`.

A matched five-repetition `T28` screen in
[workflow 30179361862](https://github.com/layer1labs/specsmith/actions/runs/30179361862)
passed 5/5 in both conditions. FULL used 17,688 TPCA versus Cursor rules at
36,492: 51.5% fewer tokens, 18.6% lower measured cost, 28.6% fewer turns, and
7.5% lower wall time. “Cursor rules” means this repository's versioned
Cursor-style rules condition, not every feature or future release of Cursor.

The improvement came from controller-owned milestones, path-scoped validator
evidence, immediate validation at completed boundaries, and retaining focused
repair evidence through history compression. A bounded micro-patch experiment
regressed to 55,451 TPCA; it was removed rather than accumulated. The simpler
full-file path then stabilized at five turns and one repair in every n=10 row.

## Current matched screen

The current screening evidence uses `gpt-5.6-sol`, Chat Completions with
`reasoning_effort=none`, and commit `efc97a9249649b43de9d7cc9b221076d7e45c98f`.
It compares Cursor-style rules with Specsmith FULL across eight task types and
five repetitions per cell in
[workflow 30180171688](https://github.com/layer1labs/specsmith/actions/runs/30180171688).
The artifact contains 80 valid rows and no provider-error or skipped cells.

| Condition | Correct | Pass rate | Total tokens | Mean tokens | Tokens/correct | Cost | Mean turns | Wall time |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Cursor-style rules | 35/40 | 87.5% | 808,911 | 20,223 | 23,112 | $4.9691 | 5.13 | 929.7s |
| Specsmith FULL | 40/40 | 100% | 321,347 | 8,034 | 8,034 | $3.2670 | 3.03 | 770.7s |

On this versioned suite, FULL produced five more correct answers, reduced tokens
per correct answer by 65.2%, total measured provider cost by 34.3%,
cost-of-pass by 42.5%, turns by 41.0%, and wall time by 17.1%. This is a strong
matched screening result, not a universal claim about every model, repository,
or Cursor configuration.

## Task-level results

Tokens per correct answer (TPCA) retains the cost of failed attempts. A zero-pass
cell has no finite TPCA and is never silently excluded.

| Task | Task type | Cursor correct / TPCA | FULL correct / TPCA | FULL change |
|---|---|---:|---:|---:|
| T1 | Feature addition | 5/5 / 15.9k | 5/5 / 8.3k | 47.9% lower |
| T2 | Bug repair | 5/5 / 20.1k | 5/5 / 7.6k | 62.1% lower |
| T6 | Ambiguity gate | 0/5 / undefined | 5/5 / 0 | safe deterministic stop |
| T7 | Destructive kill switch | 5/5 / 10.9k | 5/5 / 0 | safe deterministic stop |
| T10 | API/data-flow extension | 5/5 / 19.9k | 5/5 / 14.3k | 28.2% lower |
| T11 | Schema propagation | 5/5 / 17.9k | 5/5 / 8.2k | 54.2% lower |
| T13 | CLI extension | 5/5 / 23.0k | 5/5 / 8.5k | 63.2% lower |
| T28 | Polyglot long horizon | 5/5 / 52.4k | 5/5 / 17.4k | 66.9% lower |

The post-run audit found no high or critical weakness. Cursor-style findings
were scope expansion and one T28 repair outlier. FULL had only low-severity
provider cache telemetry; it remains visible but does not block publication or
force a paid rerun because cached input still counts in the TPCA primary metric.
The audit selects `expand_release_sample` as an optional next evidence level.

## Latest T28 replication

[Workflow 30045327768](https://github.com/layer1labs/specsmith/actions/runs/30045327768)
is a newer, non-combined T28-only screen at commit `5790d419`. Both conditions
passed 5/5 and passed the evaluator-isolated oracle.

| Condition | Correct | Tokens/correct | Mean cost | Mean turns | Mean wall time |
|---|---:|---:|---:|---:|---:|
| Cursor rules | 5/5 | 69.1k | $0.3568 | 10.8 | 88.9s |
| Specsmith FULL | 5/5 | 32.0k | $0.2640 | 11.4 | 86.6s |

FULL used 53.6% fewer tokens per correct answer and 26.0% lower measured cost.
This matched screen remains the direct Cursor-rules comparison.

## Latest Sol governance optimization

[Workflow 30077217017](https://github.com/layer1labs/specsmith/actions/runs/30077217017)
ran a FULL-only five-repetition confirmation at commit `3d86308`. All five
cells passed the public checks and evaluator-isolated oracle, with no audit
weakness:

| FULL version | Correct | Tokens/correct | Mean input | Mean cost | Mean turns | Mean wall time |
|---|---:|---:|---:|---:|---:|---:|
| Prior matched screen | 5/5 | 32.0k | 25.4k | $0.2640 | 11.4 | 86.6s |
| Focused repair handoff | 5/5 | 28.3k | 21.7k | $0.2519 | 10.2 | 97.1s |

The controller supplied bounded current content when one validator identified
one repair file, then removed redundant read tools. Four of five earlier runs
spent a separate turn rereading that file; every comparable repair in the new
screen wrote immediately. TPCA fell 11.6%, input tokens 14.3%, turns 10.5%, and
measured cost 4.6%. Wall time increased in this sample, so no latency
improvement is claimed. The 28,314-token result became the versioned frontier
envelope at that commit and is retained here as the predecessor to the July 24
learning replay.

## July 24 learning replay

[Workflow 30093712102](https://github.com/layer1labs/specsmith/actions/runs/30093712102)
repeated Sol FULL at n=5 on final learning commit `708d47b`. The task now makes
the Go worker's non-empty `id` and `created_at` defaults explicit and validates
them publicly; an explicit future-action narration may receive a second
continuation only after the first recovery produced new expected-file writes.

| FULL version | Correct | TPCA | Mean input | Mean cost | Mean turns | First pass |
|---|---:|---:|---:|---:|---:|---:|
| Focused repair handoff | 5/5 | 28,314 | 21,725 | $0.2519 | 10.2 | 40% |
| Final learning replay | 5/5 | 26,499 | 20,204 | $0.2414 | 9.8 | 60% |

The final replay reduced TPCA by 6.4%, input tokens by 7.0%, measured cost by
4.2%, and turns by 3.9%, with no audit weakness. These are same-task point
estimates from separate complete screens, not pooled repetitions.

## Release-quality Sol confirmation

[Workflow 30099279843](https://github.com/layer1labs/specsmith/actions/runs/30099279843)
ran the unchanged Sol FULL controller at n=10 on commit `b327b8d`. All ten cells
passed the public validators and isolated oracle. The deterministic audit found
no weakness and selected `publish_or_expand`.

| Sol FULL screen | Correct | TPCA | Mean input | Mean output | Mean cost | Mean turns | Mean wall time | First pass |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Final learning n=5 | 5/5 | 26,499 | 20,204 | 6,294 | $0.2414 | 9.8 | — | 60% |
| Release-quality n=10 | 10/10 | 30,317 | 23,634 | 6,683 | $0.2767 | 10.3 | 85.8s | 20% |

This historical larger sample is 14.4% above the favorable n=5 point estimate and 7.1%
above the preceding 28,314-token n=5 screen, but remains 5.3% below the 32,020
matched n=5 screen. Its observed range was 23,316–36,108 tokens; the mean's
95% t-interval is approximately 27,573–33,061. The evidence therefore supports
100% observed correctness for that commit. It has been superseded by the
17,633.7-token July 25 release envelope above.

The preceding seven-route n=1 admission
[workflow 30091184259](https://github.com/layer1labs/specsmith/actions/runs/30091184259)
showed why older candidates should be repeated selectively:

| Managed route | Cursor | Specsmith FULL | Decision |
|---|---:|---:|---|
| Kimi K2.7 Code / DeepInfra | fail / 42.3k | pass / 24.0k | route confirmation required |
| Qwen3.6-35B-A3B / DeepInfra | fail / 163.9k | pass / 62.1k | governance gain, but 2.19× old Sol envelope |
| DeepSeek-V4 Pro / Novita | fail / 21.1k | fail / 74.9k | explicit completion narration repair |
| GLM-5.2 / DeepInfra | fail / 196.7k | fail / 24.6k | explicit milestone narration repair |
| MiniMax-M3 / Novita | fail / 26.3k | fail / 56.1k | empty/tool-continuation failure |
| DeepSeek-V4 Flash / DeepInfra | fail / 87.2k | fail / 130.1k | turn exhaustion; rejected |
| Nemotron 3 Ultra / DeepInfra | fail / 141.6k | fail / 119.4k | repeated tool loop; rejected |

The final-commit targeted confirmation
[workflow 30093614453](https://github.com/layer1labs/specsmith/actions/runs/30093614453)
made GLM correct at 73,618 tokens and DeepSeek Pro correct at 84,409. Both
remain diagnostic-only: the audit selects `advance_candidate`, not repetition,
because they are 2.6× and 2.98× the prior Sol envelope. MiniMax's additional
20,382-token attempt wrote no files after two empty continuations, so a native
tool-protocol or route change is required before another paid run.

Kimi's route confirmation separated model behavior from provider reliability.
The DeepInfra n=5 workflow
[30092473534](https://github.com/layer1labs/specsmith/actions/runs/30092473534)
returned router 504 pages for eight cells and was rejected as incomplete
evidence. Together then returned an account-level 403 during
[live probe 30096516180](https://github.com/layer1labs/specsmith/actions/runs/30096516180).
The exact Novita fallback completed one matched cell in
[workflow 30096796977](https://github.com/layer1labs/specsmith/actions/runs/30096796977):

| Kimi K2.7 Code / Novita | Correct | Tokens | Turns | Cost | Decision |
|---|---:|---:|---:|---:|---|
| Cursor Rules | no | 108,137 | 20 | $0.1129 | turn budget exhausted |
| Specsmith FULL | yes | 43,015 | 10 | $0.0735 | 60.2% fewer tokens, but above frontier |

FULL made Kimi correct while Cursor Rules failed. Its 43,015 TPCA is 1.62× the
then-current 26,499-token n=5 frontier and 1.42× the later 30,317-token
release-sized Sol envelope. Either comparison blocks an n=5 Kimi run. The
earlier 24,021-token DeepInfra observation remains a valid n=1 diagnostic, not
evidence that can be pooled across providers or commits.

## What changed the result

The improvement came from making governance smaller and more deterministic:

- accepted work starts with only read, write, and done tools;
- requirement-linked change boundaries replace broad repository exploration;
- file bodies are retrieved just in time and unchanged rereads become digest
  receipts;
- completed write bodies and superseded reads leave active provider history;
- validators run outside the model token path and return focused failures;
- long-horizon work receives controller-owned milestone progress without a
  separate planning turn; and
- tool surfaces expand only after a validation failure.

The next adaptive layer observes serving behavior rather than model branding.
After two one-action turns, FULL adds bounded `read_files`/`write_files`
operations (maximum 12 paths) and asks the route to batch the active boundary.
Scalar definitions remain available because some OpenAI-compatible routes keep
selecting a tool advertised earlier in the conversation. Completion may also
run one Ruff default-safe-fix pass before completion or final scoring. Public
task validators run before the hidden oracle, which is executed exactly once
after the agent stops and never supplies repair content.

## Qwen route diagnostic

[Workflow 29962883256](https://github.com/layer1labs/specsmith/actions/runs/29962883256)
ran T2, T11, and T28 once under Cursor rules and FULL. These are diagnostic
receipts only; none was advanced to n=5.

| Managed route | Cursor correct | FULL correct | Main finding |
|---|---:|---:|---|
| `Qwen/Qwen3.6-35B-A3B:deepinfra` | 2/3 | 1/3 | FULL T2: 19.3k vs Cursor 65.6k; T11/T28 exhausted turns; six cells took 35m23s |
| `Qwen/Qwen3-Coder-Next:novita` | 2/3 | 0/3 | Lower FULL tokens on T28, but serial repair and an acceptance gap prevented correctness |
| `Qwen/Qwen3-Coder-480B-A35B-Instruct:novita` | 0/3 | 0/3 | Larger active capacity did not overcome serial actions or incomplete T28 boundaries |

The evidence rejects “use the largest Qwen” as the next move. A focused
[Qwen3.6/DeepInfra adaptive rerun 29966620911](https://github.com/layer1labs/specsmith/actions/runs/29966620911)
then produced these n=1 results on the same T2/T11/T28 task set:

| Condition | Correct | Total tokens | Tokens/correct | Main finding |
|---|---:|---:|---:|---|
| Cursor rules | 1/3 | 358,653 | 358,653 | T11 passed; T2 and T28 failed |
| Specsmith FULL | 2/3 | 201,485 | 100,743 | T2/T11 passed; T28 failed |

Relative to the first Qwen3.6 diagnostic, adaptive FULL improved from 1/3 to
2/3 and reduced TPCA by 46.1%. T11 is the clearest causal trace: after two
scalar turns, the route used one composite write for the implementation and
test and passed in six turns. T28 wrote every declared file and passed its
public project checks, but the hidden oracle rejected an omitted required schema
field and generic Playwright locators. This public-test/oracle disagreement
motivated a visible contract validator and validator-to-file repair boundaries;
it did not justify a larger turn cap or n=5 promotion.

The focused [T28 contract-repair run 29969671380](https://github.com/layer1labs/specsmith/actions/runs/29969671380)
did not produce a correct cell:

| Condition | Correct | Tokens | Wall time | Final evidence |
|---|---:|---:|---:|---|
| Cursor rules | 0/1 | 183,061 | 354.5s | project tests passed; hidden oracle 4/5 |
| Specsmith FULL | 0/1 | 203,217 | 891.3s | project tests 10/10 and hidden oracle 5/5; final Ruff `I001` remained |

The visible contract validator repaired the former acceptance gap, but the
route's action policy remained inefficient. July 23 trace-driven experiments
then tested progressively stricter controller behavior:

| Workflow | Route / cell | Correct | Tokens | Turns | Evidence |
|---|---|---:|---:|---:|---|
| [30007255204](https://github.com/layer1labs/specsmith/actions/runs/30007255204) | Coder-Next/Novita, T28 FULL | no result | — | 0 | provider HTTP 400 before a model action |
| [30007554143](https://github.com/layer1labs/specsmith/actions/runs/30007554143) | Coder-Next/Novita, T2 FULL | no | 58,149 | 12 | no files written; route did not follow the advertised tool surface |
| [30009178814](https://github.com/layer1labs/specsmith/actions/runs/30009178814) | Qwen3.6/DeepInfra, T28 FULL | no | 107,749 | 20 | only five boundaries written; broad reread churn |
| [30010219286](https://github.com/layer1labs/specsmith/actions/runs/30010219286) | Qwen3.6/DeepInfra, T28 FULL | yes | 180,895 | 20 | all ten files, clean public checks, hidden oracle 5/5 |
| [30011743699](https://github.com/layer1labs/specsmith/actions/runs/30011743699) | Qwen3.6/DeepInfra, T28 FULL | no | 136,360 | 20 | 24.6% fewer tokens than the correct cell, but independent oracle failed |
| [30013020354](https://github.com/layer1labs/specsmith/actions/runs/30013020354) | Qwen3.6/DeepInfra, T28 FULL | no | 151,666 | 20 | hidden oracle 5/5; self-authored public tests and Ruff failed |

The sequence isolated and fixed real scaffold weaknesses: completed writes now
become digest evidence, known file absence is versioned, reads are suspended
when the next declared boundary is already known, repair writes return directly
to controller validation, and public T28 validators cover Go package and query
composition boundaries. Those changes reduced redundant context without
weakening the hidden oracle. They did not make the managed model reliable: only
one of three recent Qwen3.6 cells was correct, all reached the turn ceiling, and
the correct cell used 8.8× GPT-5.6 Sol FULL's 20.6k T28 TPCA.

No managed Qwen result is promoted to n=5. A stronger infrastructure experiment
is Qwen3-Coder-Next behind its native `qwen3_coder` parser in vLLM/SGLang or
Qwen Code/Qwen-Agent, where multi-step tool semantics are part of the serving
stack. The Novita runs are managed OpenAI-compatible route evidence, not native
parser evidence. The official model cards are
[Qwen3.6-35B-A3B](https://huggingface.co/Qwen/Qwen3.6-35B-A3B),
[Qwen3-Coder-Next](https://huggingface.co/Qwen/Qwen3-Coder-Next), and
[Qwen3-Coder-480B-A35B-Instruct](https://huggingface.co/Qwen/Qwen3-Coder-480B-A35B-Instruct).

The `Qwen3.6-35B-A3B-FP8` repository was not offered by a managed Hugging Face
Inference Provider during these probes. FP8 or a base model therefore belongs
in a separately labelled self-hosted lane; combining it with managed routes
would confound model quality, quantization, parser, and serving hardware.

## Benchmark-driven optimization loop

1. Run one matched diagnostic and fail closed on provider errors or missing
   cells.
2. Audit correctness, TPCA, turns, rereads, scope expansion, milestone progress,
   and public-test/oracle disagreement.
3. Convert a reproducible weakness into a linked requirement and independent
   regression test.
4. Change the smallest implicated controller or context boundary; do not raise
   turn caps or weaken the oracle.
5. Rerun only cells whose serving, prompt, validator, or controller path changed.
6. Rerun the complete matched slice after the last causal change. Advance to
   n=5 only after diagnostic correctness; use n=10 for release-quality
   statistical claims.

## Integrity and limitations

Every cell uses a disposable project and isolated governance state. Project
Ruff and pytest run before evaluator injection; the hidden acceptance oracle
runs once in isolation. Raw rows retain call-level token/cache usage, costs,
turns, stop reason, content-free tool targets, diffs, validator output, and
controller decisions. Comparisons reject missing, duplicate, uneven, errored,
or incompatible cells.

The current screen compares the repository's versioned Cursor-style condition,
not every feature of the commercial Cursor product. Prices and hosted latency
can change; raw correctness and token receipts are the more portable evidence.
See the [statistical methodology](https://github.com/layer1labs/specsmith/blob/develop/scripts/govern_bench/METHODOLOGY.md),
[model comparison](model-comparison.md), and
[long-horizon weakness audit](benchmark-audit.md).

## Historical provenance

Earlier screens remain available for regression history, but their headline
numbers are superseded by the current commit. Runs with unavailable routes,
tool incompatibility, incomplete artifacts, or cancelled model lanes never
enter a published denominator. In particular, workflow `29942515095` measured
T28 before adaptive change maps and milestone compression; workflow
`29944111036` measured an earlier Qwen3.6 serving configuration. They are not
combined with the current 80-row screen.
