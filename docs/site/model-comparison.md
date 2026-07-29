# Governance Efficiency Model Comparison

## Governance as model-capability substitution

The comparison asks a stricter question than “which model scores best?”: can a
lower-tier model with Specsmith match a frontier ungoverned model at lower
tokens per correct answer or cost per pass?

GovernanceBench now reports that result only from a complete matched 2×2
experiment:

| Required cell | What it isolates |
|---|---|
| lower-tier + raw | lower-tier route baseline |
| lower-tier + FULL | governance-assisted candidate |
| frontier + raw | substitution target |
| frontier + FULL | governance lift at the frontier |

The locked `substitution-screen` uses T1, T10, T13, and T28 with five
repetitions per cell. The release profile uses all eight tasks at n=10. The
lower-tier+FULL headline must preserve correctness against frontier raw; lower
token or dollar cost cannot compensate for fewer correct outcomes. One-run
admission remains mandatory before repeated spend.

The preregistered release
[workflow 30210886840](https://github.com/layer1labs/specsmith/actions/runs/30210886840)
completed 320/320 valid cells. Terra+FULL passed 80/80 at 11.7k TPCA versus
Sol raw at 65/80 and 28.0k. Mixed-suite fixed-suite and task-cluster gates
passed. The coding-only sensitivity was 60/60 at 15.6k versus 55/60 at 30.3k,
but its correctness lower bound missed the non-inferiority margin by 0.7
percentage points. The supported claim is therefore mixed-suite,
task-conditional substitution—not general small-model replacement.

## Evidence levels

| Evidence | Model/routes | Repetitions | Treatment |
|---|---|---:|---|
| [30210886840](https://github.com/layer1labs/specsmith/actions/runs/30210886840) | GPT-5.6 Terra + Sol | 10 per eight tasks × raw/FULL | 320 valid; mixed-suite substitution gates pass; coding-only gate is inconclusive |
| [30413249488](https://github.com/layer1labs/specsmith/actions/runs/30413249488) | GPT-5.6 Terra / native Responses | 5 T28 FULL | 5/5 correct at 17.2k TPCA, $0.1176 mean cost, five turns, clean audit |
| [30412913235](https://github.com/layer1labs/specsmith/actions/runs/30412913235) | GPT-5.6 Terra / native Responses | 1 T28 FULL | Correct at 17.0k TPCA; promoted to n=5 |
| [30412677765](https://github.com/layer1labs/specsmith/actions/runs/30412677765) | GPT-5.6 Sol / native Responses | 1 T28 FULL | Correct at 18.5k TPCA; native tool/continuation route admitted |
| [30414435928](https://github.com/layer1labs/specsmith/actions/runs/30414435928) | GPT-5.6 Luna / native Responses | 1 T28 FULL | Failed at 72.9k/20 turns; non-string milestone content blocked 14 calls; 3/4 milestones |
| [30209142281](https://github.com/layer1labs/specsmith/actions/runs/30209142281) | GPT-5.6 Sol | 1 per T1/T10/T11/T13/T28 FULL | Post-broad admission: T11 improved to 11.2k/2 turns; T13 preload regressed and was removed |
| [30206398622](https://github.com/layer1labs/specsmith/actions/runs/30206398622) | GPT-5.6 Sol | 10 per eight tasks × Cursor/FULL | 160 valid; FULL 80/80 at 10.7k, Cursor 70/80 at 24.8k TPCA |
| [30206394966](https://github.com/layer1labs/specsmith/actions/runs/30206394966) | GPT-5.6 Terra + Sol | 5 per T1/T10/T13/T28 × raw/FULL | Terra+FULL 20/20 at 19.1k; Sol raw 20/20 at 29.2k TPCA |
| [30206263461](https://github.com/layer1labs/specsmith/actions/runs/30206263461) | GPT-5.6 Luna + Terra | 1 T28 FULL each | Both correct; Luna rejected at 43.1k, Terra promoted at 17.7k TPCA |
| [30206236593](https://github.com/layer1labs/specsmith/actions/runs/30206236593) | GPT-5.6 Sol | 1 each T1/T10/T28 FULL | Repair readmission: 7.8k / 9.3k / 17.8k, all correct; promoted |
| [30205541608](https://github.com/layer1labs/specsmith/actions/runs/30205541608) | Qwen3.6-35B-A3B / DeepInfra | 1 T28 FULL | Correct at 67.7k TPCA, 3.87× Sol anchor; rejected before n=5 |
| [30205537706](https://github.com/layer1labs/specsmith/actions/runs/30205537706) | GPT-5.6 Sol | 1 each T1/T10/T28 FULL | 3/3 correct; T10 controller regression triggered repair/readmission |
| [30199359636](https://github.com/layer1labs/specsmith/actions/runs/30199359636) | GPT-5.6 Sol | 10 per eight tasks × two conditions | Current broad diagnostic: FULL 74/80 at 10.1k TPCA; Cursor-style 70/80 at 23.9k; blocked by T10/T13 correctness |
| [30201998763](https://github.com/layer1labs/specsmith/actions/runs/30201998763) | GPT-5.6 Sol | 10 per T10/T13 condition | Post-repair confirmation: 40/40 correct; FULL 12.3k versus Cursor-style 30.2k TPCA; no high/critical finding |
| [30180171688](https://github.com/layer1labs/specsmith/actions/runs/30180171688) | GPT-5.6 Sol | 5 per eight tasks × two conditions | Prior broad screen: FULL 40/40 at 8.0k TPCA; Cursor-style 35/40 at 23.1k |
| [30179751802](https://github.com/layer1labs/specsmith/actions/runs/30179751802) | GPT-5.6 Sol | 10 T28 FULL | Prior standalone control: 10/10, 17.6k TPCA, five turns, no audit weakness |
| [30179361862](https://github.com/layer1labs/specsmith/actions/runs/30179361862) | GPT-5.6 Sol | 5 per T28 condition | Prior matched control: both 5/5; FULL 17.7k versus Cursor-style 36.5k TPCA |
| [30180139456](https://github.com/layer1labs/specsmith/actions/runs/30180139456) | Qwen3.6, Qwen3-Coder-480B, GLM-5.2 | 1 T28 FULL each | Validator-repair replay: only Qwen3.6 passed, at 129.9k TPCA; no candidate promoted |
| [30099279843](https://github.com/layer1labs/specsmith/actions/runs/30099279843) | GPT-5.6 Sol | 10 T28 FULL | Release-quality control: 10/10, 30.3k TPCA, no audit weakness |
| [30093712102](https://github.com/layer1labs/specsmith/actions/runs/30093712102) | GPT-5.6 Sol | 5 T28 FULL | Final learning commit: 5/5, 26.5k TPCA, no audit weakness |
| [30093614453](https://github.com/layer1labs/specsmith/actions/runs/30093614453) | DeepSeek-V4 Pro + GLM-5.2 | 1 T28 FULL each | Both correct after targeted repairs; 84.4k and 73.6k TPCA, not promoted |
| [30091184259](https://github.com/layer1labs/specsmith/actions/runs/30091184259) | Seven managed frontier routes | 1 per T28 condition | Admission/trace screen; only Kimi and Qwen FULL passed |
| [30092473534](https://github.com/layer1labs/specsmith/actions/runs/30092473534) | Kimi K2.7 Code / DeepInfra | requested 5 per condition | Rejected incomplete artifact; eight router 504 cells |
| [30096516180](https://github.com/layer1labs/specsmith/actions/runs/30096516180) | Kimi K2.7 Code / Together | live probe | Account-level HTTP 403; no benchmark cell |
| [30096796977](https://github.com/layer1labs/specsmith/actions/runs/30096796977) | Kimi K2.7 Code / Novita | 1 per T28 condition | Cursor failed at 108.1k; FULL passed at 43.0k |
| [30077217017](https://github.com/layer1labs/specsmith/actions/runs/30077217017) | GPT-5.6 Sol | 5 T28 FULL | Superseded optimized envelope: 5/5, 28.3k TPCA |
| [30045327768](https://github.com/layer1labs/specsmith/actions/runs/30045327768) | GPT-5.6 Sol | 5 per T28 condition | Historical matched Cursor/FULL comparator |
| [30076208564](https://github.com/layer1labs/specsmith/actions/runs/30076208564) | DeepSeek-V4 Pro / Novita | 1 FULL | Correct diagnostic; 47.9k TPCA, not promoted |
| [30074528288](https://github.com/layer1labs/specsmith/actions/runs/30074528288) | Kimi K2.7 Code / DeepInfra | 1 FULL | Correct diagnostic; 101.7k TPCA, not promoted |
| [30045980234](https://github.com/layer1labs/specsmith/actions/runs/30045980234) | GLM-5.2 / DeepInfra | 1 FULL | Correct diagnostic; 72.2k TPCA, not promoted |
| [30075176235](https://github.com/layer1labs/specsmith/actions/runs/30075176235), [30075720489](https://github.com/layer1labs/specsmith/actions/runs/30075720489) | MiniMax-M3 / Novita | 1 each | Two failed diagnostics; text-only then empty-response stops |
| [30077072490](https://github.com/layer1labs/specsmith/actions/runs/30077072490), [30077459159](https://github.com/layer1labs/specsmith/actions/runs/30077459159), [30077929145](https://github.com/layer1labs/specsmith/actions/runs/30077929145), [30078601832](https://github.com/layer1labs/specsmith/actions/runs/30078601832) | GPT-OSS-120B / DeepInfra then Novita | 1 each | Four failed provider, serialization, and completion-protocol diagnostics; rejected |
| [29963772623](https://github.com/layer1labs/specsmith/actions/runs/29963772623) + [29963515885](https://github.com/layer1labs/specsmith/actions/runs/29963515885) | GPT-5.6 Sol | 5 per task/condition | Current eight-task matched screen |
| [30010219286](https://github.com/layer1labs/specsmith/actions/runs/30010219286), [30011743699](https://github.com/layer1labs/specsmith/actions/runs/30011743699), [30013020354](https://github.com/layer1labs/specsmith/actions/runs/30013020354) | Qwen3.6-35B-A3B / DeepInfra | 1 each | Trace-driven T28 diagnostics; never combined |
| [30007255204](https://github.com/layer1labs/specsmith/actions/runs/30007255204), [30007554143](https://github.com/layer1labs/specsmith/actions/runs/30007554143) | Qwen3-Coder-Next / Novita | 1 each | Provider/tool-route admission failures |
| [29969671380](https://github.com/layer1labs/specsmith/actions/runs/29969671380) | Qwen3.6-35B-A3B / DeepInfra | 1 | T28 contract-repair diagnostic |
| [29966620911](https://github.com/layer1labs/specsmith/actions/runs/29966620911) | Qwen3.6-35B-A3B / DeepInfra | 1 | Adaptive managed-route diagnostic |
| [29962883256](https://github.com/layer1labs/specsmith/actions/runs/29962883256) | Qwen3.6-35B-A3B, Qwen3-Coder-Next, Qwen3-Coder-480B-A35B | 1 | Managed-route diagnostic only |
| `29839696631`, `29942515095` | GPT-5.6 Sol | 5 | Superseded historical screens |
| `29944111036` | Qwen3.6-35B-A3B / Scaleway | 1 | Superseded route diagnostic |

Results are never combined across incompatible commits, task grids, routes, or
repetition sets. GPT-5.6 uses Chat Completions with `reasoning_effort=none` for
function-tool compatibility in every condition.

## Frontier control and earlier broad diagnostic

The promotion funnel first admitted Terra at n=1, then at n=5, before the
completed n=10 release result above. Luna was also correct at admission but
used 43,112 tokens and eleven turns, so it did not advance.

The earlier long-horizon frontier control was GPT-5.6 Sol plus FULL at 17.5k
TPCA (10/10). In the same broad n=10 run, the versioned Cursor-style condition
also passed 10/10 at 54.1k TPCA.

| Condition | Correct | Tokens/correct | Cost | Mean turns |
|---|---:|---:|---:|---:|
| Cursor-style rules, all tasks | 70/80 | 23.9k | $9.4978 | 5.16 |
| Specsmith FULL, all tasks | 74/80 | 10.1k | $7.4014 | 3.35 |
| Cursor-style rules, coding only | 60/60 | 25.9k | $8.9857 | 6.02 |
| Specsmith FULL, coding only | 54/60 | 13.9k | $7.4014 | 4.47 |

The all-task aggregate favors FULL, but the coding-only pass-rate regression
blocks a superiority claim. T10 passed 9/10 and T13 5/10 under FULL versus
10/10 for Cursor-style rules in both tasks. T28, T1, T2, and T11 still favor
FULL materially. The result compares with this repository's versioned
Cursor-style rules condition; it is not a claim about every interactive
feature or future version of the commercial Cursor product.

The data-driven T10/T13 repair then passed all 40 targeted n=10 cells. FULL used
12.3k TPCA versus Cursor-style rules at 30.2k, with 29.9% lower cost/pass and
zero high/critical audit findings. This clears the measured correctness
blocker for the repaired commit without pooling incompatible runs.

## Managed Qwen findings

The locked July 26 admission produced Qwen3.6's best correct managed T28 result
so far: 67,701 tokens, twelve turns, $0.0249 measured route cost, and one stable
tool-schema hash. That is a 47.9% reduction from the prior 129,905-token correct
diagnostic, but still 3.87× the release-quality Sol FULL anchor. The deterministic
audit selected `advance_candidate`, so this route is not repeated and cannot be
used in a lower-tier-governed versus frontier-raw claim.

The July 25 selective replay promoted hidden failures into public API, schema,
Go-tag, and accessible-UI validators, then reran only the affected candidates:

| Route | Result | Tokens | Turns | Decision |
|---|---:|---:|---:|---|
| `Qwen/Qwen3.6-35B-A3B:deepinfra` | pass | 129,905 | 19 | correct but 7.4× current Sol TPCA; reject repetition |
| `Qwen/Qwen3-Coder-480B-A35B-Instruct:novita` | fail | 55,953 | 12 | serialized repair loop and text stop; reject |
| `zai-org/GLM-5.2:deepinfra` | fail | 29,864 | 5 | completed API/Go, then repeated UI narration after bounded recovery; reject |

These are diagnostic n=1 cells. Workflow success means the harness completed;
only the first row passed the acceptance oracle.

| Route | Cursor correct | FULL correct | FULL TPCA | Serving observation |
|---|---:|---:|---:|---|
| `Qwen/Qwen3.6-35B-A3B:deepinfra` | 2/3 | 1/3 | 186.8k | best managed candidate; T2 benefited strongly, T11/T28 remained serial and slow |
| `Qwen/Qwen3-Coder-Next:novita` | 2/3 | 0/3 | undefined | lower FULL history on T28, but no correct FULL cell |
| `Qwen/Qwen3-Coder-480B-A35B-Instruct:novita` | 0/3 | 0/3 | undefined | larger active capacity did not repair tool-loop behavior |

These n=1 rows diagnose serving/model interaction; they do not rank the models.
Qwen3.6/DeepInfra took 35m23s for six cells, versus about six minutes for each
Novita model job. A low list price is therefore not a low task cost when action
turns and latency multiply.

The strongest positive Qwen receipt was T2: Qwen3.6 FULL passed in 19.3k tokens
and four turns, while Cursor passed in 65.6k tokens and ten turns. T11 exposed
the opposite boundary: Cursor passed, while FULL exhausted 12 turns after
serial reads and an unrelated-defect detour. All T28 cells failed.

The adaptive Qwen3.6 rerun changed that diagnostic from Cursor 2/3 and FULL
1/3 to Cursor 1/3 and FULL 2/3; stochastic n=1 results must not be combined as
replicates. Within the new run, FULL used 201,485 tokens (100.7k TPCA) versus
Cursor's 358,653 tokens (358.7k TPCA). FULL T11 passed in six turns after one
composite two-file write. T28 remained incorrect at the 20-turn boundary despite
all public checks passing, exposing a contract-validator and repair-direction
gap rather than evidence that more turns or a larger model would solve it.

The contract-repair T28 run then failed both conditions. Cursor used 183.1k
tokens and passed 4/5 hidden checks. FULL used 203.2k tokens over 891.3 seconds,
implemented every declared file, and passed the hidden oracle 5/5, but one Ruff
`I001` remained after the last write. Turns 15–20 were unchanged rereads. The
visible contract and milestone decomposition therefore improved substantive
coverage but did not make this serving route efficient or reliable.

## July 23 admission decision

| Workflow | Correct | Tokens | Public evidence | Independent evidence |
|---|---:|---:|---|---|
| [30010219286](https://github.com/layer1labs/specsmith/actions/runs/30010219286) | yes | 180,895 | passed | hidden oracle 5/5 |
| [30011743699](https://github.com/layer1labs/specsmith/actions/runs/30011743699) | no | 136,360 | passed | hidden oracle failed |
| [30013020354](https://github.com/layer1labs/specsmith/actions/runs/30013020354) | no | 151,666 | self-authored tests and Ruff failed | hidden oracle 5/5 |

The token controls materially reduced some traces but did not produce repeatable
correctness. All three used 20 turns. The one correct cell was 8.8× GPT-5.6 Sol
FULL's current 20.6k T28 TPCA, so managed Qwen3.6 is rejected for an n=5 screen.
The Qwen3-Coder-Next/Novita experiments also failed admission: `30007255204`
returned HTTP 400 before the first action, while `30007554143` wrote no files in
58,149 tokens. Neither demonstrates the native parser.

## Native Qwen experiment

No same-route repetition was earned. The repository now defines the cleaner
one-cell experiment in `.github/workflows/qwen-native-bench.yml`:

- `Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8`;
- vLLM `v0.24.0` with automatic tool choice and `qwen3_xml`;
- one L40S GPU, 32k context, exact native tool probe, and zero provider retries;
- 20-minute deployment, 120-second request, and 15-minute cell bounds;
- pause and delete attempted even when deployment or inference fails.

Workflow `30317300977` reached HF identity resolution but endpoint creation
returned 403 because `HF_TOKEN` lacked `inference.endpoints.write`. No endpoint
or model request was created. After that secret permission is corrected, rerun
the existing workflow once; do not alter the model, parser, hardware, task,
controller, or timeout bounds. A correct cell must also beat the current
17,501.7-token Sol envelope before an n=5 screen is justified.

If the literal-parser cell still fails, the next distinct lane is a Qwen-native
agent scaffold such as Qwen Code or Qwen-Agent, with scaffold and endpoint
metadata retained. A larger Coder-480B capacity control is lower priority
because the Novita result already showed that parameter count alone did not
repair tool-loop behavior.

## FP8 and base variants

The Qwen3.6 FP8 repository was not mapped to a managed Hugging Face Inference
Provider during the probe. Test it only in a separately labelled self-hosted
lane with exact hardware, quantization, runtime, parser, and sampling metadata.
A base model is not the preferred tool agent without post-training or an agent
scaffold; compare it as a scientific control, not as the expected winner.

## Recommended comparison set

- GPT-5.6 Sol: frontier efficacy and current repeated anchor.
- A current smaller OpenAI model: degradation and price sensitivity, never as a
  proxy for frontier behavior.
- Qwen3.6/DeepInfra: managed open-weight portability after adaptive tools.
- Qwen3-Coder-30B/native `qwen3_xml`: pinned one-cell endpoint admission.

## July 24 open-frontier replay

All seven exact routes passed metadata and paid tool-call probes in
[workflow 30091129732](https://github.com/layer1labs/specsmith/actions/runs/30091129732).
The matched n=1 results in workflow `30091184259` are diagnostic:

| Candidate | Cursor result | FULL result | Audit decision |
|---|---:|---:|---|
| Kimi K2.7 Code / DeepInfra | fail, 42,319 | pass, 24,021 | confirm route before repetition |
| Qwen3.6-35B-A3B / DeepInfra | fail, 163,904 | pass, 62,060 | advance candidate; above envelope |
| DeepSeek-V4 Pro / Novita | fail, 21,095 | fail, 74,923 | repair explicit completion narration |
| GLM-5.2 / DeepInfra | fail, 196,733 | fail, 24,619 | repair explicit milestone narration |
| MiniMax-M3 / Novita | fail, 26,275 | fail, 56,054 | repair provider/tool continuation |
| DeepSeek-V4 Flash / DeepInfra | fail, 87,207 | fail, 130,057 | rejected at turn ceiling |
| Nemotron 3 Ultra / DeepInfra | fail, 141,608 | fail, 119,407 | rejected repeated-tool loop |

Specsmith materially improved the Qwen3.6 outcome, but 62.1k TPCA was still
2.19× the old Sol envelope and therefore did not earn n=5. The final targeted
repair run made GLM and DeepSeek Pro correct, but their 73.6k and 84.4k TPCA
also failed the efficiency envelope. MiniMax's post-repair trace wrote no files
and ended after two empty continuations; further repetition requires a new
native tool protocol or serving route.

DeepSeek V4 Flash and Nemotron completed the previous next-candidate queue and
are rejected on their measured routes. The remaining infrastructure experiment
is Qwen3-Coder-Next with the native `qwen3_coder` parser. The local 12 GB RTX
4070 cannot host the 80B checkpoint, and this repository has no configured
OpenAI-compatible endpoint secret/URL for an external native deployment, so a
managed Novita rerun would not test the requested parser.

Kimi route confirmation also completed. DeepInfra returned router HTML 504
responses in eight requested n=5 cells, Together failed its live probe with
HTTP 403, and Novita completed a matched n=1 screen. On Novita, Cursor Rules
failed after 108,137 tokens and 20 turns; FULL passed after 43,015 tokens and
10 turns. That is a substantial within-route governance improvement, but the
correct FULL cell costs 1.62× the 26,499-token n=5 point estimate and 1.42× the
release-sized 30,317-token Sol envelope. The audit therefore blocks n=5 rather
than treating provider fallback as a reason to waive the efficiency gate.

## Current 20B–32B open-model result

The July 27 admission used exact managed routes and a single T28/FULL
diagnostic before any repeated spend:

| Model / route | Initial admission | Trace-backed follow-up | Decision |
|---|---|---|---|
| Qwen3.6-27B / DeepInfra | fail, 11,208 tokens, 3 turns | pass, 72,255 tokens, 14 turns | capability admitted; 4.13× Sol TPCA, so no repetition |
| GPT-OSS-20B / Nscale | fail, 85,438 tokens, 12 turns | none | route ignored supplied evidence and ended empty |
| Qwen3-Coder-30B-A3B / Scaleway | fail, 122,892 tokens, 20 turns | none | serialized tool calls and turn exhaustion |
| GLM-4.7-Flash / DeepInfra | fail, 54,309 tokens, 8 turns | none | malformed repair sequence and empty stop |
| Qwen3-32B / DeepInfra | — | fail, 63,636 tokens, 6 turns | repeated narration and incomplete scope |

The successful Qwen3.6 result is
[workflow 30265818081](https://github.com/layer1labs/specsmith/actions/runs/30265818081);
the Qwen3-32B follow-up is
[workflow 30265830535](https://github.com/layer1labs/specsmith/actions/runs/30265830535).
Both are pinned to commit `4bb1bf1`. The original four-model cohort is
[workflow 30264387650](https://github.com/layer1labs/specsmith/actions/runs/30264387650).

Qwen3.6-27B proves that the 20B–32B search band should not be dismissed as
incapable. It does not prove substitution: the cell is n=1 and uses 4.13× the
release-quality governed Sol token envelope. The strongest next experiment is
not another managed-route repetition. It is the same one-cell gate behind a
native Qwen tool parser or a patch-oriented editing surface, followed by n=5
only if correctness remains intact and TPCA enters the frontier envelope.

The final managed-route confirmation changed only observed controller
boundaries. Finish-reason telemetry and scalar fallback still failed at
33,884 tokens in
[workflow 30268327224](https://github.com/layer1labs/specsmith/actions/runs/30268327224).
Exact bounded recovery for the model's implementation promise then passed in
[workflow 30269000016](https://github.com/layer1labs/specsmith/actions/runs/30269000016)
at 77,776 tokens and 14 turns. This second correct cell is 7.6% above the
prior pass and 4.44× the Sol envelope. The next candidate must therefore
change the native parser or editing interface; repeating the same managed
route is stopped.

Subsequent controller-protocol isolation changed that managed-route
recommendation. Plain scalar parallel calls with automatic tool choice passed
T28 in
[workflow 30274872374](https://github.com/layer1labs/specsmith/actions/runs/30274872374)
at 26,850 tokens and six turns. That is a 62.8% reduction from 72,255 tokens,
but still 1.53× the governed Sol envelope. Required-tool mode used 42,697
tokens, write-only mode used 37,058, and validator-authority mode used 43,622;
context compaction failed. These remain separate n=1 diagnostics: scalar
parallelism is the preferred Qwen controller, but it does not pass the
small-model substitution screen.

Later route and native-interface isolation did not displace that winner.
Qwen3-Coder-Next and Qwen3-Coder-480B on Novita failed at 78,742 and 57,251
tokens respectively in
[workflow 30286692090](https://github.com/layer1labs/specsmith/actions/runs/30286692090).
An exact single-file edit surface stayed near the winner's token level but
failed after coupled import/annotation repairs were split across turns. A
fixed-scalar milestone bundle then made Qwen3.6-27B fully correct in
[workflow 30289266484](https://github.com/layer1labs/specsmith/actions/runs/30289266484),
but used 71,090 tokens and 13 turns; Qwen3-Coder-480B failed the same control at
122,567 tokens.

The resulting atomic multi-hunk patch surface is locally verified, but its live
[run 30290375485](https://github.com/layer1labs/specsmith/actions/runs/30290375485)
received an HTML 504 and its
[single retry 30291702747](https://github.com/layer1labs/specsmith/actions/runs/30291702747)
failed the availability probe. Those attempts are provider-censored, not model
failures. The best measured managed Qwen result therefore remains the 26,850
token scalar-parallel cell, still 1.53× the Sol envelope.

A subsequent hosted Qwen3-Coder-30B route passed exact structured-tool probes
and isolated three atomic-patch policies:

| Workflow | Policy | Correct | Tokens | Decision |
|---|---|---:|---:|---|
| [30317439173](https://github.com/layer1labs/specsmith/actions/runs/30317439173) | atomic patch | no | 123,384 | reject baseline failure |
| [30317963475](https://github.com/layer1labs/specsmith/actions/runs/30317963475) | scoped atomic patch | no | 34,892 | retain failure-spend controls; repair correctness |
| [30318295306](https://github.com/layer1labs/specsmith/actions/runs/30318295306) | scoped + required tools | no | 81,648 | reject forced tool choice |

The scoped variant lowered failure spend materially but did not pass the
oracle. The required variant repeated one three-action batch and motivated a
deterministic batch-loop guard. The provider does not disclose whether its
backend used `qwen3_xml`, so these are hosted structured-tool results.

The literal vLLM `qwen3_xml` lane was initially censored in
[workflow 30317300977](https://github.com/layer1labs/specsmith/actions/runs/30317300977).
With corrected endpoint permission,
[workflow 30358919239](https://github.com/layer1labs/specsmith/actions/runs/30358919239)
proved the parser but failed atomic and scoped T28 cells at 34,146 and 53,451
tokens. A native required-tool follow-up in
[workflow 30359943752](https://github.com/layer1labs/specsmith/actions/runs/30359943752)
also failed at 181,884 tokens and 20 turns. Native serving removes parser
uncertainty; it does not rescue this 30B checkpoint under the tested policies.
The clean next comparison is a stronger tool-serving model or controller-owned
milestone decomposition, not more repetitions of these failed cells.

Milestone-packet follow-ups tested that decomposition directly:

| Workflow | Controller | Correct | Tokens | Turns | Milestones |
|---|---|---:|---:|---:|---:|
| [30367659754](https://github.com/layer1labs/specsmith/actions/runs/30367659754) | packet | no | 108,021 | 20 | 1/4 |
| [30367659754](https://github.com/layer1labs/specsmith/actions/runs/30367659754) | packet + adaptive recovery | no | 112,933 | 17 | 1/4 |
| [30369089983](https://github.com/layer1labs/specsmith/actions/runs/30369089983) | validator authority + atomic repair | no | 18,646 | 5 | 1/4 |
| [30370203101](https://github.com/layer1labs/specsmith/actions/runs/30370203101) | authority v2 + repeated forcing | no | 98,679 | 20 | 1/4 |

Independent-validator authority and repair-only patches materially bounded
failure cost, but did not improve milestone completion. Repeated required turns
regressed by 5.29× relative to the fail-fast authority cell. The native
Qwen3-Coder-30B checkpoint is therefore rejected for T28 promotion under every
tested controller; the next credible comparison needs a stronger tool-serving
model or route.

## Historical open-frontier admissions

Four current checkpoints were admitted through live route probes and one T28
FULL diagnostic each:

| Candidate | Pinned route | Router price / 1M input-output | Why it is useful |
|---|---|---:|---|
| [Kimi K2.7 Code](https://huggingface.co/moonshotai/Kimi-K2.7-Code) | DeepInfra | $0.74 / $3.50 | code-specialized 262K agent with explicit tool-oriented evaluation settings |
| [GLM-5.2](https://huggingface.co/zai-org/GLM-5.2) | DeepInfra | $0.93 / $3.00 | one-million-token long-horizon coding control |
| [DeepSeek-V4 Pro](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro) | Novita | $1.60 / $3.20 | 49B-active million-token reasoning/coding control |
| [MiniMax-M3](https://huggingface.co/MiniMaxAI/MiniMax-M3) | Novita | $0.30 / $1.20 | inexpensive one-million-token long-horizon challenger |

All four initial routes passed live tool-call probes in
[workflow 30045915766](https://github.com/layer1labs/specsmith/actions/runs/30045915766).

| Candidate | Correct | Tokens | Turns | Cost | Wall time | Decision |
|---|---:|---:|---:|---:|---:|---|
| DeepSeek-V4 Pro | yes | 47,855 | 7 | $0.1013 | 286.9s | strongest open challenger; above Sol envelope |
| GLM-5.2 | yes | 72,187 | 11 | $0.1015 | 376.6s | above Sol envelope |
| Kimi K2.7 Code | yes | 101,713 | 15 | $0.1326 | 552.8s | above Sol envelope |
| MiniMax-M3 | no | 53,196 | 8 | $0.0301 | 235.6s | text-only stop |
| MiniMax-M3 retry | no | 24,093 | 4 | $0.0151 | 128.1s | empty-response stop |

The three correct diagnostics passed the independent oracle, but even DeepSeek
used 69% more tokens than the then-current 28,314-token Sol+FULL envelope. The MiniMax
failures led to bounded narration recovery and fail-closed `governed_failure`
admission logic; they are not low-cost successes.

GPT-OSS-120B provided a useful provider control. DeepInfra called one file tool,
then emitted two empty continuations in
[run 30077072490](https://github.com/layer1labs/specsmith/actions/runs/30077072490).
The audit now labels this `tool_continuation_failure`. Novita resumed correctly
in [run 30077459159](https://github.com/layer1labs/specsmith/actions/runs/30077459159),
but emitted one action per turn, exhausted all 20 turns at 55,023 tokens, and
failed correctness. That trace exposed an adaptive-controller defect:
pre-enabled composite writes suppressed the later composite-read upgrade.
Composite read and write state are now independent, so a serialized route gains
bounded `read_files` after two scalar turns without enlarging Sol's initial tool
surface. The resulting
[run 30077929145](https://github.com/layer1labs/specsmith/actions/runs/30077929145)
fell to 44,692 tokens and 17 turns—18.8% fewer tokens and three fewer turns—but
the provider serialized exact `done` arguments as plain JSON after all declared
files were written. Exact-schema recovery is now permitted only after complete
write-scope evidence; deterministic public and independent checks still decide
correctness. The confirmation
[run 30078601832](https://github.com/layer1labs/specsmith/actions/runs/30078601832)
did not reach complete write scope, so recovery correctly did not activate; it
exhausted 20 turns at 49,339 tokens. The managed GPT-OSS model/route pair is
rejected.

## Next infrastructure queue

The next managed admissions should remain bounded:

1. **GPT-5.6 Luna strict-schema repair admission** — the initial native route
   failed because fourteen `write_milestone` calls carried non-string content.
   Rerun one T28/FULL cell after making every fixed scalar slot required and
   unused slots nullable, which enables provider strict validation. Preserve
   the same controller, effort, verbosity, timeouts, validators, and oracle.
   Luna receives no repetition budget unless correctness passes and efficiency
   improves materially on Terra.
2. **GPT-5.6 Terra native release confirmation** — expand the identical T28
   cell from five to ten repetitions before making a release-quality native
   route claim. Do not pool the earlier n=1 admission.
3. **Qwen3-Coder-Next with its native `qwen3_coder` parser** — provision a
   multi-GPU or hosted endpoint with bounded request timeouts and begin with one
   T28 FULL atomic-patch cell; do not substitute the measured Novita route.
Kimi, GPT-OSS, GLM, DeepSeek, MiniMax, Flash, and Nemotron receive no further
managed-route repetitions on the measured configurations. A new attempt must
change a demonstrated serving or controller boundary and starts again at n=1.
Every candidate must beat the current Sol FULL T28 token envelope before
earning a matched n=5 screen.

The Sol n=10 release-quality confirmation is complete in workflow `30099279843`.
Promote a route from n=1 to n=5 only after it produces correct cells and use
n=10 before a release-quality statistical claim. Repeat an older candidate only
when a controller, validator, prompt contract, parser, or serving route changed;
otherwise the deterministic envelope should stop the paid run. Preserve raw
token, cost, latency, sampling, parser, and provider receipts so a serving
change is not mistaken for a model-quality change.

## Failure provenance

Unavailable routing, incompatible function-tool settings, cancelled jobs,
provider errors, and incomplete artifacts remain in provenance but never enter
a leaderboard denominator. This is especially important for open-weight models:
the model checkpoint, chat template, tool parser, quantization, and host can each
change the result.
