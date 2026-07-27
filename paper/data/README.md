# Compact benchmark evidence

Each directory contains `cells.csv` and `manifest.json`. The manifest records
the cited workflow, immutable commit, source-artifact SHA-256 digest, canonical
cell digest, CSV digest, included fields, and deliberately excluded trace
fields.

| Directory | Workflow | Purpose |
|---|---:|---|
| `substitution-release` | 30210886840 | Preregistered eight-task Terra/Sol raw/FULL n=10 result and coding sensitivity |
| `broad-n10` | 30206398622 | Eight-task GPT-5.6 Sol Cursor-style/FULL replication |
| `screen-n5` | 30206394966 | Four-task Terra/Sol raw/FULL substitution screen |
| `admission-30210897895` | 30210897895 | Initial GPT-4o mini and Llama 3.1 8B negative admissions |
| `admission-30211566178` | 30211566178 | Same admissions after bounded controller repairs |
| `admission-30211920507` | 30211920507 | Final Llama 3.1 8B closing-tag route diagnostic |
| `admission-30265818081` | 30265818081 | Qwen3.6-27B correct n=1 T28/FULL admission; above frontier efficiency envelope |
| `admission-30265830535` | 30265830535 | Qwen3-32B failed n=1 T28/FULL follow-up |
| `admission-30269000016` | 30269000016 | Qwen3.6-27B correct final T28/FULL confirmation; no TPCA gain |
| `controller-30274870047` | 30274870047 | Required-tool control; correct at 42,697 tokens |
| `controller-30274872374` | 30274872374 | Scalar-parallel winner; correct at 26,850 tokens |
| `controller-30277090373` | 30277090373 | Compact-auto negative diagnostic; premature text stop |
| `controller-30277092347` | 30277092347 | Write-only diagnostic; correct at 37,058 tokens |
| `controller-30278261221` | 30278261221 | Repaired compact-auto negative diagnostic; turn exhaustion |
| `controller-30280275590` | 30280275590 | Independent-validator authority diagnostic; correct at 43,622 tokens |

Full raw rows, traces, diffs, and validator output remain in the cited GitHub
Actions artifacts for the configured retention period. They are not copied
into the repository because the paper's statistics require only the compact
measurements, while the larger fields may contain model-generated source or
prompt text.

Verify a compact directory from the repository root:

```bash
python scripts/govern_bench/export_evidence.py \
  --verify-manifest paper/data/screen-n5/manifest.json
```
