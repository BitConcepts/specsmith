# Corrected frozen real-repository replication

Workflow
[30589098641](https://github.com/layer1labs/specsmith/actions/runs/30589098641)
completed protocol `GB-PREPRINT-2026-07-30-V2` at commit
`f2bedf1e06a7da2b27152754c69b15d5584b43d3`.

The grid contains 60 valid T30 cells:

- GPT-5.6 Terra and GPT-5.6 Sol through the OpenAI Responses API;
- raw, versioned Cursor-style, and Specsmith FULL conditions;
- ten repetitions per model/condition;
- no provider retry, skip, error, or censored cell.

| Route and condition | Correct | TPCA | Cost/pass | Failed-token share |
|---|---:|---:|---:|---:|
| Terra raw | 1/10 | 1,316,860 | $4.65094 | 84.0% |
| Terra Cursor-style | 1/10 | 1,165,503 | $3.73937 | 88.1% |
| Terra FULL | 2/10 | 362,650 | $1.46335 | 76.9% |
| Sol raw | 5/10 | 234,526 | $0.66978 | 47.7% |
| Sol Cursor-style | 1/10 | 1,027,057 | $2.94382 | 85.2% |
| Sol FULL | 8/10 | 105,523 | $0.52046 | 26.6% |

Sol FULL reduced TPCA 55.0% versus Sol raw and 89.7% versus the versioned
Cursor-style condition while improving correctness to 8/10 from 5/10 and
1/10. These are large point improvements, but the four within-model joint
uncertainty gates remain false. Terra FULL materially reduced failed
expenditure versus its controls but passed only 2/10. Terra FULL therefore
does not substitute for Sol raw on this task: its correctness is 30 percentage
points lower and its point TPCA ratio is 1.546.

The paired upper TPCA confidence bound is undefined because some bootstrap
resamples contain no correct Sol-raw answer. The serializer records that bound
as JSON `null`, and the superiority claim fails closed.

`manifest.json` authenticates the two raw source artifacts and canonical
60-row CSV. Raw transcripts and diffs remain attached to the workflow rather
than duplicated in Git.
