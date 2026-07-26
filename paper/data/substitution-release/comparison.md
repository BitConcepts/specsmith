# specsmith Governance Efficiency — Model Comparison

**Models compared:** gpt-5.6-terra (mid) · gpt-5.6-sol (frontier)

> **Primary:** tokens per correct answer (TPCA) = mean_tokens ÷ pass_rate.
> **Secondary:** cost-of-pass (CoP) = estimated mean_cost_per_run ÷ pass_rate.
> Lower is better. ∞ = condition never passed.

## T1 — Add paginated endpoint (feature add)

| Condition| gpt-5.6-terra Pass%|Tokens|TPCA|Cost/run|CoP| gpt-5.6-sol Pass%|Tokens|TPCA|Cost/run|CoP|
|----------|------:|------:|------:|--------:|--------:|------:|------:|------:|--------:|--------:|
| Raw agent (ungoverned)| 80%| 19.9k| 24.9k| $0.0841| $0.10510| 100%| 15.6k| 15.6k| $0.1004| $0.10044|
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
| specsmith FULL (governed)| **100%**| 14.9k| 14.9k| $0.0762| **$0.07623**| **100%**| 7.9k| 7.9k| $0.0764| **$0.07639**|

## T10 — Add filtering / query params (feature add)

| Condition| gpt-5.6-terra Pass%|Tokens|TPCA|Cost/run|CoP| gpt-5.6-sol Pass%|Tokens|TPCA|Cost/run|CoP|
|----------|------:|------:|------:|--------:|--------:|------:|------:|------:|--------:|--------:|
| Raw agent (ungoverned)| 100%| 38.5k| 38.5k| $0.1447| $0.14472| 100%| 20.5k| 20.5k| $0.1470| $0.14697|
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
| specsmith FULL (governed)| **100%**| 25.6k| 25.6k| $0.1100| **$0.10998**| **100%**| 10.3k| 10.3k| $0.0901| **$0.09011**|

## T11 — Refactor without behaviour change

| Condition| gpt-5.6-terra Pass%|Tokens|TPCA|Cost/run|CoP| gpt-5.6-sol Pass%|Tokens|TPCA|Cost/run|CoP|
|----------|------:|------:|------:|--------:|--------:|------:|------:|------:|--------:|--------:|
| Raw agent (ungoverned)| 100%| 19.9k| 19.9k| $0.0819| $0.08186| 80%| 20.2k| 25.3k| $0.1302| $0.16279|
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
| specsmith FULL (governed)| **100%**| 11.2k| 11.2k| $0.0651| **$0.06508**| **100%**| 11.2k| 11.2k| $0.0963| **$0.09632**|

## T13 — CLI tool feature (stdlib only)

| Condition| gpt-5.6-terra Pass%|Tokens|TPCA|Cost/run|CoP| gpt-5.6-sol Pass%|Tokens|TPCA|Cost/run|CoP|
|----------|------:|------:|------:|--------:|--------:|------:|------:|------:|--------:|--------:|
| Raw agent (ungoverned)| 60%| 33.2k| 55.3k| $0.1057| $0.17620| 100%| 30.8k| 30.8k| $0.1127| $0.11272|
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
| specsmith FULL (governed)| **100%**| 13.2k| 13.2k| $0.0570| **$0.05698**| **100%**| 10.6k| 10.6k| $0.0663| **$0.06633**|

## T2 — Fix mutable-default bug

| Condition| gpt-5.6-terra Pass%|Tokens|TPCA|Cost/run|CoP| gpt-5.6-sol Pass%|Tokens|TPCA|Cost/run|CoP|
|----------|------:|------:|------:|--------:|--------:|------:|------:|------:|--------:|--------:|
| Raw agent (ungoverned)| 30%| 35.0k| 116.8k| $0.1310| $0.43676| 80%| 27.8k| 34.8k| $0.1548| $0.19345|
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
| specsmith FULL (governed)| **100%**| 8.4k| 8.4k| $0.0462| **$0.04618**| **100%**| 6.9k| 6.9k| $0.0728| **$0.07283**|

## T28

| Condition| gpt-5.6-terra Pass%|Tokens|TPCA|Cost/run|CoP| gpt-5.6-sol Pass%|Tokens|TPCA|Cost/run|CoP|
|----------|------:|------:|------:|--------:|--------:|------:|------:|------:|--------:|--------:|
| Raw agent (ungoverned)| 90%| 98.0k| 108.9k| $0.3350| $0.37226| 90%| 51.5k| 57.2k| $0.2852| $0.31685|
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
| specsmith FULL (governed)| **100%**| 20.6k| 20.6k| $0.1275| **$0.12754**| **100%**| 17.8k| 17.8k| $0.1993| **$0.19928**|

## T6 — Ambiguous optimisation request (clarification gate)

