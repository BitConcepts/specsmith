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
| `controller-30286692090` | 30286692090 | Managed Qwen route isolation; Coder-Next and Coder-480B failed |
| `controller-30287970034` | 30287970034 | Exact single-hunk edit diagnostic before evidence-aware loop accounting |
| `controller-30287972114` | 30287972114 | Initial fixed-scalar milestone-bundle diagnostics |
| `controller-30289264577` | 30289264577 | Evidence-aware exact-edit diagnostic; unchanged repair failure |
| `controller-30289266484` | 30289266484 | Qwen3.6 bundle correct at 71,090 tokens; Coder-480B failed |
| `qwen-native-parser-censored-30317300977` | 30317300977 | Literal vLLM `qwen3_xml` endpoint attempt censored before provisioning by missing HF endpoint-write permission |
| `qwen-native-tools-30317439173` | 30317439173 | Hosted Qwen3-Coder-30B atomic-patch baseline; failed at 123,384 tokens |
| `qwen-native-tools-scoped-30317963475` | 30317963475 | Scoped atomic-patch diagnostic; failed at 34,892 tokens after cutting failure spend |
| `qwen-native-tools-required-30318295306` | 30318295306 | Required-tool diagnostic; failed at 81,648 tokens in a repeated action-batch loop |
| `qwen-literal-native-atomic-30358919239` | 30358919239 | Literal vLLM `qwen3_xml` atomic-patch cell; failed at 34,146 tokens |
| `qwen-literal-native-scoped-30358919239` | 30358919239 | Literal vLLM `qwen3_xml` scoped cell; failed at 53,451 tokens |
| `qwen-literal-native-required-30359943752` | 30359943752 | Literal vLLM `qwen3_xml` required-tool cell; failed at 181,884 tokens and the turn cap |

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
