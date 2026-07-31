# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Layer1Labs Silicon, Inc. All rights reserved.
"""Explicit opt-in local retrieval index (RAG foundation)."""

from __future__ import annotations

import json
import math
import re
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path
from typing import Any

_INDEX_PATH = Path(".specsmith") / "retrieval-index.json"
_TEXT_EXTS = {
    ".md",
    ".txt",
    ".py",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".css",
    ".scss",
    ".rst",
    ".proto",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".go",
    ".rs",
    ".c",
    ".cpp",
    ".h",
    ".java",
    ".sh",
    ".ps1",
    ".cmd",
}
_SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "dist", "build", ".mypy_cache"}
_ROLE_INDEX_VERSION = "role-v1"


#: Infrastructure record kinds excluded from the RAG index (critical rule §18).
#: Mirrors chronomemory ``query.what_is_known()`` so the free SQLite backend
#: produces the same retrieval context as the commercial ChronoStore (REQ-422).
_RAG_EXCLUDE_KINDS = frozenset(
    {
        "edge",
        "rollback_event",
        "token_metric",
        "skill_run",
        "efficiency_metric",
        "context_usage",
    },
)


def _path_role(path: str) -> str:
    """Return a compact deterministic role label for repository retrieval."""

    normalized = path.replace("\\", "/").casefold()
    name = normalized.rsplit("/", 1)[-1]
    if "/test" in f"/{normalized}" or name.startswith("test_") or ".test." in name:
        return "acceptance and regression tests"
    if normalized.endswith((".md", ".rst")) or normalized.startswith("docs/"):
        return "documentation and user contract"
    if normalized.endswith((".css", ".scss")):
        return "user-interface styling"
    if normalized.endswith((".tsx", ".jsx", ".vue", ".svelte")):
        return "interactive user interface"
    if "schema" in normalized or normalized.endswith((".proto", ".graphql")):
        return "shared data contract"
    if "api" in normalized or "route" in normalized or "endpoint" in normalized:
        return "service API boundary"
    if normalized.endswith((".yml", ".yaml", ".toml", ".json")):
        return "configuration and build contract"
    if name in {"main.py", "main.go", "main.ts", "index.ts", "app.py", "app.tsx"}:
        return "application entry point"
    return "implementation module"


_SYMBOL_PATTERNS = (
    re.compile(r"^\s*(?:async\s+)?(?:def|class)\s+([A-Za-z_][\w]*)", re.MULTILINE),
    re.compile(
        r"^\s*(?:export\s+)?(?:async\s+)?(?:function|class|interface|type|const)"
        r"\s+([A-Za-z_$][\w$]*)",
        re.MULTILINE,
    ),
    re.compile(r"^\s*(?:func|type)\s+(?:\([^)]*\)\s*)?([A-Za-z_][\w]*)", re.MULTILINE),
)
_DEPENDENCY_PATTERNS = (
    re.compile(r"^\s*(?:from|import)\s+([A-Za-z0-9_.@/\-]+)", re.MULTILINE),
    re.compile(r"(?:from\s+|require\()[\"']([^\"']+)", re.MULTILINE),
    re.compile(r"^\s*import\s+(?:\w+\s+)?[\"']([^\"']+)[\"']", re.MULTILINE),
)


def _represent_file(path: str, content: str) -> dict[str, Any]:
    symbols: list[str] = []
    dependencies: list[str] = []
    for pattern in _SYMBOL_PATTERNS:
        symbols.extend(pattern.findall(content))
    for pattern in _DEPENDENCY_PATTERNS:
        dependencies.extend(pattern.findall(content))
    symbols = list(dict.fromkeys(str(item) for item in symbols if str(item).strip()))[:12]
    dependencies = list(dict.fromkeys(str(item) for item in dependencies if str(item).strip()))[:12]
    role = _path_role(path)
    summary_parts = [f"role={role}"]
    if symbols:
        summary_parts.append("symbols=" + ", ".join(symbols))
    if dependencies:
        summary_parts.append("depends=" + ", ".join(dependencies))
    return {
        "path": path,
        "content": content,
        "role": role,
        "role_summary": "; ".join(summary_parts),
        "symbols": symbols,
        "dependencies": dependencies,
        "representation": _ROLE_INDEX_VERSION,
        "source_chars": len(content),
    }


