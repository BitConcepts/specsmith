# specsmith Governance Efficiency — Model Comparison

**Models compared:** gpt-5.6-sol (frontier) · gpt-5.6-terra (mid)

> **Primary:** tokens per correct answer (TPCA) = mean_tokens ÷ pass_rate.
> **Secondary:** cost-of-pass (CoP) = estimated mean_cost_per_run ÷ pass_rate.
> Lower is better. ∞ = condition never passed.

## T1 — Add paginated endpoint (feature add)

| Condition| gpt-5.6-sol Pass%|Tokens|TPCA|Cost/run|CoP| gpt-5.6-terra Pass%|Tokens|TPCA|Cost/run|CoP|
|----------|------:|------:|------:|--------:|--------:|------:|------:|------:|--------:|--------:|
| Raw agent (ungoverned)| 100%| 15.6k| 15.6k| $0.1005| $0.10046| 80%| 21.8k| 27.2k| $0.0865| $0.10816|
| CLAUDE.md / AGENTS.md| —| —| —| —| —| —| —| —| —| —|
| Cursor .cursor/rules| —| —| —| —| —| —| —| —| —| —|
| GitHub Copilot instructions| —| —| —| —| —| —| —| —| —| —|
| OpenAI Codex CLI AGENTS.md| —| —| —| —| —| —| —| —| —| —|
| Cline .clinerules| —| —| —| —| —| —| —| —| —| —|
| Aider CONVENTIONS.md| —| —| —| —| —| —| —| —| —| —|
| BMAD Blueprint→Milestone| —| —| —| —| —| —| —| —| —| —|
| OpenSpec REQUIREMENTS.md| —| —| —| —| —| —| —| —| —| —|
| Agile BDD / TDD| —| —| —| —| —| —| —| —| —| —|
| specsmith LIGHT (preflight)| —| —| —| —| —| —| —| —| —| —|
| specsmith FULL (governed)| **100%**| 7.9k| 7.9k| $0.0780| **$0.07799**| **100%**| 19.5k| 19.5k| $0.0934| **$0.09337**|

## T10 — Add filtering / query params (feature add)

| Condition| gpt-5.6-sol Pass%|Tokens|TPCA|Cost/run|CoP| gpt-5.6-terra Pass%|Tokens|TPCA|Cost/run|CoP|
|----------|------:|------:|------:|--------:|--------:|------:|------:|------:|--------:|--------:|
| Raw agent (ungoverned)| 100%| 19.6k| 19.6k| $0.1636| $0.16361| 60%| 33.2k| 55.3k| $0.1236| $0.20594|
| CLAUDE.md / AGENTS.md| —| —| —| —| —| —| —| —| —| —|
| Cursor .cursor/rules| —| —| —| —| —| —| —| —| —| —|
| GitHub Copilot instructions| —| —| —| —| —| —| —| —| —| —|
| OpenAI Codex CLI AGENTS.md| —| —| —| —| —| —| —| —| —| —|
| Cline .clinerules| —| —| —| —| —| —| —| —| —| —|
| Aider CONVENTIONS.md| —| —| —| —| —| —| —| —| —| —|
| BMAD Blueprint→Milestone| —| —| —| —| —| —| —| —| —| —|
| OpenSpec REQUIREMENTS.md| —| —| —| —| —| —| —| —| —| —|
| Agile BDD / TDD| —| —| —| —| —| —| —| —| —| —|
| specsmith LIGHT (preflight)| —| —| —| —| —| —| —| —| —| —|
| specsmith FULL (governed)| **100%**| 15.6k| 15.6k| $0.1194| **$0.11940**| **100%**| 28.2k| 28.2k| $0.1215| **$0.12146**|

## T13 — CLI tool feature (stdlib only)

| Condition| gpt-5.6-sol Pass%|Tokens|TPCA|Cost/run|CoP| gpt-5.6-terra Pass%|Tokens|TPCA|Cost/run|CoP|
|----------|------:|------:|------:|--------:|--------:|------:|------:|------:|--------:|--------:|
| Raw agent (ungoverned)| 100%| 35.2k| 35.2k| $0.1220| $0.12196| 80%| 37.1k| 46.3k| $0.1194| $0.14922|
| CLAUDE.md / AGENTS.md| —| —| —| —| —| —| —| —| —| —|
| Cursor .cursor/rules| —| —| —| —| —| —| —| —| —| —|
| GitHub Copilot instructions| —| —| —| —| —| —| —| —| —| —|
| OpenAI Codex CLI AGENTS.md| —| —| —| —| —| —| —| —| —| —|
| Cline .clinerules| —| —| —| —| —| —| —| —| —| —|
| Aider CONVENTIONS.md| —| —| —| —| —| —| —| —| —| —|
| BMAD Blueprint→Milestone| —| —| —| —| —| —| —| —| —| —|
| OpenSpec REQUIREMENTS.md| —| —| —| —| —| —| —| —| —| —|
| Agile BDD / TDD| —| —| —| —| —| —| —| —| —| —|
| specsmith LIGHT (preflight)| —| —| —| —| —| —| —| —| —| —|
| specsmith FULL (governed)| **100%**| 12.5k| 12.5k| $0.0707| **$0.07073**| **100%**| 9.4k| 9.4k| $0.0438| **$0.04384**|

## T28

