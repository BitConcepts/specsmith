# Specsmith GovernanceBench Preprint

This directory contains the source, generated tables, and compact evidence for
the Specsmith GovernanceBench preprint. The reviewed PDF is published at
`output/pdf/specsmith-governancebench-preprint.pdf`.

Regenerate the result include from the repository root:

```powershell
python scripts/govern_bench/render_preprint_results.py `
  --summary paper/data/substitution-release/summary.json `
  --coding-summary paper/data/substitution-release/coding-summary.json `
  --output paper/generated/results.tex `
  --workflow-id 30210886840 `
  --commit-sha 75a8c7911187abe8db2b6ca77f0e08fa7859ffe7
```

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
