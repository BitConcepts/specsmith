# Preprint, Evidence, and Public Claims

## Governance as capability substitution

The accompanying preprint studies whether deterministic requirements,
bounded context, executable verification, and fail-closed stopping can let a
lower-tier model complete repository tasks with the correctness of a frontier
model while using fewer tokens per correct answer.

- [Preprint source](https://github.com/layer1labs/specsmith/tree/develop/paper)
- [Reproducibility data](https://github.com/layer1labs/specsmith/tree/develop/paper/data)
- [Benchmark implementation](https://github.com/layer1labs/specsmith/tree/develop/scripts/govern_bench)
- [Statistical methodology](https://github.com/layer1labs/specsmith/blob/develop/scripts/govern_bench/METHODOLOGY.md)

The paper reports systems, not model weights. “Lower-tier” means the exact
published API route selected as the candidate in a matched experiment. It
does not imply a parameter count or architecture that the provider has not
published. “Small model” is reserved for a route with a published size, such
as Llama 3.1 8B.

## Claim ladder

Public wording follows the strongest completed evidence gate, not the most
favorable point estimate.

| Claim | Evidence required | Current status |
|---|---|---|
| Specsmith improves one model on the exact benchmark | Same-commit matched conditions, complete cells, executable correctness | Supported for GPT-5.6 Sol FULL versus the versioned Cursor-style condition on the eight-task n=10 grid |
| A lower-tier governed system substitutes for frontier raw on the mixed release suite | Preregistered eight-task 2×2 design, n=10, fixed-suite correctness and TPCA gates | Supported for Terra FULL versus Sol raw in workflow 30210886840 |
| The result is robust to resampling the eight named tasks | Task-cluster correctness and TPCA confidence gates both pass | Supported within the benchmark distribution; this is not evidence on fresh repositories |
| A lower-tier governed system substitutes on coding-only work | Prespecified coding slice clears the same correctness and TPCA gates | Not confirmed: observed results favor Terra FULL, but the correctness lower bound missed the margin by 0.7 pp |
| The result generalizes to new repositories and task families | Independent replication across fresh real repositories, languages, providers, and task distributions | Not established |
| Published 8B or mini models replace frontier models | A small-model admission, matched n=5 screen, and n=10 release gate all pass | Rejected for current routes: Llama 3.1 8B and GPT-4o mini T28 admissions failed |
| A reasoning-capable 20B–32B model can complete governed T28 | Correct public checks and independent oracle in admission | Supported at n=1 for Qwen3.6-27B/DeepInfra; the best controller diagnostic used 26,850 tokens and 6 turns |
| A 20B–32B governed model replaces frontier Sol efficiently | Correct admission inside the versioned Sol envelope, then matched n=5 and n=10 gates | Not supported: the best correct 27B cell still used 1.53× the Sol token envelope and has no matched n=5 confirmation |
| Native Responses tools improve the governed T28 model/cost frontier | Same-controller route admission followed by matched n=5 and n=10 confirmation | Screening only: Terra passed 5/5 at 17,213 TPCA and $0.1176 per pass; Luna failed admission; no n=10 native claim |
| Small models universally replace frontier models | Broad external replication across fresh repositories, languages, providers, and task distributions | Not claimed |

The decisive
[workflow 30210886840](https://github.com/layer1labs/specsmith/actions/runs/30210886840)
ran all four matched cells for eight tasks and ten repetitions at preregistered
commit `75a8c791`. Terra+FULL passed 80/80 at 11,737 tokens per correct answer
and $0.0602 per pass; Sol raw passed 65/80 at 28,023 TPCA and $0.1511 per pass.
The TPCA ratio was 0.419 (fixed-suite 95% interval 0.358–0.485; task-cluster
interval 0.212–0.708). Correctness-difference intervals were +3.3 to +34.1 pp
and −4.4 to +54.7 pp. Both mixed-suite gates passed.

The prespecified six-task coding sensitivity prevents the two deterministic
clarification/safety gates from carrying a coding claim. Terra+FULL passed
60/60 coding cells at 15,649 TPCA; Sol raw passed 55/60 at 30,250 TPCA. The
fixed-suite TPCA interval remained favorable at 0.437–0.608, but the
correctness-difference lower bound was −5.7 pp, just outside the −5 pp margin.
Coding-only substitution is therefore not confirmed.

## Approved wording

These forms remain valid only with the named workflow, models, conditions,
task suite, sample size, and confidence result:

> In the preregistered eight-task GovernanceBench mixed suite (workflow
> 30210886840), GPT-5.6 Terra with Specsmith FULL cleared the correctness
> non-inferiority and token-superiority gates against raw GPT-5.6 Sol.

> Terra FULL passed 80/80 cells at 11,737 tokens per correct answer versus
> Sol raw at 65/80 and 28,023. The prespecified coding-only correctness gate
> did not pass, so the result supports task-conditional routing rather than
> general model equivalence.

Do not shorten this to “small models replace frontier models” unless a
published-size model passes the complete promotion funnel. Do not describe
the versioned Cursor-style benchmark condition as every Cursor feature or
release.

The final Llama 3.1 8B admission in
[workflow 30211920507](https://github.com/layer1labs/specsmith/actions/runs/30211920507)
recovered the route's exact text-serialized function calls through the normal
tool guards, but still failed T28 at 98,543 tokens. It issued 20 independent
actions in 20 turns, triggered the repeated-boundary guard, and exhausted the
cap. The earlier GPT-4o mini admission also failed at 107,896 tokens. Both
routes are rejected before repetition; adding spend cannot repair a failed
admission.

A later reasoning-capable cohort tested GPT-OSS-20B, Qwen3.6-27B,
Qwen3-Coder-30B-A3B, GLM-4.7-Flash, and Qwen3-32B. After one trace-backed
controller repair, Qwen3.6-27B passed T28 in
[workflow 30265818081](https://github.com/layer1labs/specsmith/actions/runs/30265818081)
at 72,255 tokens. That is useful evidence that a published 27B model can
complete the governed task, but it is an n=1 capability result and 4.13× the
governed Sol token envelope. It strengthens the case for native-parser and
edit-interface research, not a current frontier-replacement claim.

An exact-boundary confirmation later passed in
[workflow 30269000016](https://github.com/layer1labs/specsmith/actions/runs/30269000016)
at 77,776 tokens and 14 turns. It is not pooled with the first cell because
the controller commit changed between runs. The result shows that 27B
capability can recur, but the 4.44× frontier-envelope ratio and lack of TPCA
gain preserve the negative efficiency conclusion.

A later controller-protocol isolation found a material within-route gain.
[Workflow 30274872374](https://github.com/layer1labs/specsmith/actions/runs/30274872374)
used automatic scalar-parallel file calls and passed the same T28 public and
hidden gates in six turns and 26,850 tokens. This is 62.8% below the original
correct admission, but it is a separate n=1 controller diagnostic and remains
1.53× the 17,501.7-token governed Sol envelope. Required-tool, write-only,
context-compaction, and validator-authority variants did not beat it.
Accordingly the result supports interface optimization, not frontier
replacement or a broad small-model claim.

A subsequent native-interface series provides a controlled mechanism result.
Changing only the managed Qwen route did not help: Coder-Next and Coder-480B
failed. A fixed-scalar milestone bundle made Qwen3.6-27B correct at 71,090
tokens, demonstrating that provider-visible tool structure can recover
long-horizon correctness, but not frontier efficiency. Exact-edit diagnostics
remained near 27k tokens but could not express coupled multi-hunk repairs. The
resulting atomic patch control passed local safety and routing tests; its two
live attempts were provider-censored by a 504 and a failed availability probe.
They are excluded from performance inference. The evidence therefore preserves
the 26,850-token scalar cell as the best Qwen diagnostic and does not strengthen
the substitution claim.

A newer atomic-patch series tested
`Qwen/Qwen3-Coder-30B-A3B-Instruct:scaleway` after an exact structured-tool
probe. The baseline
[workflow 30317439173](https://github.com/layer1labs/specsmith/actions/runs/30317439173)
failed T28 at 123,384 tokens, 20 turns, and four of ten declared files.
Removing model-owned rereads and narrowing the patch surface in
[workflow 30317963475](https://github.com/layer1labs/specsmith/actions/runs/30317963475)
reduced the failed attempt to 34,892 tokens, 10 turns, and 29.86 seconds:
71.7% fewer tokens, 73.9% lower estimated cost, and 78.3% lower wall time.
It still wrote only three files and failed the independent oracle, so the
result is evidence of bounded failure cost, not correctness or substitution.
Requiring a tool on every turn in
[workflow 30318295306](https://github.com/layer1labs/specsmith/actions/runs/30318295306)
regressed to 81,648 tokens and repeated the same three-action batch; that
variant is rejected.

The separately preregistered literal parser first produced censored workflow
[30317300977](https://github.com/layer1labs/specsmith/actions/runs/30317300977).
After correcting the endpoint permission,
[workflow 30358919239](https://github.com/layer1labs/specsmith/actions/runs/30358919239)
served the official FP8 checkpoint on vLLM `0.24.0`, passed the exact native
`qwen3_xml` tool probe, and then failed atomic and scoped T28 cells at 34,146
and 53,451 tokens. The scoped cell was slower and more expensive in tokens,
contrary to the hosted route result. Native required-tool workflow
[30359943752](https://github.com/layer1labs/specsmith/actions/runs/30359943752)
failed at 181,884 tokens, 20 turns, and five of ten files. It exchanged
premature prose stops for truncation and milestone fragmentation. Both
ephemeral endpoints were confirmed paused and deleted; their combined receipt
cost was approximately `$0.430977`.

These runs resolve the parser uncertainty but strengthen the negative
conclusion: native `qwen3_xml` compatibility is necessary, not sufficient, and
globally required tool choice is actively inefficient for this model/task.
None of the three rows is eligible for repetition or a frontier-substitution
claim.

Active milestone packets were then tested on the same literal-parser route.
[Workflow 30367659754](https://github.com/layer1labs/specsmith/actions/runs/30367659754)
produced packet-only and one-turn-adaptive failures at 108,021/20 turns and
112,933/17 turns; each completed one of four milestones. Independent-validator
authority plus a repair-only atomic surface in
[workflow 30369089983](https://github.com/layer1labs/specsmith/actions/runs/30369089983)
reduced the failed diagnostic to 18,646 tokens, five turns, and 36.30 seconds,
an 82.7% reduction from packet-only. It still completed only one milestone and
failed both public and hidden correctness.

A final trace-derived forced-repair revision in
[workflow 30370203101](https://github.com/layer1labs/specsmith/actions/runs/30370203101)
regressed to 98,679 tokens and 20 turns. After reaching invalid-severity
handling, the model repeated the same already-applied patch thirteen times.
This establishes a useful negative result: deterministic evidence authority and
atomic editing can sharply lower failure cost, while required tool forcing does
not supply missing semantic capability. None of these rows has defined TPCA or
supports model substitution. Compact evidence v2 records the 1/4 milestone
yield, and a final content-free no-op guard stops the second identical retry;
that guard is locally verified but was not followed by another paid run.

The native Responses route then held the controller constant and changed only
the model-serving interface. Sol passed one T28/FULL admission at 18,474 tokens
in [workflow 30412677765](https://github.com/layer1labs/specsmith/actions/runs/30412677765).
Terra passed admission and then 5/5 screening cells in
[workflow 30413249488](https://github.com/layer1labs/specsmith/actions/runs/30413249488)
at 17,213 mean tokens, $0.1176 mean cost, five turns, and no audit weakness.
This is screening evidence, not a release claim. Luna failed its separately
labeled admission in
[workflow 30414435928](https://github.com/layer1labs/specsmith/actions/runs/30414435928):
72,880 tokens, 20 turns, three of four milestones, and a failed independent
oracle. Fourteen milestone calls were rejected because used content fields were
not strings. A preregistered repair enables provider strict validation with
required nullable fixed slots; it must pass a new n=1 cell before any
repetition. These results reinforce that native tool availability alone does
not guarantee efficient tool serialization on a lower-cost model.

## Reproduction

The cited workflow retains full traces for the repository's configured
artifact-retention period. The repository permanently archives compact cell
measurements and SHA-256 manifests that intentionally exclude prompts, source
diffs, validator logs, governance decisions, and assistant transcripts.

```bash
python scripts/govern_bench/export_evidence.py \
  --input bench-results-terra.json bench-results-sol.json \
  --output-dir paper/data/substitution-release \
  --workflow-id 30210886840 \
  --commit-sha 75a8c7911187abe8db2b6ca77f0e08fa7859ffe7

python scripts/govern_bench/compare_runs.py \
  bench-results-terra.json bench-results-sol.json \
  --summary-output paper/data/substitution-release/summary.json

python scripts/govern_bench/compare_runs.py \
  bench-results-terra.json bench-results-sol.json \
  --tasks T1 T2 T10 T11 T13 T28 \
  --summary-output paper/data/substitution-release/coding-summary.json

python scripts/govern_bench/render_preprint_results.py \
  --summary paper/data/substitution-release/summary.json \
  --coding-summary paper/data/substitution-release/coding-summary.json \
  --output paper/generated/results.tex \
  --workflow-id 30210886840 \
  --commit-sha 75a8c7911187abe8db2b6ca77f0e08fa7859ffe7
```

The renderer rejects a partial task grid, fewer than ten repetitions, or an
unsupported comparison schema. Missing, skipped, errored, duplicate, or dry-run
cells are also excluded from evidence export.

Verify any archived compact bundle:

```bash
python scripts/govern_bench/export_evidence.py \
  --verify-manifest paper/data/substitution-release/manifest.json
```

Pass `--source-dir PATH_TO_DOWNLOADED_RAW_ARTIFACTS` to verify the raw artifact
digests as well. Nested `gh run download` directories are discovered
recursively; missing or duplicate source names fail closed.
