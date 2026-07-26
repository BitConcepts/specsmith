# specsmith — Governed Project Skill

## Purpose

Specsmith keeps requirements, tests, epistemic context, and verification
evidence aligned while an AI agent works. `AGENTS.md` defines the project
protocol; `.specsmith/` and `.chronomemory/` hold governance state.

## Start a session

```bash
specsmith kill-session
specsmith audit --project-dir .
specsmith sync --project-dir .
specsmith checkpoint --project-dir .
```

Before every code change:

```bash
specsmith preflight "<describe the intended change>" --json
```

Proceed only when the decision is `accepted`. Preserve the returned work item,
requirements, independent tests, and scope.

## Preferred invocation

Use native Specsmith MCP tools when the agent supports them. In Grace, use
`/specsmith <verb>`. For headless automation and CI, call the direct CLI.

```bash
specsmith run
specsmith status --project-dir .
specsmith validate --strict --project-dir .
specsmith audit --project-dir .
specsmith checkpoint --project-dir .
```

## Finish a session

Run the linked independent tests, record only verified claims, then:

```bash
specsmith save --project-dir .
specsmith kill-session
```
