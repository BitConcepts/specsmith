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
passed 65/80 at 28.0k. Both mixed-suite confidence gates passed; the separate
coding-only confidence gate remained inconclusive.

For the long-horizon polyglot task, native structured milestone tools with
GPT-5.6 Sol passed an independent 10/10 confirmation at 17.9k TPCA, five turns,
and 1.77% coefficient of variation. The schema change reduced TPCA by 7.2%
from the immediately preceding native controller diagnostic. A frozen-controller
Terra replication was less stable: T28 passed 9/10 at 19.6k TPCA, while a new
independent synthetic repository task initially passed 5/5 at 22.0k TPCA with
0% first-pass completion. A trace-derived v5 screen then passed 5/5 at 18.1k
TPCA and 80% first-pass. Its independent n=10 sample passed 10/10 at 20.1k
TPCA, but first-pass completion fell to 30%; the audit found a recurring UI
test-contract repair in 6/10 observed patch receipts and requires optimization
before another confirmation. Versioned v6 made that invariant explicit:
admission `30545048843` passed first-pass at 17.4k tokens, and n=5
`30545401727` passed 5/5 at 18.7k TPCA with 60% first-pass and no UI repair.
The remaining two repairs were milestone-one Python toolchain mistakes.
Versioned v7 made those constraints explicit and passed an independent 10/10
confirmation at 17.6k TPCA, five turns, 100% first-pass, and 1.62% CV.
These results are task- and route-specific. Managed
20B–32B and Qwen native-tool candidates have useful correct diagnostics but
have not passed the repeated replacement gates, so Specsmith does not claim
that small models generally replace frontier models.

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
