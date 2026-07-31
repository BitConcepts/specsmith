# Specsmith GovernanceBench Preprint

This directory contains the source, generated tables, and compact evidence for
the Specsmith GovernanceBench preprint. The repository review copy is rendered
to `output/pdf/specsmith-governancebench-preprint.pdf`; it has not been
submitted to a preprint server.

Regenerate the result include from the repository root:

```powershell
python scripts/govern_bench/render_preprint_results.py `
  --summary paper/data/substitution-release/summary.json `
  --coding-summary paper/data/substitution-release/coding-summary.json `
  --output paper/generated/results.tex `
  --workflow-id 30210886840 `
  --commit-sha 75a8c7911187abe8db2b6ca77f0e08fa7859ffe7
```

Verify the corrected real-repository evidence:

```powershell
python scripts/govern_bench/export_evidence.py `
  --verify-manifest paper/data/preprint-real-repo-v2-30589098641/manifest.json `
  --source-dir tmp/preprint-run-30589098641
```

The raw Terra and Sol artifacts are attached to workflow `30589098641`.
`paper/data/publication-v1-invalidation.json` records why V1 T30 is excluded,
and `paper/data/publication-readiness-status.json` records the completed claim
gates and remaining external-validity boundary.

Build the PDF:

```powershell
Set-Location paper
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

The paper is generated from cited GitHub Actions benchmark artifacts. Raw
provider transcripts remain attached to those workflows for the configured
artifact-retention period; `data/` permanently stores the compact per-cell
measurements and source digests needed to reproduce the reported statistics.
The benchmark harness, task fixtures, hidden acceptance oracles, pricing
estimates, and deterministic analysis are versioned in this repository.

Before public submission, replace the collective author line only if the human
authors want individual attribution. Do not change numerical claims manually;
regenerate `generated/results.tex` from the archived compact data.
