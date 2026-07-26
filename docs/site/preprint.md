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
