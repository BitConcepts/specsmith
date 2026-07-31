# specsmith Governance Efficiency — Model Comparison

**Models compared:** gpt-5.6-terra (mid) · gpt-5.6-sol (frontier)

> **Primary:** tokens per correct answer (TPCA) = mean_tokens ÷ pass_rate.
> **Secondary:** cost-of-pass (CoP) = estimated mean_cost_per_run ÷ pass_rate.
> Lower is better. ∞ = condition never passed.

## T29

| Condition| gpt-5.6-terra Pass%|Tokens|TPCA|Cost/run|CoP| gpt-5.6-sol Pass%|Tokens|TPCA|Cost/run|CoP|
|----------|------:|------:|------:|--------:|--------:|------:|------:|------:|--------:|--------:|
| Raw agent (ungoverned)| 60%| 69.0k| 115.0k| $0.2827| $0.47119| 90%| 48.5k| 53.9k| $0.2958| $0.32867|
| CLAUDE.md / AGENTS.md| —| —| —| —| —| —| —| —| —| —|
| Cursor .cursor/rules| 80%| 78.8k| 98.4k| $0.3145| $0.39311| 80%| 43.6k| 54.5k| $0.2852| $0.35649|
| GitHub Copilot instructions| —| —| —| —| —| —| —| —| —| —|
| OpenAI Codex CLI AGENTS.md| —| —| —| —| —| —| —| —| —| —|
| Cline .clinerules| —| —| —| —| —| —| —| —| —| —|
| Aider CONVENTIONS.md| —| —| —| —| —| —| —| —| —| —|
| BMAD Blueprint→Milestone| —| —| —| —| —| —| —| —| —| —|
| OpenSpec REQUIREMENTS.md| —| —| —| —| —| —| —| —| —| —|
| Agile BDD / TDD| —| —| —| —| —| —| —| —| —| —|
| specsmith LIGHT (preflight)| —| —| —| —| —| —| —| —| —| —|
| specsmith FULL (governed)| **100%**| 17.6k| 17.6k| $0.1214| **$0.12142**| **100%**| 22.9k| 22.9k| $0.2922| **$0.29217**|

## Cross-task summary

Mean across all tasks shown above.

| Condition| gpt-5.6-terra Pass%|Mean TPCA|Mean CoP|$/mo @20/day| gpt-5.6-sol Pass%|Mean TPCA|Mean CoP|$/mo @20/day|
|----------|------:|--------:|--------:|-----------:|------:|--------:|--------:|-----------:|
| Raw agent (ungoverned)| 60%| 115.0k| $0.47119| $124.39| 90%| 53.9k| $0.32867| $130.15|
| CLAUDE.md / AGENTS.md| —| —| —| —| —| —| —| —|
| Cursor .cursor/rules| 80%| 98.4k| $0.39311| $138.37| 80%| 54.5k| $0.35649| $125.48|
| GitHub Copilot instructions| —| —| —| —| —| —| —| —|
| OpenAI Codex CLI AGENTS.md| —| —| —| —| —| —| —| —|
| Cline .clinerules| —| —| —| —| —| —| —| —|
| Aider CONVENTIONS.md| —| —| —| —| —| —| —| —|
| BMAD Blueprint→Milestone| —| —| —| —| —| —| —| —|
| OpenSpec REQUIREMENTS.md| —| —| —| —| —| —| —| —|
| Agile BDD / TDD| —| —| —| —| —| —| —| —|
| specsmith LIGHT (preflight)| —| —| —| —| —| —| —| —|
| specsmith FULL (governed)| **100%**| **17.6k**| **$0.12142**| **$53.42**| **100%**| **22.9k**| **$0.29217**| **$128.55**|

## Governance as model-capability substitution

This is a 2×2 factorial comparison: both models run both UNGOVERNED and SPECSMITH_FULL on the identical task and repetition grid. The headline pair asks whether the lower-tier governed route can match the frontier ungoverned route; the other two cells preserve the within-model governance controls.

