# Epistemic Chat Handoffs

Specsmith condenses chat context through an extractive handoff envelope rather
than an ungrounded prose summary. Each retained excerpt has a stable source ID,
the envelope declares its confidence and uncertainty, and recipients are told to
verify source IDs before relying on an excerpt as a decision.

At Tier 2 context pressure, Specsmith stores the envelope as an ESDB
`chat_handoff` record and retains a compact rendering in the active history.
Zoo-Code can export the same portable JSON envelope:

```powershell
specsmith zoo-code export-handoff --project-dir . --output handoff.json
```

## Session Storage and Git

`.chronomemory/session-events.jsonl` is the canonical session continuity log.
It is deterministic text, supports review and branch reconciliation, and is
replayed on session load. `.specsmith/esdb.sqlite3` and its WAL sidecars are
local derived indexes; do not commit or manually merge them.
