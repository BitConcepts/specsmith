# chronomemory Changelog

All notable changes to the chronomemory ESDB engine.
Available on [PyPI](https://pypi.org/project/chronomemory/#history).

## [0.2.7] — 2026-06-25

### Changed

- **PyPI-only distribution** — chronomemory is published to PyPI with all required
  wheels; `pip install specsmith[esdb]` installs from PyPI with no extra index.

---

## [0.2.4] — 2026-06-23

### Fixed

- **O(1) WAL append** (`_append_wal`): uses a direct `open("a")` append with the
  current WAL schema.
- **Stale `.wal.tmp` cleanup on `open()`**: interrupted-write temporary files are
  removed before acquiring the write lock.

### Added

- **`conftest.py` CI reliability hook**: guarantees the CI "Check for test failures" step
  has valid pass/fail data even when Python crashes during JUnit XML write on Windows Server 2025.

---

## [0.2.3] — 2026-06-23

### Added

- **Cross-platform single-writer file lock** (`events.wal.lock`) — prevents concurrent writes.
- **Chain validation warning on `open()`** — `RuntimeWarning` if WAL hash chain is broken.
- **WAL auto-compaction threshold** (`max_wal_events`) — keeps WAL size bounded.
- **`__del__` safety net** — `ResourceWarning` if store is GC'd while open.
- **`open()` idempotency** — double-open is a no-op.
- **`EsdbBridge` per-operation lock release** — releases write lock immediately after each call.
- **18 new production-hardening tests**.

### Fixed

- `_WriteLock._try_clear_stale()` Windows `OSError` handling for stale lock detection.

---

## [0.2.2] — 2026-06-22

### Changed

- **`EsdbId` unified to `String`-typed ID** — full bidirectional Python↔Rust WAL replay.

---

## [0.2.1] — 2026-06-22

### Changed

- **Rust↔Python record schema alignment** — `RecordKind`, `RecordStatus`, `EdgeType` now
  serialise with Python-compatible lowercase strings. Fixes `query(kind="fact")` on Rust-written WALs.
- **Serde aliases** for Python vocabulary (`"deprecated"`, `"tombstone"`, etc.).

---

## [0.2.0] — 2026-06-22

### Added

- Production hardening: file locking, auto-compaction, `__del__` safety, startup performance test.

---

## [0.1.8] — 2026-06-22

### Fixed

- `_append_wal()` Windows hash-chain corruption on dual-open pattern.

---

## [0.1.3] — 2026-06-11

### Fixed

- **Hash alignment**: compact JSON separators in WAL hash computation — aligns Python
  `json.dumps` with Rust `serde_json`; fixes cross-language SHA-256 chain verification.

---

## [0.1.2] — 2026-06-11

- First public PyPI release. CI Python↔Rust round-trip.

---

## [0.1.0] — 2026-05-18

- Initial release: `ChronoStore`, `ChronoRecord`, `WalEvent`, `EsdbBridge`.
- NDJSON WAL with SHA-256 hash chain.
- 7 OEA anti-hallucination fields (H15–H22).
- Snapshot + WAL tail replay, tombstone semantics, atomic writes.
- Zero runtime dependencies.

---

[Full release history on PyPI](https://pypi.org/project/chronomemory/#history)
