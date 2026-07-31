# Preserved V1 T28/T29 evidence

Workflow
[30578319069](https://github.com/layer1labs/specsmith/actions/runs/30578319069)
ran protocol `GB-PREPRINT-2026-07-30-V1` at commit
`e9305bb01e5cb861f07ae7f7b01a8bf1a431c574`.

Only independently valid strata are summarized here:

- Sol T28 and T29: raw, Cursor-style, and FULL, n=10;
- Terra T29: raw, Cursor-style, and FULL, n=10.

Terra T28 is not summarized because raw repetitions 4 and 6 ended in bounded
provider timeouts. All V1 T30 rows are invalidated because of the evaluator
defects recorded in `../publication-v1-invalidation.json`.

The generated comparison files contain aggregate metrics and paired
substitution summaries. Raw cell artifacts remain attached to the workflow;
they are deliberately not duplicated in Git.
