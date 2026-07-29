# Specsmith Governance Efficiency Benchmark

## Current promotion and release protocol

Benchmark spend now follows locked, versioned profiles:

1. `admission`: one T28/FULL cell for a new model or route;
2. `controller-admission`: one T1, T10, T11, T13, and T28 FULL cell after controller changes;
3. `substitution-screen`: T1/T10/T13/T28, raw and FULL, n=5 for two-model
   capability-substitution evidence;
4. `substitution-release`: the complete eight-task raw/FULL 2×2 matrix at n=10
   for a lower-tier versus frontier release claim;
5. `release-controls`: T10/T13/T28, Cursor-style and FULL, n=10;
6. `broad-release`: the eight-task Cursor/FULL matrix at n=10 for one aggregate
   same-commit release claim.

Profile task, condition, and repetition overrides fail closed. A failed n=1
admission is repaired or rejected instead of repeated. The lower-tier-governed
versus frontier-ungoverned question requires all four matched counterfactuals,
not a comparison assembled from unrelated historical runs.

Release-grade substitution requires a paired 10,000-sample bootstrap, a
five-percentage-point correctness non-inferiority margin, and an upper 95% TPCA
ratio below one. Fixed-suite and task-cluster intervals are reported
separately. The latter tests robustness to resampling the benchmark's named
tasks; it is necessary but not sufficient for claims about fresh repositories
or new task families.

The FULL controller now keeps one compact five-tool schema throughout a run
and records its hash for cache-efficiency auditing. T1 preloads its versioned
implementation/public-test boundary; T10 adds its imported Todo model and
dependency manifest after admission proved them necessary. T11 adds only the
non-evaluator files repeated in every broad-run first action. T13 remains
retrieval-driven because its matching preload increased token use in
admission. T28 still receives only its active milestone. These changes target
retrieval turns without widening model-visible context or exposing evaluator
evidence.

## July 26 preregistered model-substitution release

