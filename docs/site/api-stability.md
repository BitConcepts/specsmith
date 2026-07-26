# Current API contract

This page defines the current public contract. Current documentation, fixtures,
and release evidence are authoritative; Specsmith does not promise operation
against superseded public surfaces.

## Stable contracts

The following contracts require synchronized documentation, fixtures, and
release evidence when changed:

- `preflight` JSON fields and decision exit codes;
- `verify` JSON fields, equilibrium result, and retry/stop exit codes;
- requirement and linked-test IDs in canonical YAML;
- work-item lifecycle states and project-scoped identity;
- governance checkpoints, ledger event provenance, and ESDB integrity;
- Grace block events consumed by supported integrations.

## Focused CLI contract

Normal help exposes the mission-essential workflow:

```text
init  import  run  preflight  verify  req  test  audit  checkpoint
status  sync  save  integrate  doctor  kill-session  commands
```

`specsmith commands` lists the supporting governance, context, provider, MCP,
policy, ESDB, integration, and validation commands. Git hosting, deployment,
browsers, generic multi-agent orchestration, model leaderboards, dashboards,
voice, patent search, wireframes, and workspaces are not public CLI contracts.

## API-surface snapshot

`specsmith api-surface` emits the machine-readable command, exit-code, and event
surface used by CI. The canonical fixture is
`tests/fixtures/api_surface.json`. Any intentional change must update the fixture,
focused CLI tests, documentation, and changelog in the same reviewed change.

Root-command and event-field changes must update the API-surface fixture,
focused tests, documentation, and changelog together.

## Internal interfaces

Modules under `src/specsmith/agent/`, local cache layout, provider adapters, and
prompt wording may evolve before 1.0. They must not weaken deterministic
preflight, verification, provenance, or user-configuration preservation.

## Release policy

- Published tags and package versions are immutable.
- Release candidates must pass the fixed-point repository workflow before a tag
  is created.
- Consumers should target the current documented surface.