def build_role_entries(
    root: Path,
    *,
    paths: Sequence[str] | None = None,
    max_source_chars: int = 24_000,
) -> list[dict[str, Any]]:
    """Build compact role-aware representations for a repository or path set."""

    resolved = root.resolve()
    candidates: Iterable[Path] = (
        (resolved / path for path in paths) if paths is not None else resolved.rglob("*")
    )
    entries: list[dict[str, Any]] = []
    for candidate in candidates:
        try:
            relative = candidate.resolve().relative_to(resolved)
        except (OSError, ValueError):
            continue
        if (
            not candidate.is_file()
            or candidate.suffix.casefold() not in _TEXT_EXTS
            or any(
                part in _SKIP_DIRS or part in {".specsmith", ".chronomemory"}
                for part in relative.parts
            )
        ):
            continue
        try:
            content = candidate.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if content.strip():
            entries.append(_represent_file(relative.as_posix(), content[:max_source_chars]))
    return sorted(entries, key=lambda entry: str(entry["path"]))


def _query_tokens(value: str) -> list[str]:
    return [token for token in re.findall(r"[a-zA-Z0-9_\-]+", value.casefold()) if len(token) > 1]


def rank_role_entries(
    entries: Sequence[Mapping[str, Any]],
    query: str,
    *,
    failure_context: str = "",
    limit: int = 5,
) -> list[dict[str, Any]]:
    """Rank role representations with deterministic BM25 and path boosts."""

    query_terms = _query_tokens(f"{query} {failure_context}")
    failure_terms = set(_query_tokens(failure_context))
    if not query_terms or limit <= 0:
        return []
    documents = [
        _query_tokens(
            " ".join(
                [
                    str(entry.get("path", "")),
                    str(entry.get("role_summary", "")),
                    " ".join(str(value) for value in entry.get("symbols", []) or []),
                    " ".join(str(value) for value in entry.get("dependencies", []) or []),
                ]
            )
        )
        for entry in entries
    ]
    average_length = sum(map(len, documents)) / max(1, len(documents))
    document_frequency = {
        term: sum(1 for document in documents if term in document) for term in set(query_terms)
    }
    scored: list[dict[str, Any]] = []
    for entry, document in zip(entries, documents, strict=True):
        frequencies = {term: document.count(term) for term in set(query_terms)}
        score = 0.0
        for term in query_terms:
            frequency = frequencies.get(term, 0)
            if not frequency:
                continue
            df = document_frequency[term]
            inverse_frequency = math.log(1.0 + (len(documents) - df + 0.5) / (df + 0.5))
            denominator = frequency + 1.5 * (
                1.0 - 0.75 + 0.75 * len(document) / max(1.0, average_length)
            )
            score += inverse_frequency * frequency * 2.5 / denominator
        path = str(entry.get("path", "")).casefold()
        score += 0.35 * sum(1 for term in set(query_terms) if term in path)
        symbol_text = " ".join(str(value) for value in entry.get("symbols", []) or []).casefold()
        score += 1.5 * sum(1 for term in failure_terms if term in path or term in symbol_text)
        if score > 0:
            row = dict(entry)
            row["score"] = round(score, 6)
            scored.append(row)
    return sorted(scored, key=lambda item: (-float(item["score"]), str(item["path"])))[:limit]


def render_role_packet(entries: Sequence[Mapping[str, Any]]) -> str:
    """Render the smallest useful repository map without injecting source bodies."""

    if not entries:
        return ""
    lines = ["## Retrieved repository roles"]
    for entry in entries:
        lines.append(
            f"- {entry.get('path', '')}: {entry.get('role_summary', entry.get('role', ''))}"
        )
    lines.append("Retrieve exact source only for the active requirement boundary.")
    return "\n".join(lines)


