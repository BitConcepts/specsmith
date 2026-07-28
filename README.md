# Specsmith

[![CI](https://github.com/layer1labs/specsmith/actions/workflows/ci.yml/badge.svg)](https://github.com/layer1labs/specsmith/actions/workflows/ci.yml)
[![Docs](https://readthedocs.org/projects/specsmith/badge/?version=stable)](https://specsmith.readthedocs.io/stable/)
[![PyPI](https://img.shields.io/pypi/v/specsmith?label=stable&style=flat&color=blue&cacheSeconds=60)](https://pypi.org/project/specsmith/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Specsmith is a lean governance layer for AI-assisted development. It keeps four
things explicit while your existing coding agent and toolchain do the work:

1. the requirement being changed;
2. the test that proves it;
3. the evidence that was actually observed; and
4. a compact epistemic context that does not turn guesses into facts.

Specsmith is not an IDE, autonomous coding agent, CI replacement, generic skill
catalog, or legal-compliance certificate. It integrates with those tools instead
of duplicating them.

## Install

The CLI is distributed through PyPI and should be isolated with `pipx`:

```bash
pipx install specsmith
specsmith --version
```

Python-library use remains available from an ordinary environment:

```bash
pip install specsmith
```

## Five-minute start

Adopt an existing repository:

```bash
cd your-project
specsmith import --project-dir . --yes
specsmith req add --title "The API returns a stable error envelope"
specsmith test add --req REQ-001 --title "Verify the error envelope" --type integration
specsmith preflight "Implement the error envelope. Scope: REQ-001" --json
```

Let your normal agent edit the code and let your normal test runner execute the
tests. Then close the evidence loop:

```bash
pytest -q                         # or your native test command
specsmith audit --project-dir .
specsmith checkpoint --project-dir .
```

For a new repository, use `specsmith init`. See the
[quick start](https://specsmith.readthedocs.io/stable/quickstart/) for Windows,
Linux, CI, and provider setup.

## The core loop

```text
requirement -> linked test -> accepted preflight -> host edits/tests
            -> verify/audit evidence -> compact trusted context
```

- `req` and `test` maintain requirement-to-test traceability.
- `preflight` classifies intent and stops ambiguous or destructive work.
- `verify`, `audit`, and `checkpoint` preserve observed evidence and uncertainty.
- `compress` and ESDB keep context bounded without promoting unsupported claims.
- `integrate` and MCP expose that contract to coding agents and editors.

Run `specsmith --help` for the small core surface and `specsmith commands` for
the complete supported command list.

## Grace local REPL

Grace is Specsmith's optional local fallback—not a replacement for a coding
agent you already use.

```bash
specsmith run
```

The first run explains provider recovery and useful commands:

```text
grace> /help
grace> /status
grace> /why
grace> /specsmith preflight "Fix config repair. Scope: REQ-001"
```

Grace reports its active provider, model, requirement/test context, token
pressure, and evidence state. Grace is the supported user-facing REPL.

Use `/why` to inspect the evidence behind the current decision.

For CPU-safe local fallback and VRAM-aware recommendations, see the
[local model guide](https://specsmith.readthedocs.io/stable/local-models/).

## Agent integrations

Prefer the host tool's native Git, browser, testing, and framework capabilities.
Specsmith supplies only its distinct governance context.

```bash
specsmith integrate <tool> --project-dir .
specsmith mcp --help
```

- [Agent integration guide](https://specsmith.readthedocs.io/stable/agent-integrations/)
- [Zoo Code / Roo Code setup and config repair](https://specsmith.readthedocs.io/stable/zoo-code-roo/)
- [Invocation strategy](https://specsmith.readthedocs.io/stable/invocation-strategy/)

Zoo Code integration repairs missing, older, and tampered managed configuration
while preserving unrelated user settings. The same generated assets and tests
run on Windows and Linux.

## Policy

Policy stays intentionally small. Keep preflight and linked-test enforcement on;
add approvals only where risk justifies them.

```yaml
required_preflight: true
required_tests: true
required_human_approval:
  - release
risk_threshold: high
```

See the [policy reference](https://specsmith.readthedocs.io/stable/policy/) and
the [`examples/policies`](examples/policies) directory.

## Governance efficiency benchmark

The same-commit GPT-5.6 Sol n=10 replication completed 160/160 valid rows.
FULL passed 80/80 at 10.7k tokens per correct answer (TPCA); the versioned
Cursor-style condition passed 70/80 at 24.8k. On coding-only tasks both passed
60/60, while FULL used 14.3k versus 27.1k TPCA.

The preregistered matched n=10 substitution run found that GPT-5.6 Terra +
FULL passed 80/80 mixed-suite cells at 11.7k TPCA, while frontier Sol raw
passed 65/80 at 28.0k. Both mixed-suite confidence gates passed. The
prespecified coding-only slice favored Terra + FULL (60/60 at 15.6k versus
55/60 at 30.3k), but its correctness interval missed the non-inferiority
margin by 0.7 percentage points. A governed Qwen3.6-27B cell has now passed
the full long-horizon admission. A later n=1 controller diagnostic reduced
that correct cell from 72.3k to 26.9k tokens, but it remains 1.53× the 17.5k
GPT-5.6 Sol envelope and has not passed repeated promotion gates. A fixed-scalar
milestone bundle independently restored correctness at 71.1k tokens; exact-edit
and alternate managed Qwen routes failed. On a hosted Qwen3-Coder-30B
native-tool route, scoped atomic patching cut a failed T28 attempt from 123.4k
to 34.9k tokens, but did not make it correct; forcing tool use regressed to
81.6k. A later literal vLLM `qwen3_xml` run proved native parser compatibility,
but its atomic, scoped, and required-tool cells still failed at 34.1k, 53.5k,
and 181.9k tokens. Milestone packets also failed; independent-validator
authority plus atomic repair cut one failed diagnostic to 18.6k tokens, but it
completed only one of four milestones. Forcing repeated repairs regressed to
98.7k. Specsmith therefore does not claim that small models generally replace
frontier models.

See the
[full benchmark report](https://specsmith.readthedocs.io/stable/efficiency-benchmark/),
[preprint and claim guide](https://specsmith.readthedocs.io/stable/preprint/),
[weakness audit](https://specsmith.readthedocs.io/stable/benchmark-audit/), and
[model comparison](https://specsmith.readthedocs.io/stable/model-comparison/)
for methodology, task-level results, historical receipts, limitations, and
optimization insights.

## ESDB and evidence

SQLite is the free default ESDB. ChronoMemory/ChronoStore is an optional
commercial backend for cryptographic WAL integrity, richer provenance, and
epistemic rollback.

```bash
specsmith esdb status
```

See the [ESDB guide](https://specsmith.readthedocs.io/stable/esdb/) for repair,
licensing, and the Python API. Commercial inquiries:
[licensing@layer1labs.ai](mailto:licensing@layer1labs.ai).

## Development and release quality

The supported baseline is Python 3.10–3.13 on Linux, macOS, and Windows. CI
enforces formatting, Ruff, mypy, strict documentation builds, governance schema
validation, dependency auditing, CodeQL, the full test matrix, and built-wheel
smoke tests.

```bash
ruff format --check src/ tests/
ruff check src/ tests/
pytest tests/ -q
mypy src/specsmith/
mkdocs build --strict
```

Contributor guidance is in [CONTRIBUTING.md](CONTRIBUTING.md). Security reports
belong in [SECURITY.md](SECURITY.md). Release history is in
[CHANGELOG.md](CHANGELOG.md).

## Documentation

- [Stable documentation](https://specsmith.readthedocs.io/stable/)
- [CLI and first steps](https://specsmith.readthedocs.io/stable/standalone-cli/)
- [Requirements and test workflow](https://specsmith.readthedocs.io/stable/governance/)
- [Examples](docs/examples/README.md)

Specsmith is MIT licensed. ChronoMemory is separately licensed; see
[COMMERCIAL-LICENSE.md](COMMERCIAL-LICENSE.md).
