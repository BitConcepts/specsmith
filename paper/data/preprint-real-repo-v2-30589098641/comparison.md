# specsmith Governance Efficiency — Model Comparison

**Models compared:** gpt-5.6-terra (mid) · gpt-5.6-sol (frontier)

> **Primary:** tokens per correct answer (TPCA) = mean_tokens ÷ pass_rate.
> **Secondary:** cost-of-pass (CoP) = estimated mean_cost_per_run ÷ pass_rate.
> Lower is better. ∞ = condition never passed.

## T30

| Condition| gpt-5.6-terra Pass%|Tokens|TPCA|Cost/run|CoP| gpt-5.6-sol Pass%|Tokens|TPCA|Cost/run|CoP|
|----------|------:|------:|------:|--------:|--------:|------:|------:|------:|--------:|--------:|
| Raw agent (ungoverned)| 10%| 131.7k| 1316.9k| $0.4651| $4.65094| 50%| 117.3k| 234.5k| $0.3349| $0.66978|
| CLAUDE.md / AGENTS.md| —| —| —| —| —| —| —| —| —| —|
| Cursor .cursor/rules| 10%| 116.6k| 1165.5k| $0.3739| $3.73937| 10%| 102.7k| 1027.1k| $0.2944| $2.94382|
| GitHub Copilot instructions| —| —| —| —| —| —| —| —| —| —|
| OpenAI Codex CLI AGENTS.md| —| —| —| —| —| —| —| —| —| —|
| Cline .clinerules| —| —| —| —| —| —| —| —| —| —|
| Aider CONVENTIONS.md| —| —| —| —| —| —| —| —| —| —|
| BMAD Blueprint→Milestone| —| —| —| —| —| —| —| —| —| —|
| OpenSpec REQUIREMENTS.md| —| —| —| —| —| —| —| —| —| —|
| Agile BDD / TDD| —| —| —| —| —| —| —| —| —| —|
| specsmith LIGHT (preflight)| —| —| —| —| —| —| —| —| —| —|
| specsmith FULL (governed)| **20%**| 72.5k| 362.6k| $0.2927| **$1.46335**| **80%**| 84.4k| 105.5k| $0.4164| **$0.52046**|

## Cross-task summary

Mean across all tasks shown above.

| Condition| gpt-5.6-terra Pass%|Mean TPCA|Mean CoP|$/mo @20/day| gpt-5.6-sol Pass%|Mean TPCA|Mean CoP|$/mo @20/day|
|----------|------:|--------:|--------:|-----------:|------:|--------:|--------:|-----------:|
| Raw agent (ungoverned)| 10%| 1316.9k| $4.65094| $204.64| 50%| 234.5k| $0.66978| $147.35|
| CLAUDE.md / AGENTS.md| —| —| —| —| —| —| —| —|
| Cursor .cursor/rules| 10%| 1165.5k| $3.73937| $164.53| 10%| 1027.1k| $2.94382| $129.53|
| GitHub Copilot instructions| —| —| —| —| —| —| —| —|
| OpenAI Codex CLI AGENTS.md| —| —| —| —| —| —| —| —|
| Cline .clinerules| —| —| —| —| —| —| —| —|
| Aider CONVENTIONS.md| —| —| —| —| —| —| —| —|
| BMAD Blueprint→Milestone| —| —| —| —| —| —| —| —|
| OpenSpec REQUIREMENTS.md| —| —| —| —| —| —| —| —|
| Agile BDD / TDD| —| —| —| —| —| —| —| —|
| specsmith LIGHT (preflight)| —| —| —| —| —| —| —| —|
| specsmith FULL (governed)| **20%**| **362.6k**| **$1.46335**| **$128.77**| **80%**| **105.5k**| **$0.52046**| **$183.20**|

## Governance as model-capability substitution

This is a 2×2 factorial comparison: both models run both UNGOVERNED and SPECSMITH_FULL on the identical task and repetition grid. The headline pair asks whether the lower-tier governed route can match the frontier ungoverned route; the other two cells preserve the within-model governance controls.

| Lower-tier governed route | Pass | TPCA | CoP | Frontier ungoverned route | Pass | TPCA | CoP | Outcome |
|---|---:|---:|---:|---|---:|---:|---:|---|
| gpt-5.6-terra + FULL | 20% | 362.6k | $1.46335 | gpt-5.6-sol + UNGOVERNED | 50% | 234.5k | $0.66978 | Does not match stronger-model correctness |