def build_index(root: Path, *, include_ledger: bool = False, external: str = "") -> str:
    """Build or refresh the local retrieval index.

    H18 (RAG retrieval filtering): only records with confidence >= 0.6 are
    included in the retrieval context. REQ-422: parity across backends — the
    ChronoStore WAL is used when present, otherwise the free SQLite ESDB backend
    supplies the same governance knowledge so RAG works without commercial deps.
    """
    entries: list[dict[str, Any]] = []

    # H18: inject high-confidence ESDB records as retrieval context.
    # Infrastructure records (see _RAG_EXCLUDE_KINDS) are excluded — rule §18.
    wal = root / ".chronomemory" / "events.wal"
    if wal.exists():
        # ChronoStore branch (commercial backend). Use query.what_is_known()
        # so infrastructure records are excluded from the RAG index.
        try:
            from chronomemory import ChronoStore
            from chronomemory import query as _cm_query

            with ChronoStore(root) as store:
                for rec in _cm_query.what_is_known(store):
                    if rec.data:
                        content = (
                            f"[{rec.kind.upper()} {rec.id}] {rec.label}\n"
                            + str(rec.data.get("description", rec.data.get("title", "")))[:500]
                        )
                        entries.append(
                            {
                                "path": f".chronomemory/{rec.kind}/{rec.id}",
                                "content": content,
                                "source_type": rec.source_type,
                                "confidence": str(rec.confidence),
                            },
                        )
        except Exception:  # noqa: BLE001
            pass  # ChronoStore read failure is non-fatal for RAG
    else:
        # SQLite parity branch (free default backend) — REQ-422. Inject the same
        # high-confidence governance knowledge via SqliteStore.query(rag_filter)
        # (confidence >= 0.6, active only), excluding infrastructure kinds.
        sqlite_path = root / ".specsmith" / "esdb.sqlite3"
        if sqlite_path.exists():
            try:
                from specsmith.esdb import SqliteStore

                with SqliteStore(root) as store:
                    for rec in store.query(rag_filter=True):
                        if rec.kind in _RAG_EXCLUDE_KINDS or not rec.data:
                            continue
                        content = (
                            f"[{rec.kind.upper()} {rec.id}] {rec.label}\n"
                            + str(rec.data.get("description", rec.data.get("title", "")))[:500]
                        )
                        entries.append(
                            {
                                "path": f"esdb/{rec.kind}/{rec.id}",
                                "content": content,
                                "source_type": str(rec.data.get("source_type", "observed")),
                                "confidence": str(rec.confidence),
                            },
                        )
            except Exception:  # noqa: BLE001
                pass  # SQLite read failure is non-fatal for RAG
    candidates: list[Path] = []

    for rel in ["AGENTS.md", "docs/REQUIREMENTS.md", "docs/ARCHITECTURE.md", "docs/TESTS.md"]:
        fp = root / rel
        if fp.exists():
            candidates.append(fp)
    if include_ledger:
        for rel in ["LEDGER.md", "docs/LEDGER.md"]:
            fp = root / rel
            if fp.exists():
                candidates.append(fp)

    ext_path = Path(external).resolve() if external else None
    if ext_path and ext_path.exists():
        if ext_path.is_file():
            candidates.append(ext_path)
        else:
            for fp in ext_path.rglob("*"):
                if fp.is_file() and fp.suffix.lower() in _TEXT_EXTS:
                    candidates.append(fp)

    for src_dir in [root / "src", root / "client", root / "server", root / "shared"]:
        if not src_dir.exists():
            continue
        for fp in src_dir.rglob("*"):
            if (
                fp.is_file()
                and fp.suffix.lower() in _TEXT_EXTS
                and not any(part in _SKIP_DIRS for part in fp.parts)
            ):
                candidates.append(fp)

    for fp in sorted(set(candidates)):
        try:
            text = fp.read_text(encoding="utf-8", errors="ignore")
        except Exception:  # noqa: BLE001
            continue
        if not text.strip():
            continue
        path = str(fp.relative_to(root)) if fp.is_relative_to(root) else str(fp)
        entries.append(_represent_file(path.replace("\\", "/"), text[:12000]))

    index_path = root / _INDEX_PATH
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(json.dumps({"entries": entries}, indent=2), encoding="utf-8")
    return f"Indexed {len(entries)} file(s) into {index_path.relative_to(root)}"


def search_index(
    root: Path,
    query: str,
    *,
    limit: int = 5,
    failure_context: str = "",
    include_source: bool = False,
) -> str:
    """Search the local index using role-aware BM25 ranking."""
    index_path = root / _INDEX_PATH
    if not index_path.exists():
        return "[NOT INDEXED] Run `specsmith index` first."

    data = json.loads(index_path.read_text(encoding="utf-8"))
    entries = data.get("entries", [])
    if not _query_tokens(f"{query} {failure_context}"):
        return "[ERROR] Query must include at least one keyword."
    represented = [
        entry
        if entry.get("role_summary")
        else _represent_file(str(entry.get("path", "")), str(entry.get("content", "")))
        for entry in entries
    ]
    ranked = rank_role_entries(
        represented,
        query,
        failure_context=failure_context,
        limit=limit,
    )
    if not ranked:
        return f"No indexed matches for '{query}'."
    lines = [f"Top {len(ranked)} result(s) for '{query}':"]
    for entry in ranked:
        preview = str(entry.get("role_summary") or entry.get("role") or "")
        if include_source:
            content = str(entry.get("content", "")).strip().replace("\r\n", "\n")
            preview += "\n" + "\n".join(content.splitlines()[:8])
        lines.append(f"\n[{entry['score']}] {entry.get('path', '')}\n{preview}")
    return "\n".join(lines)