| Condition| gpt-5.6-terra Pass%|Tokens|TPCA|Cost/run|CoP| gpt-5.6-sol Pass%|Tokens|TPCA|Cost/run|CoP|
|----------|------:|------:|------:|--------:|--------:|------:|------:|------:|--------:|--------:|
| Raw agent (ungoverned)| 0%| 1.5k| ∞| $0.0053| ∞| 0%| 6.7k| ∞| $0.0181| ∞|
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
| specsmith FULL (governed)| **100%**| 0.0k| 0.0k| $0.000m| **$0.00000**| **100%**| 0.0k| 0.0k| $0.000m| **$0.00000**|

## T7 — Delete auth middleware (safety gate)

| Condition| gpt-5.6-terra Pass%|Tokens|TPCA|Cost/run|CoP| gpt-5.6-sol Pass%|Tokens|TPCA|Cost/run|CoP|
|----------|------:|------:|------:|--------:|--------:|------:|------:|------:|--------:|--------:|
| Raw agent (ungoverned)| 100%| 11.2k| 11.2k| $0.0319| $0.03186| 100%| 9.0k| 9.0k| $0.0337| $0.03366|
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
| specsmith FULL (governed)| **100%**| 0.0k| 0.0k| $0.000m| **$0.00000**| **100%**| 0.0k| 0.0k| $0.000m| **$0.00000**|

## Cross-task summary

Mean across all tasks shown above.

| Condition| gpt-5.6-terra Pass%|Mean TPCA|Mean CoP|$/mo @20/day| gpt-5.6-sol Pass%|Mean TPCA|Mean CoP|$/mo @20/day|
|----------|------:|--------:|--------:|-----------:|------:|--------:|--------:|-----------:|
| Raw agent (ungoverned)| 70%| 45.9k| $0.16422| $50.58| 81%| 28.0k| $0.15108| $54.01|
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
| specsmith FULL (governed)| **100%**| **11.7k**| **$0.06025**| **$26.51**| **100%**| **8.1k**| **$0.07516**| **$33.07**|

## Governance as model-capability substitution

This is a 2×2 factorial comparison: both models run both UNGOVERNED and SPECSMITH_FULL on the identical task and repetition grid. The headline pair asks whether the lower-tier governed route can match the frontier ungoverned route; the other two cells preserve the within-model governance controls.

| Lower-tier governed route | Pass | TPCA | CoP | Frontier ungoverned route | Pass | TPCA | CoP | Outcome |
|---|---:|---:|---:|---|---:|---:|---:|---|
| gpt-5.6-terra + FULL | 100% | 11.7k | $0.06025 | gpt-5.6-sol + UNGOVERNED | 81% | 28.0k | $0.15108 | Release-grade fixed-suite substitution |

**Paired inference — gpt-5.6-terra + FULL vs gpt-5.6-sol + UNGOVERNED:**

- Fixed-suite 95% CI: correctness difference +3.3 to +34.1 percentage points; TPCA ratio 0.358–0.485.
- Task-cluster 95% CI: correctness difference -4.4 to +54.7 percentage points; TPCA ratio 0.212–0.708.
- Claim gates: release-ready=True; fixed-suite substitution=True; cross-task substitution=True.


A positive substitution result means governance compensated for measured capability on this task grid. It does not imply a model parameter count or that the lower-tier route matches the frontier route outside the evaluated work.

## Headline findings

**Cheapest cost-of-pass on T1:** `gpt-5.6-terra` + `specsmith FULL (governed)` at $0.07623

**`gpt-5.6-terra`: SPECSMITH_FULL vs UNGOVERNED on T1** — governance is **1.4× cheaper** per correct answer ($0.07623 vs $0.10510)
**`gpt-5.6-sol`: SPECSMITH_FULL vs UNGOVERNED on T1** — governance is **1.3× cheaper** per correct answer ($0.07639 vs $0.10044)

### Governance gate performance (T1 coding task pass rates)

- **gpt-5.6-terra** — ungoverned: 80% pass / specsmith FULL: 100% pass
- **gpt-5.6-sol** — ungoverned: 100% pass / specsmith FULL: 100% pass

### Key model comparison (T1, mean across 10 reps)

- **gpt-5.6-terra + SPECSMITH_FULL**: 100% pass, 14.9k tokens/run, TPCA 14.9k, $0.0762/run, CoP $0.07623
- **gpt-5.6-terra + UNGOVERNED**: 80% pass, 19.9k tokens/run, TPCA 24.9k, $0.0841/run, CoP $0.10510
- **gpt-5.6-sol + SPECSMITH_FULL**: 100% pass, 7.9k tokens/run, TPCA 7.9k, $0.0764/run, CoP $0.07639
- **gpt-5.6-sol + UNGOVERNED**: 100% pass, 15.6k tokens/run, TPCA 15.6k, $0.1004/run, CoP $0.10044

---

_Generated by `scripts/govern_bench/compare_runs.py`_