| Lower-tier governed route | Pass | TPCA | CoP | Frontier ungoverned route | Pass | TPCA | CoP | Outcome |
|---|---:|---:|---:|---|---:|---:|---:|---|
| gpt-5.6-terra + FULL | 100% | 17.6k | $0.12142 | gpt-5.6-sol + UNGOVERNED | 90% | 53.9k | $0.32867 | Matches/exceeds correctness with lower TPCA |

**Paired inference — gpt-5.6-terra + FULL vs gpt-5.6-sol + UNGOVERNED:**

- Fixed-suite 95% CI: correctness difference -27.8 to +60.3 percentage points; TPCA ratio 0.258–0.381.
- Task-cluster 95% CI: correctness difference -27.8 to +60.3 percentage points; TPCA ratio 0.260–0.381.
- Claim gates: release-ready=True; fixed-suite substitution=False; cross-task substitution=False.


A positive substitution result means governance compensated for measured capability on this task grid. It does not imply a model parameter count or that the lower-tier route matches the frontier route outside the evaluated work.

## Paired within-model governance gates

These intervals test FULL against each same-model control on matched repetition IDs. Point improvements remain descriptive when the joint correctness-noninferiority and TPCA-superiority gate does not pass.

**gpt-5.6-terra: FULL vs UNGOVERNED:**

- Point correctness difference: +40.0 percentage points; TPCA ratio 0.153.
- Fixed-suite 95% CI: correctness difference -26.0 to +89.2 percentage points; TPCA ratio 0.081–0.217.
- Joint gate: False.

**gpt-5.6-terra: FULL vs CURSOR_RULES:**

- Point correctness difference: +20.0 percentage points; TPCA ratio 0.179.
- Fixed-suite 95% CI: correctness difference -27.8 to +76.3 percentage points; TPCA ratio 0.119–0.228.
- Joint gate: False.

**gpt-5.6-sol: FULL vs UNGOVERNED:**

- Point correctness difference: +10.0 percentage points; TPCA ratio 0.425.
- Fixed-suite 95% CI: correctness difference -27.8 to +60.3 percentage points; TPCA ratio 0.346–0.494.
- Joint gate: False.

**gpt-5.6-sol: FULL vs CURSOR_RULES:**

- Point correctness difference: +20.0 percentage points; TPCA ratio 0.420.
- Fixed-suite 95% CI: correctness difference -27.8 to +76.3 percentage points; TPCA ratio 0.271–0.572.
- Joint gate: False.

## Headline findings

**Cheapest cost-of-pass on T29:** `gpt-5.6-terra` + `specsmith FULL (governed)` at $0.12142

**`gpt-5.6-terra`: SPECSMITH_FULL vs UNGOVERNED on T29** — point estimate: governance is **3.9× cheaper** per correct answer ($0.12142 vs $0.47119)
**`gpt-5.6-sol`: SPECSMITH_FULL vs UNGOVERNED on T29** — point estimate: governance is **1.1× cheaper** per correct answer ($0.29217 vs $0.32867)

### Governance gate performance (T29 coding task pass rates)

- **gpt-5.6-terra** — ungoverned: 60% pass / specsmith FULL: 100% pass
- **gpt-5.6-sol** — ungoverned: 90% pass / specsmith FULL: 100% pass

### Key model comparison (T29, mean across 10 reps)

- **gpt-5.6-terra + SPECSMITH_FULL**: 100% pass, 17.6k tokens/run, TPCA 17.6k, $0.1214/run, CoP $0.12142
- **gpt-5.6-terra + UNGOVERNED**: 60% pass, 69.0k tokens/run, TPCA 115.0k, $0.2827/run, CoP $0.47119
- **gpt-5.6-sol + SPECSMITH_FULL**: 100% pass, 22.9k tokens/run, TPCA 22.9k, $0.2922/run, CoP $0.29217
- **gpt-5.6-sol + UNGOVERNED**: 90% pass, 48.5k tokens/run, TPCA 53.9k, $0.2958/run, CoP $0.32867

---

_Generated by `scripts/govern_bench/compare_runs.py`_