[Workflow 30210886840](https://github.com/layer1labs/specsmith/actions/runs/30210886840)
completed the locked `substitution-release` profile at preregistered commit
`75a8c791`: eight tasks, four matched model/governance cells, ten repetitions,
and 320/320 valid rows.

| System | Correct | TPCA | Cost/pass |
|---|---:|---:|---:|
| Terra raw | 56/80 | 45,915 | $0.1642 |
| Terra + FULL | 80/80 | 11,737 | $0.0602 |
| Sol raw | 65/80 | 28,023 | $0.1511 |
| Sol + FULL | 80/80 | 8,082 | $0.0752 |

For the primary Terra+FULL versus Sol-raw comparison, the TPCA ratio was 0.419
(fixed-suite 95% interval 0.358–0.485; task-cluster interval 0.212–0.708).
Correctness-difference intervals were +3.3 to +34.1 percentage points and
−4.4 to +54.7 points. Both preregistered mixed-suite gates passed: Terra+FULL
used 58.1% lower TPCA and 60.1% lower estimated cost per pass.

The six coding tasks are reported separately:

| Coding-only system | Correct | TPCA | Cost/pass |
|---|---:|---:|---:|
| Terra + FULL | 60/60 | 15,649 | $0.0803 |
| Sol raw | 55/60 | 30,250 | $0.1691 |

The coding TPCA intervals favored Terra+FULL, but the fixed-suite correctness
lower bound was −5.7 points, 0.7 points below the preregistered −5-point
non-inferiority margin. The coding-only substitution gate therefore did not
pass. The supported result is capability substitution on this mixed benchmark
distribution, with robustness to resampling its eight named tasks—not general
equivalence on fresh repositories.

## July 26 final same-commit evidence

[Workflow 30206398622](https://github.com/layer1labs/specsmith/actions/runs/30206398622)
ran the locked eight-task n=10 release profile at commit `36435f2`. All 160
rows are valid and every coding cell passed in both conditions.

| Slice / condition | Correct | TPCA | Cost/pass | Mean turns | Total wall |
|---|---:|---:|---:|---:|---:|
| All tasks — Cursor-style | 70/80 | 24,839 | $0.1347 | 5.43 | 1,897s |
| All tasks — FULL | 80/80 | 10,691 | $0.0830 | 2.94 | 1,699s |
| Coding only — Cursor-style | 60/60 | 27,062 | $0.1496 | 6.33 | 1,791s |
| Coding only — FULL | 60/60 | 14,254 | $0.1096 | 3.92 | 1,699s |

FULL reduced all-task TPCA by 57.0%, cost/pass by 38.4%, turns by 45.9%, and
wall time by 10.4%. With equal coding correctness it reduced coding TPCA by
47.3%, cost/pass by 26.7%, and turns by 38.1%. T28 remained 10/10 at 17,955
versus 47,021 TPCA.

[Workflow 30206394966](https://github.com/layer1labs/specsmith/actions/runs/30206394966)
is the matched n=5 model-substitution screen:

| Four-task aggregate | Correct | TPCA | Cost/pass |
|---|---:|---:|---:|
| Sol raw | 20/20 | 29,161 | $0.1679 |
| Sol FULL | 20/20 | 13,502 | $0.1192 |
| Terra raw | 16/20 | 64,759 | $0.2207 |
| Terra FULL | 20/20 | 19,053 | $0.0952 |

Terra+FULL matched Sol-raw correctness while using 34.7% lower TPCA and 43.3%
lower cost/pass. The advantage is not uniform: Terra+FULL costs more tokens on
T1/T10, but wins materially on T13/T28. Terra raw's lower correctness confirms
that the result is governance lift, not Terra alone.

The broad audit found no governed correctness failure. It did identify a T11
retrieval/repair hotspot and elevated T13 variance. In the post-run
[controller admission 30209142281](https://github.com/layer1labs/specsmith/actions/runs/30209142281),
T11's bounded context cut the cell from 23,472 tokens and six turns to 11,210
tokens and two turns. T13's matching preload increased the cell from 14,424 to
16,190 tokens, so it was removed. Both tasks remain in controller admission.
These diagnostics are not pooled into the immutable `36435f2` evidence.

## July 26 locked-profile admissions

The first locked admissions at commit `04dbabb` correctly prevented premature
repetition:

| Workflow / model | Profile | Correct | Tokens | Turns | Decision |
|---|---|---:|---:|---:|---|
| [30205541608](https://github.com/layer1labs/specsmith/actions/runs/30205541608) · Qwen3.6-35B-A3B/DeepInfra | T28/FULL | 1/1 | 67,701 | 12 | reject repetition |
| [30205537706](https://github.com/layer1labs/specsmith/actions/runs/30205537706) · GPT-5.6 Sol | T1/T10/T28 FULL | 3/3 | 20,603 / 63,128 / 17,981 | 5 / 11 / 5 | optimize and readmit |

Qwen used one stable schema and improved materially over its earlier 129,905
token correct diagnostic, but remained 3.87× the release T28 anchor and began
with a broad scope request. It therefore does not earn an n=5 substitution
screen.

Sol's T28 control remained within 2.7% of the 17,502-token anchor. T1 was a
repair outlier, while T10 exposed a controller defect: the preload omitted
`app/models.py` and `pyproject.toml`, then the global read suspension denied
the model's request for exactly those dependencies. Guessing produced three
contract-repair cycles. The repair adds those two bounded dependency files,
strengthens side-effect-free test guidance, and adds T1/T10/T13 release
envelopes so same-model controller regressions fail admission automatically.

The repaired controller readmission in
[workflow 30206236593](https://github.com/layer1labs/specsmith/actions/runs/30206236593)
passed all three cells with one stable schema per row:

| Task | Before repair | After repair | Release anchor | After turns |
|---|---:|---:|---:|---:|
| T1 | 20,603 | 7,845 | 10,216 | 2 |
| T10 | 63,128 | 9,305 | 13,842 | 2 |
| T28 | 17,981 | 17,818 | 17,502 | 5 |

T1 and T10 are now 23.2% and 32.8% below their release anchors; T28 is 1.8%
above its anchor. The audit found only expected n=1 undersampling and selected
`repeat_screen`.

The parallel weaker-model admission
[workflow 30206263461](https://github.com/layer1labs/specsmith/actions/runs/30206263461)
also passed both T28 cells. Luna used 43,112 tokens and eleven turns, so the
audit rejected repetition. Terra used 17,655 tokens, five turns, and $0.1157:
within 0.9% of the Sol FULL token anchor at roughly half this admission's
measured Sol cost. Terra therefore advances to the complete matched n=5
raw/FULL substitution screen against Sol.

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

## Reasoning-capable 20B–32B admission

[Workflow 30264387650](https://github.com/layer1labs/specsmith/actions/runs/30264387650)
screened four exact Hugging Face routes on one T28/FULL cell at commit
`0e6ca75a`. A green workflow means the artifact was produced, not that the
task passed:

| Exact model route | Correct | Tokens | Turns | Stop |
|---|---:|---:|---:|---|
| `Qwen/Qwen3.6-27B:deepinfra` | no | 11,208 | 3 | narrated the next milestone without a tool |
| `openai/gpt-oss-20b:nscale` | no | 85,438 | 12 | empty response after repeated suppressed reads |
| `Qwen/Qwen3-Coder-30B-A3B-Instruct:scaleway` | no | 122,892 | 20 | serialized actions and exhausted the cap |
| `zai-org/GLM-4.7-Flash:deepinfra` | no | 54,309 | 8 | empty response after partial API repair |

The Qwen3.6 trace had already completed and validated the first milestone.
Its exact narration, “Now implementing Milestone 2,” was missing from the
bounded continuation detector. The controller now recognizes that phrase,
gives one forceful recovery after a model requests already-supplied evidence,
and stops after three ignored suppressed reads. The audit reports the latter
as `suppressed_read_loop`.

The identical Qwen3.6 admission then passed in
[workflow 30265818081](https://github.com/layer1labs/specsmith/actions/runs/30265818081)
at commit `4bb1bf1`: all ten declared files, public checks, and the independent
oracle passed in 14 model turns, 72,255 tokens, and $0.0812 on the pinned
route. This is a capability result for a published 27B model, but it is 4.13×
the 17,501.7-token governed Sol T28 envelope. The deterministic audit returned
`advance_candidate`, not repetition.

The nearest additional managed tool-capable checkpoint,
`Qwen/Qwen3-32B:deepinfra`, failed
[workflow 30265830535](https://github.com/layer1labs/specsmith/actions/runs/30265830535)
after 63,636 tokens and six turns. Phi-4 Reasoning Plus, Devstral Small 2 24B,
and current 14B Mistral candidates did not have a managed Hugging Face router
mapping for this credential path; DeepSeek-R1-Distill-Qwen-14B did not
advertise tool support. They were rejected at route selection rather than
misreported as benchmark failures.

The result narrows the claim precisely: Specsmith can help a 27B model finish
this controlled long-horizon task, but the current serving/controller pair
does not replace frontier Sol on token efficiency. No n=5 spend is justified
from that result; later sections test parser, patch, and other serving-boundary
changes rather than pooling them as repetitions.

Two final causal checks closed this managed-route loop. Finish-reason
telemetry and scalar fallback after an invalid composite payload produced a
33,884-token failure in
[workflow 30268327224](https://github.com/layer1labs/specsmith/actions/runs/30268327224);
the model stopped while promising Milestone 2. Extending the same bounded
future-action recovery yielded a second correct cell in
[workflow 30269000016](https://github.com/layer1labs/specsmith/actions/runs/30269000016):
77,776 tokens, 14 turns, all ten files, and a passing independent oracle.
Every provider finish reason was `tool_calls` or `stop`, ruling out output
truncation for that run. The confirmation is 7.6% more expensive than the
72,255-token pass and 4.44× the Sol envelope. The optimization produced no
TPCA gain, so the audit returned `advance_candidate` and managed DeepInfra
repetition stops here.

### July 27 controller protocol isolation

The next same-task diagnostics isolated tool schema, tool choice, context
replacement, and evidence authority without changing T28 or its hidden oracle.
Each row is an independent n=1 cell and is not pooled across commits.

| Workflow · controller variant | Correct | Tokens | Turns | Finding |
|---|---:|---:|---:|---|
| [30274870047](https://github.com/layer1labs/specsmith/actions/runs/30274870047) · required tools | yes | 42,697 | 9 | forcing any tool remained correct but increased serial repair |
| [30274872374](https://github.com/layer1labs/specsmith/actions/runs/30274872374) · scalar parallel | yes | **26,850** | **6** | parallel scalar writes avoided the route's unreliable nested arrays |
| [30274875030](https://github.com/layer1labs/specsmith/actions/runs/30274875030) · scalar + required | censored | 19,463 | 5 | Hugging Face 504 after six files |
| [30274877475](https://github.com/layer1labs/specsmith/actions/runs/30274877475) · scalar + required + compact | censored | 44,977 | 9 | Hugging Face 504 after repair churn |
| [30277090373](https://github.com/layer1labs/specsmith/actions/runs/30277090373) · compact auto | no | 11,726 | 3 | promised the UI batch without emitting tools |
| [30277092347](https://github.com/layer1labs/specsmith/actions/runs/30277092347) · write only | yes | 37,058 | 8 | removed the initial read but implementation repairs erased the saving |
| [30278261221](https://github.com/layer1labs/specsmith/actions/runs/30278261221) · repaired compact auto | no | 126,495 | 20 | lost useful continuity and oscillated between API contracts |
| [30280275590](https://github.com/layer1labs/specsmith/actions/runs/30280275590) · validator authority | yes | 43,622 | 10 | independent evidence converged, but did not improve TPCA |

The 26,850-token scalar-parallel result is 62.8% below the earlier
72,255-token correct admission and 65.5% below its 77,776-token confirmation.
It is still 1.53× the 17,501.7-token governed Sol envelope and remains an n=1
diagnostic. Therefore it supports a concrete controller improvement, not a
small-model substitution claim or n=5 promotion.

The experiment also identifies the stable design: keep automatic tool choice,
use simple scalar file schemas, ask for independent calls in one response,
validate milestone boundaries deterministically, and give independent
validators authority over tests authored by the same model run. Aggressive
history replacement, global required-tool forcing, and removing reads did not
improve the correct-answer cost.

### Native editing, fixed-scalar bundles, and managed route isolation

The next n=1 diagnostics changed only the model route or provider-visible file
operation. They retain the same T28 task, public validators, hidden oracle, and
bounded controller:

| Workflow · route/interface | Correct | Tokens | Turns | Files | Finding |
|---|---:|---:|---:|---:|---|
| [30286692090](https://github.com/layer1labs/specsmith/actions/runs/30286692090) · Coder-Next/Novita scalar | no | 78,742 | 15 | 4/10 | serialized writes and repeated loop |
| [30286692090](https://github.com/layer1labs/specsmith/actions/runs/30286692090) · Coder-480B/Novita scalar | no | 57,251 | 12 | 4/10 | text stop; model swap alone did not help |
| [30287970034](https://github.com/layer1labs/specsmith/actions/runs/30287970034) · Qwen3.6 exact edit | no | 26,234 | 7 | 3/10 | one-hunk repair could not keep coupled import and annotation changes |
| [30287972114](https://github.com/layer1labs/specsmith/actions/runs/30287972114) · Qwen3.6 milestone bundle | no | 43,491 | 8 | 3/10 | rejected payloads exposed a loop-accounting defect |
| [30287972114](https://github.com/layer1labs/specsmith/actions/runs/30287972114) · Coder-480B milestone bundle | no | 82,049 | 15 | 8/10 | throughput improved, correctness did not |
| [30289264577](https://github.com/layer1labs/specsmith/actions/runs/30289264577) · evidence-aware exact edit | no | 27,815 | 6 | 3/10 | unchanged validator evidence correctly stopped repeated ineffective patches |
| [30289266484](https://github.com/layer1labs/specsmith/actions/runs/30289266484) · evidence-aware Qwen3.6 bundle | **yes** | 71,090 | 13 | 10/10 | fixed scalar bundle restored public and oracle correctness |
| [30289266484](https://github.com/layer1labs/specsmith/actions/runs/30289266484) · evidence-aware Coder-480B bundle | no | 122,567 | 20 | 7/10 | turn cap and 10.7:1 input/output ratio |

The loop guard now counts only successful writes and treats a same-file repair
as repeated only when normalized authoritative validator evidence is unchanged.
The native `patch_file` control applies up to three exact non-overlapping hunks
atomically, with no write unless every hunk validates. Its first live run,
[30290375485](https://github.com/layer1labs/specsmith/actions/runs/30290375485),
was censored by an HTML 504 after 15,128 tokens; the one prescribed retry,
[30291702747](https://github.com/layer1labs/specsmith/actions/runs/30291702747),
failed at the route-availability probe. Neither row is correctness or efficiency
evidence.

This closes the managed-route decision. The bundle proves that provider-visible
tool structure can restore correctness, but its 71,090 TPCA is 4.06× the
17,501.7-token Sol envelope and 2.65× the 26,850-token scalar winner. This
closed further DeepInfra repetition and advanced the atomic patch to the hosted
route and literal-parser experiments below.

### Hosted native-tool and literal-parser isolation

The next route used `Qwen/Qwen3-Coder-30B-A3B-Instruct:scaleway`. It passed an
exact structured-tool probe before each paid cell, but the hosted service does
not expose its server-side parser flag; these rows are native-tool route
evidence, not proof of literal `qwen3_xml`.

| Workflow · controller | Correct | Tokens | Cost | Turns | Wall time | Finding |
|---|---:|---:|---:|---:|---:|---|
| [30317439173](https://github.com/layer1labs/specsmith/actions/runs/30317439173) · atomic patch | no | 123,384 | $0.040616 | 20 | 137.44 s | 4/10 files; turn exhaustion |
| [30317963475](https://github.com/layer1labs/specsmith/actions/runs/30317963475) · scoped atomic patch | no | 34,892 | $0.010609 | 10 | 29.86 s | 3/10 files; premature text stop |
| [30318295306](https://github.com/layer1labs/specsmith/actions/runs/30318295306) · scoped + required tools | no | 81,648 | $0.040819 | 13 | 209.69 s | one file; repeated three-action batch and empty response |

Scoping cut failed-run tokens by 71.7%, estimated cost by 73.9%, rework turns
by 73.3%, and wall time by 78.3% relative to the hosted baseline. Because all
three cells failed the unchanged independent oracle, TPCA remains undefined.
Forcing tools reversed much of the saving and is rejected. The trace instead
earned a deterministic repeated-batch guard: an identical multi-file action
batch receives bounded recovery and stops on its fourth occurrence, using only
content-free target and argument digests.

The literal parser lane initially produced censored infrastructure workflow
[30317300977](https://github.com/layer1labs/specsmith/actions/runs/30317300977).
After the endpoint-write permission was corrected,
[30358919239](https://github.com/layer1labs/specsmith/actions/runs/30358919239)
and
[30359943752](https://github.com/layer1labs/specsmith/actions/runs/30359943752)
successfully provisioned `Qwen3-Coder-30B-A3B-Instruct-FP8` on vLLM `v0.24.0`
with `qwen3_xml`, one L40S GPU, a 32k context, zero provider retries, and exact
required-tool probes. Both endpoint receipts confirm pause and deletion.

| Workflow · literal-parser policy | Correct | Tokens | Turns | Wall time | Finding |
|---|---:|---:|---:|---:|---|
| [30358919239](https://github.com/layer1labs/specsmith/actions/runs/30358919239) · atomic patch | no | 34,146 | 9 | 29.15 s | 3/10 files; promised a repair but stopped on prose |
| [30358919239](https://github.com/layer1labs/specsmith/actions/runs/30358919239) · scoped atomic patch | no | 53,451 | 11 | 74.89 s | 3/10 files; scoped context increased failure spend |
| [30359943752](https://github.com/layer1labs/specsmith/actions/runs/30359943752) · scoped + required tools | no | 181,884 | 20 | 372.75 s | 5/10 files; truncation and milestone fragmentation exhausted the cap |

The two ephemeral endpoint receipts report approximately `$0.166508` and
`$0.264469`, or `$0.430977` total. Native parsing removed the hosted route
ambiguity but did not produce correctness. Global required-tool forcing removed
premature prose stops at more than five times the best literal-parser failure
tokens, so it is rejected. No literal-parser row has defined TPCA, and none is
eligible for paid repetition.

### Milestone packets and evidence authority

Three later workflows compiled T28 into bounded active work packets and recorded
milestone yield explicitly. All used the same FP8 checkpoint, native
`qwen3_xml` parser, task, hidden oracle, and 20-turn cap.

| Workflow · policy | Correct | Tokens | Turns | Milestones | Wall time | Finding |
|---|---:|---:|---:|---:|---:|---|
| [30367659754](https://github.com/layer1labs/specsmith/actions/runs/30367659754) · packet only | no | 108,021 | 20 | 1/4 | 205.37 s | serialized repair exhausted the cap |
| [30367659754](https://github.com/layer1labs/specsmith/actions/runs/30367659754) · packet + one-turn adaptive | no | 112,933 | 17 | 1/4 | 187.62 s | one required recovery fired, then prose stop |
| [30369089983](https://github.com/layer1labs/specsmith/actions/runs/30369089983) · validator authority + atomic repair | no | 18,646 | 5 | 1/4 | 36.30 s | two native patches; fail-fast after prose |
| [30370203101](https://github.com/layer1labs/specsmith/actions/runs/30370203101) · authority v2 + repeated forcing | no | 98,679 | 20 | 1/4 | 169.75 s | identical already-applied patch loop |

Validator authority withheld contradictory tests authored by the same model run
and selected one independent repair boundary. Combined with a repair-only atomic
surface, it reduced failed-run tokens by 82.7% relative to packet-only. That is
a large failure-cost improvement, not a TPCA result: public tests and the hidden
oracle still failed. V2 then proved that repeatedly forcing tools converts prose
failure into expensive no-op looping; it is rejected.

The final trace earned a content-free single-action no-op guard. One identical
no-op receives recovery and the second stops the loop. Compact evidence schema
v2 now preserves milestone completion and tokens per completed milestone while
continuing to exclude prompts, diffs, validator output, governance decisions,
and transcripts. The three endpoint receipts confirm pause and deletion and
report approximately `$0.564815` combined compute cost.

### Research-aligned next improvements

The traces agree with several independent systems results:

- [Agentless](https://arxiv.org/abs/2407.01489) found that deterministic
  localization, repair, and patch validation can outperform a more elaborate
  autonomous loop at low cost. Specsmith should keep milestone selection and
  validation controller-owned rather than add more general-purpose skills or
  agents.
- [SWE-agent](https://arxiv.org/abs/2405.15793) shows that the editing
  interface materially changes coding performance. The next A/B test should
  compare full-file replacement with a bounded patch tool on the identical
  T28 route and oracle.
- [Less Context, Better Agents](https://arxiv.org/abs/2606.10209) reports that
  retaining a short recent tool window plus compact summaries can improve both
  correctness and token use. Specsmith already replaces stale reads with
  receipts; the next measurement should retain finish reason, truncation, and
  only the latest active repair evidence.
- The [LLM-Tool Compiler](https://arxiv.org/abs/2405.17438) reports lower token
  cost from fused parallel calls. Specsmith's composite tools pursue the same
  goal, but the Qwen traces show that a generic JSON array is not reliable
  across serving routes. Native parser compatibility must be an admission
  dimension, not a model footnote.
- [FrugalGPT](https://arxiv.org/abs/2305.05176) supports cascaded routing.
  Specsmith's safe version is evidence-based escalation: deterministic gates
  first, then a lower-cost model only inside a proven task envelope, with a
  frontier fallback when correctness or loop guards fail.

These are experiment candidates, not claims of improvement. The atomic-edit,
active-packet, evidence-authority, and no-op controls have now been tested; none
made native Qwen 30B correct. A new candidate must change the model or serving
capability, not merely repeat forcing. It must beat the current exact-route cell
without weakening tests, hidden oracles, or stop bounds.

### Native Responses route screen

The accepted validator-authority, milestone-packet, repair-only atomic
controller was held constant while only the serving interface changed from
Chat Completions compatibility mode to native Responses function tools.

| Workflow | Model | Correct | TPCA | Mean cost | Turns | Audit |
|---|---|---:|---:|---:|---:|---|
| [30412677765](https://github.com/layer1labs/specsmith/actions/runs/30412677765) | GPT-5.6 Sol | 1/1 | 18,474 | $0.2590 | 5 | n=1 diagnostic; repeat eligible |
| [30412913235](https://github.com/layer1labs/specsmith/actions/runs/30412913235) | GPT-5.6 Terra | 1/1 | 17,014 | $0.1147 | 5 | n=1 diagnostic; repeat eligible |
| [30413249488](https://github.com/layer1labs/specsmith/actions/runs/30413249488) | GPT-5.6 Terra | 5/5 | 17,213 | $0.1176 | 5 | clean screen; expand to n=10 |
| [30414435928](https://github.com/layer1labs/specsmith/actions/runs/30414435928) | GPT-5.6 Luna | 0/1 | undefined (72,880 used) | undefined ($0.1823 spent) | 20 | reject repetition; repair schema |
| [30415300896](https://github.com/layer1labs/specsmith/actions/runs/30415300896) | GPT-5.6 Luna, strict schema | 1/1 | 18,798 | $0.0532 | 5 | correct repair admission; repeat eligible |
| [30415451446](https://github.com/layer1labs/specsmith/actions/runs/30415451446) | GPT-5.6 Luna, strict schema | 5/5 | 31,685 | $0.1137 | 6.2 | correct but token/first-pass regression; reject repetition |
| [30416984775](https://github.com/layer1labs/specsmith/actions/runs/30416984775) | GPT-5.6 Sol, stable-schema v3 | 1/1 | 19,288 | $0.2597 | 5 | correct; 1.10× release anchor; reject repetition |
| [30417839826](https://github.com/layer1labs/specsmith/actions/runs/30417839826) | GPT-5.6 Sol, structured v4 | 1/1 | 17,844 | $0.2582 | 5 | correct; promote to n=5 |
| [30418033123](https://github.com/layer1labs/specsmith/actions/runs/30418033123) | GPT-5.6 Sol, structured v4 | 5/5 | 17,912 | $0.2540 | 5 | clean screen; promote to n=10 |
| [30418513274](https://github.com/layer1labs/specsmith/actions/runs/30418513274) | GPT-5.6 Sol, structured v4 | 10/10 | 17,907 | $0.2501 | 5 | release-sized; publish or expand |

Every successful Sol and Terra row passed public validators and the hidden
oracle, completed all four milestones, and used one implementation attempt
with no repair cycle. The Terra
n=5 range was 16,777–17,411 tokens; mean wall time was 45.9 seconds. Relative
to the Sol native diagnostic, Terra's screen used 6.8% fewer mean tokens and
54.6% lower mean cost. The separately measured July 25 Sol release envelope
remains the release-quality comparator: this one-task n=5 screen does not
replace a matched n=10 claim.

The route defaults to low reasoning effort and low verbosity, has separate
provenance, fails closed unless a two-step live probe emits the required
function call and then continues after its output, and reuses server-side state
only across an exact history prefix. Controller compaction intentionally
invalidated continuation in these cells; implicit prompt caching still reached
5,886 mean cached input tokens in the five-run screen. The next causal
admission tested the separately labeled Luna route. Optional generic preload
now excludes files already supplied by an authoritative milestone packet,
preventing duplicate or stale file bodies without changing the default
zero-byte preload.

Luna initially selected `write_milestone` but failed its argument contract
fourteen times because used `content_N` values were not strings. Requiring all
fixed slots, making unused slots nullable, and enforcing provider strictness
removed every serialization failure: the repair admission used 74.2% fewer
tokens and 75% fewer turns. The five-run confirmation was correct in every row,
but ranged from 18,102 to 58,624 tokens, averaged 84.1% more tokens than Terra,
and completed first-pass in only 2/5 rows. Repairs repeatedly targeted
`backend/main.py`; two rows also emitted empty milestone packets, and repair
phases changed the provider-visible tool hash. Luna is therefore not promoted.

Stable-schema v3 then passed its Sol diagnostic with one unchanged tool hash,
all four milestones, and no repair. At 19,288 tokens it was nevertheless 10%
above the 17,502-token release anchor, so the audit returned
`optimize_and_rerun`. Compared with the earlier native Sol admission, strict
fixed/null schemas added roughly 120–160 input tokens per turn without a repair
benefit.

Structured v4 changed only that serialization boundary. It uses one
provider-strict bounded array of `{path, content}` objects for multi-file
milestones and retains `write_file` for the single-file milestone. Local
execution validates the complete payload before an atomic write. The T28 task
file, hidden oracle, validators, milestone sequencing, 20-turn ceiling, low
effort/verbosity, request deadlines, and zero provider retries remained
unchanged.

Admission passed at 17,844 tokens. The earned n=5 screen passed 5/5 at 17,912
mean TPCA, then an independent n=10 confirmation passed 10/10 at 17,907 mean
TPCA (17,436–18,356), $0.2501 mean cost, five turns, 100% first-pass, and 1.77%
CV. Every row completed all four milestones and retained one tool-schema hash.
Relative to v3, the release-sized mean is 7.2% lower; it is 3.1% below the
earlier native Sol admission and 2.3% above the established 17,502-token
release anchor. The audit returned `publish_or_expand` with no correctness or
efficiency blocker. Its only low-severity note was provider cache
discontinuity; preserving server history would retain stale source bodies, so
this cycle keeps bounded epistemic compression and freezes v4.

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