| Condition| gpt-5.6-sol Pass%|Tokens|TPCA|Cost/run|CoP| gpt-5.6-terra Pass%|Tokens|TPCA|Cost/run|CoP|
|----------|------:|------:|------:|--------:|--------:|------:|------:|------:|--------:|--------:|
| Raw agent (ungoverned)| 100%| 46.3k| 46.3k| $0.2856| $0.28558| 100%| 115.2k| 115.2k| $0.3768| $0.37680|
| CLAUDE.md / AGENTS.md| —| —| —| —| —| —| —| —| —| —|
| Cursor .cursor/rules| —| —| —| —| —| —| —| —| —| —|
| GitHub Copilot instructions| —| —| —| —| —| —| —| —| —| —|
| OpenAI Codex CLI AGENTS.md| —| —| —| —| —| —| —| —| —| —|
| Cline .clinerules| —| —| —| —| —| —| —| —| —| —|
| Aider CONVENTIONS.md| —| —| —| —| —| —| —| —| —| —|
| BMAD Blueprint→Milestone| —| —| —| —| —| —| —| —| —| —|
| OpenSpec REQUIREMENTS.md| —| —| —| —| —| —| —| —| —| —|
| Agile BDD / TDD| —| —| —| —| —| —| —| —| —| —|
| specsmith LIGHT (preflight)| —| —| —| —| —| —| —| —| —| —|
| specsmith FULL (governed)| **100%**| 18.1k| 18.1k| $0.2087| **$0.20874**| **100%**| 19.1k| 19.1k| $0.1220| **$0.12203**|

## Cross-task summary

Mean across all tasks shown above.

| Condition| gpt-5.6-sol Pass%|Mean TPCA|Mean CoP|$/mo @20/day| gpt-5.6-terra Pass%|Mean TPCA|Mean CoP|$/mo @20/day|
|----------|------:|--------:|--------:|-----------:|------:|--------:|--------:|-----------:|
| Raw agent (ungoverned)| 100%| 29.2k| $0.16790| $73.88| 80%| 64.8k| $0.22071| $77.69|
| CLAUDE.md / AGENTS.md| —| —| —| —| —| —| —| —|
| Cursor .cursor/rules| —| —| —| —| —| —| —| —|
| GitHub Copilot instructions| —| —| —| —| —| —| —| —|
| OpenAI Codex CLI AGENTS.md| —| —| —| —| —| —| —| —|
| Cline .clinerules| —| —| —| —| —| —| —| —|
| Aider CONVENTIONS.md| —| —| —| —| —| —| —| —|
| BMAD Blueprint→Milestone| —| —| —| —| —| —| —| —|
| OpenSpec REQUIREMENTS.md| —| —| —| —| —| —| —| —|
| Agile BDD / TDD| —| —| —| —| —| —| —| —|
| specsmith LIGHT (preflight)| —| —| —| —| —| —| —| —|
| specsmith FULL (governed)| **100%**| **13.5k**| **$0.11921**| **$52.45**| **100%**| **19.1k**| **$0.09517**| **$41.88**|

## Governance as model-capability substitution

This is a 2×2 factorial comparison: both models run both UNGOVERNED and SPECSMITH_FULL on the identical task and repetition grid. The headline pair asks whether the lower-tier governed route can match the frontier ungoverned route; the other two cells preserve the within-model governance controls.

| Smaller governed model | Pass | TPCA | CoP | Stronger ungoverned model | Pass | TPCA | CoP | Outcome |
|---|---:|---:|---:|---|---:|---:|---:|---|
| gpt-5.6-terra + FULL | 100% | 19.1k | $0.09517 | gpt-5.6-sol + UNGOVERNED | 100% | 29.2k | $0.16790 | Matches/exceeds correctness with lower TPCA |

**Paired inference — gpt-5.6-terra + FULL vs gpt-5.6-sol + UNGOVERNED:**

- Fixed-suite 95% CI: correctness difference -16.1 to +16.1 percentage points; TPCA ratio 0.539–0.784.
- Task-cluster 95% CI: correctness difference -16.1 to +16.1 percentage points; TPCA ratio 0.339–1.396.
- Claim gates: release-ready=False; fixed-suite substitution=False; cross-task substitution=False.


A positive substitution result means governance compensated for measured capability on this task grid. It does not imply a model parameter count or that the lower-tier route matches the frontier route outside the evaluated work.

## Headline findings

**Cheapest cost-of-pass on T1:** `gpt-5.6-sol` + `specsmith FULL (governed)` at $0.07799

**`gpt-5.6-sol`: SPECSMITH_FULL vs UNGOVERNED on T1** — governance is **1.3× cheaper** per correct answer ($0.07799 vs $0.10046)
**`gpt-5.6-terra`: SPECSMITH_FULL vs UNGOVERNED on T1** — governance is **1.2× cheaper** per correct answer ($0.09337 vs $0.10816)

### Governance gate performance (T1 coding task pass rates)

- **gpt-5.6-sol** — ungoverned: 100% pass / specsmith FULL: 100% pass
- **gpt-5.6-terra** — ungoverned: 80% pass / specsmith FULL: 100% pass

### Key model comparison (T1, mean across 5 reps)

- **gpt-5.6-sol + SPECSMITH_FULL**: 100% pass, 7.9k tokens/run, TPCA 7.9k, $0.0780/run, CoP $0.07799
- **gpt-5.6-sol + UNGOVERNED**: 100% pass, 15.6k tokens/run, TPCA 15.6k, $0.1005/run, CoP $0.10046
- **gpt-5.6-terra + SPECSMITH_FULL**: 100% pass, 19.5k tokens/run, TPCA 19.5k, $0.0934/run, CoP $0.09337
- **gpt-5.6-terra + UNGOVERNED**: 80% pass, 21.8k tokens/run, TPCA 27.2k, $0.0865/run, CoP $0.10816

---

_Generated by `scripts/govern_bench/compare_runs.py`_