**Paired inference — gpt-5.6-terra + FULL vs gpt-5.6-sol + UNGOVERNED:**

- Fixed-suite 95% CI: correctness difference -94.3 to +65.6 percentage points; TPCA ratio 0.372–undefined.
- Task-cluster 95% CI: correctness difference -94.3 to +63.1 percentage points; TPCA ratio 0.383–undefined.
- Claim gates: release-ready=True; fixed-suite substitution=False; cross-task substitution=False.
- An undefined upper TPCA bound means at least one bootstrap resample had no correct frontier answer; the superiority gate fails closed.


A positive substitution result means governance compensated for measured capability on this task grid. It does not imply a model parameter count or that the lower-tier route matches the frontier route outside the evaluated work.

## Paired within-model governance gates

These intervals test FULL against each same-model control on matched repetition IDs. Point improvements remain descriptive when the joint correctness-noninferiority and TPCA-superiority gate does not pass.

**gpt-5.6-terra: FULL vs UNGOVERNED:**

- Point correctness difference: +10.0 percentage points; TPCA ratio 0.275.
- Fixed-suite 95% CI: correctness difference -58.5 to +74.6 percentage points; TPCA ratio 0.136–undefined.
- Joint gate: False.
- The upper TPCA bound is undefined because a bootstrap resample had no correct control answer; the joint gate fails closed.

**gpt-5.6-terra: FULL vs CURSOR_RULES:**

- Point correctness difference: +10.0 percentage points; TPCA ratio 0.311.
- Fixed-suite 95% CI: correctness difference -58.5 to +74.6 percentage points; TPCA ratio 0.144–undefined.
- Joint gate: False.
- The upper TPCA bound is undefined because a bootstrap resample had no correct control answer; the joint gate fails closed.

**gpt-5.6-sol: FULL vs UNGOVERNED:**

- Point correctness difference: +30.0 percentage points; TPCA ratio 0.450.
- Fixed-suite 95% CI: correctness difference -45.1 to +87.4 percentage points; TPCA ratio 0.222–0.656.
- Joint gate: False.

**gpt-5.6-sol: FULL vs CURSOR_RULES:**

- Point correctness difference: +70.0 percentage points; TPCA ratio 0.103.
- Fixed-suite 95% CI: correctness difference -29.1 to +100.0 percentage points; TPCA ratio 0.075–undefined.
- Joint gate: False.
- The upper TPCA bound is undefined because a bootstrap resample had no correct control answer; the joint gate fails closed.

## Headline findings

**Cheapest cost-of-pass on T30:** `gpt-5.6-sol` + `specsmith FULL (governed)` at $0.52046

**`gpt-5.6-terra`: SPECSMITH_FULL vs UNGOVERNED on T30** — point estimate: governance is **3.2× cheaper** per correct answer ($1.46335 vs $4.65094)
**`gpt-5.6-sol`: SPECSMITH_FULL vs UNGOVERNED on T30** — point estimate: governance is **1.3× cheaper** per correct answer ($0.52046 vs $0.66978)

### Governance gate performance (T30 coding task pass rates)

- **gpt-5.6-terra** — ungoverned: 10% pass / specsmith FULL: 20% pass
- **gpt-5.6-sol** — ungoverned: 50% pass / specsmith FULL: 80% pass

### Key model comparison (T30, mean across 10 reps)

- **gpt-5.6-terra + SPECSMITH_FULL**: 20% pass, 72.5k tokens/run, TPCA 362.6k, $0.2927/run, CoP $1.46335
- **gpt-5.6-terra + UNGOVERNED**: 10% pass, 131.7k tokens/run, TPCA 1316.9k, $0.4651/run, CoP $4.65094
- **gpt-5.6-sol + SPECSMITH_FULL**: 80% pass, 84.4k tokens/run, TPCA 105.5k, $0.4164/run, CoP $0.52046
- **gpt-5.6-sol + UNGOVERNED**: 50% pass, 117.3k tokens/run, TPCA 234.5k, $0.3349/run, CoP $0.66978

---

_Generated by `scripts/govern_bench/compare_runs.py`_
