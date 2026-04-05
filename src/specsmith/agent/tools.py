# SPDX-License-Identifier: MIT
# Copyright (c) 2026 BitConcepts, LLC. All rights reserved.
"""specsmith tool registry — maps specsmith CLI commands to agent-callable tools.

Inspired by ECC's principle: specsmith commands become native tools so the
agent can call them directly without shell invocation.

Tool categories:
  - Governance: audit, validate, diff, export, doctor
  - VCS: commit, push, sync, branch, pr
  - AEE: stress-test, epistemic-audit, belief-graph, trace
  - Scaffold: init, import, upgrade
  - Ledger: add, list, stats
  - Credits: record, summary
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from specsmith.agent.core import Tool, ToolParam


def _run_specsmith(args: list[str], project_dir: str = ".") -> str:
    """Execute a specsmith command and return combined stdout+stderr."""
    cmd = [sys.executable, "-m", "specsmith"] + args + ["--project-dir", project_dir]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
        )
        output = (result.stdout + result.stderr).strip()
        if result.returncode != 0:
            return f"[exit {result.returncode}]\n{output}"
        return output or "(no output)"
    except subprocess.TimeoutExpired:
        return "[TIMEOUT] Command exceeded 120s"
    except Exception as e:  # noqa: BLE001
        return f"[ERROR] {e}"


def build_tool_registry(project_dir: str = ".") -> list[Tool]:
    """Build the full specsmith tool registry for the agentic client.

    Returns a list of Tool objects that the LLM can call.
    Each tool maps to one or more specsmith CLI commands.
    """
    pd = project_dir

    tools = [
        # ----------------------------------------------------------------
        # Governance tools
        # ----------------------------------------------------------------
        Tool(
            name="audit",
            description=(
                "Run specsmith audit: governance health checks (file existence, "
                "REQ↔TEST coverage, ledger health, governance size). "
                "Use --fix to auto-repair simple issues."
            ),
            params=[
                ToolParam("fix", "If 'true', attempt to auto-fix issues", required=False),
            ],
            handler=lambda fix="false": _run_specsmith(
                ["audit"] + (["--fix"] if fix == "true" else []), pd
            ),
            epistemic_claims=["Governance files are present and consistent"],
            uncertainty_bounds="Cannot verify runtime behavior or test correctness",
        ),
        Tool(
            name="validate",
            description=(
                "Run specsmith validate: check governance file consistency "
                "(req ↔ test ↔ arch), detect H11 blocking loops, check AGENTS.md refs."
            ),
            params=[],
            handler=lambda: _run_specsmith(["validate"], pd),
            epistemic_claims=["Requirements and tests are consistently linked"],
            uncertainty_bounds="Does not verify semantic correctness of requirements",
        ),
        Tool(
            name="epistemic_audit",
            description=(
                "Run the full AEE epistemic audit pipeline: "
                "Frame → Disassemble → Stress-Test → Failure-Mode Graph → "
                "Certainty scoring → Recovery proposals. "
                "Use this for deep knowledge quality checks."
            ),
            params=[
                ToolParam(
                    "threshold",
                    "Certainty threshold 0.0-1.0 (default 0.7)",
                    required=False,
                ),
            ],
            handler=lambda threshold="0.7": _run_specsmith(
                ["epistemic-audit", "--threshold", threshold], pd
            ),
            epistemic_claims=["Belief artifacts are stress-tested and at equilibrium"],
            uncertainty_bounds=(
                "Heuristic analysis only. Logic Knot detection uses pattern matching, "
                "not formal logic. Cannot guarantee completeness."
            ),
        ),
        Tool(
            name="stress_test",
            description=(
                "Run AEE stress-tests against docs/REQUIREMENTS.md. "
                "Applies 8 adversarial challenge functions per requirement, "
                "detects Logic Knots, emits recovery proposals."
            ),
            params=[
                ToolParam("format", "Output format: text or mermaid", required=False),
            ],
            handler=lambda format="text": _run_specsmith(  # noqa: A002
                ["stress-test", "--format", format], pd
            ),
            epistemic_claims=["Requirements survive adversarial challenges"],
            uncertainty_bounds="Pattern-based, not formal proof",
        ),
        Tool(
            name="belief_graph",
            description=(
                "Render the belief artifact dependency graph. Shows requirements "
                "as BeliefArtifacts with confidence scores, failure counts, "
                "and inferential links."
            ),
            params=[
                ToolParam("format", "text or mermaid", required=False),
                ToolParam("component", "Filter by component code (e.g. CLI, AEE)", required=False),
            ],
            handler=lambda format="text", component="": _run_specsmith(  # noqa: A002
                ["belief-graph", "--format", format]
                + (["--component", component] if component else []),
                pd,
            ),
        ),
        Tool(
            name="diff",
            description="Compare governance files against spec templates. Shows what has drifted.",
            params=[],
            handler=lambda: _run_specsmith(["diff"], pd),
        ),
        Tool(
            name="export",
            description=(
                "Generate a compliance and coverage report with REQ↔TEST matrix, "
                "audit summary, and governance inventory."
            ),
            params=[],
            handler=lambda: _run_specsmith(["export"], pd),
        ),
        Tool(
            name="doctor",
            description="Check if verification tools (ruff, mypy, pytest, etc.) are installed.",
            params=[],
            handler=lambda: _run_specsmith(["doctor"], pd),
        ),
        # ----------------------------------------------------------------
        # VCS tools
        # ----------------------------------------------------------------
        Tool(
            name="commit",
            description=(
                "Stage, audit, and commit with a governance-aware commit message. "
                "Checks LEDGER.md is updated and runs audit before committing."
            ),
            params=[
                ToolParam("message", "Override commit message", required=False),
            ],
            handler=lambda message="": _run_specsmith(
                ["commit"] + (["-m", message] if message else []), pd
            ),
        ),
        Tool(
            name="push",
            description="Push current branch with safety checks (blocks direct-to-main).",
            params=[],
            handler=lambda: _run_specsmith(["push"], pd),
        ),
        Tool(
            name="sync",
            description="Pull latest changes and warn on governance file conflicts.",
            params=[],
            handler=lambda: _run_specsmith(["sync"], pd),
        ),
        Tool(
            name="create_pr",
            description=(
                "Create a PR with governance context (ledger summary, audit results). "
                "Targets the correct base branch per branching strategy."
            ),
            params=[
                ToolParam("title", "PR title", required=False),
                ToolParam("draft", "'true' to create as draft", required=False),
            ],
            handler=lambda title="", draft="false": _run_specsmith(
                ["pr"]
                + (["--title", title] if title else [])
                + (["--draft"] if draft == "true" else []),
                pd,
            ),
        ),
        Tool(
            name="create_branch",
            description="Create a branch following the project's branching strategy.",
            params=[
                ToolParam("name", "Branch name (e.g. feature/aee-integration)"),
            ],
            handler=lambda name: _run_specsmith(["branch", "create", name], pd),
        ),
        # ----------------------------------------------------------------
        # Ledger tools
        # ----------------------------------------------------------------
        Tool(
            name="ledger_add",
            description=(
                "Add a structured entry to LEDGER.md. Use this after completing "
                "any significant task to maintain session continuity."
            ),
            params=[
                ToolParam("description", "Entry description (what was done)"),
                ToolParam("entry_type", "task, feature, fix, refactor, docs", required=False),
                ToolParam("reqs", "Affected REQ IDs (comma-separated)", required=False),
            ],
            handler=lambda description, entry_type="task", reqs="": _run_specsmith(
                ["ledger", "add", "--type", entry_type, "--reqs", reqs, description], pd
            ),
        ),
        Tool(
            name="ledger_list",
            description="List recent ledger entries to understand session state.",
            params=[],
            handler=lambda: _run_specsmith(["ledger", "list"], pd),
        ),
        # ----------------------------------------------------------------
        # Trace vault tools
        # ----------------------------------------------------------------
        Tool(
            name="trace_seal",
            description=(
                "Seal a decision, milestone, or audit gate to the cryptographic "
                "trace vault. Creates a tamper-evident SealRecord."
            ),
            params=[
                ToolParam(
                    "seal_type",
                    "Type of seal",
                    enum=["decision", "milestone", "audit-gate", "stress-test", "epistemic"],
                ),
                ToolParam("description", "What is being sealed"),
                ToolParam("artifacts", "Comma-separated artifact IDs", required=False),
            ],
            handler=lambda seal_type, description, artifacts="": _run_specsmith(
                ["trace", "seal", seal_type, description]
                + (["--artifacts", artifacts] if artifacts else []),
                pd,
            ),
        ),
        Tool(
            name="trace_verify",
            description="Verify cryptographic integrity of the trace vault chain.",
            params=[],
            handler=lambda: _run_specsmith(["trace", "verify"], pd),
        ),
        # ----------------------------------------------------------------
        # Requirements tools
        # ----------------------------------------------------------------
        Tool(
            name="req_list",
            description="List all requirements with status and coverage.",
            params=[],
            handler=lambda: _run_specsmith(["req", "list"], pd),
        ),
        Tool(
            name="req_gaps",
            description="List requirements that have no test coverage.",
            params=[],
            handler=lambda: _run_specsmith(["req", "gaps"], pd),
        ),
        Tool(
            name="req_trace",
            description="Show REQ→TEST traceability matrix.",
            params=[],
            handler=lambda: _run_specsmith(["req", "trace"], pd),
        ),
        # ----------------------------------------------------------------
        # Session tools
        # ----------------------------------------------------------------
        Tool(
            name="session_end",
            description=(
                "Run the session-end checklist: unpushed commits, open TODOs, "
                "dirty files, credit summary, and AEE epistemic status."
            ),
            params=[],
            handler=lambda: _run_specsmith(["session-end"], pd),
        ),
        # ----------------------------------------------------------------
        # Read file tool (essential for context loading)
        # ----------------------------------------------------------------
        Tool(
            name="read_file",
            description=(
                "Read the contents of a file in the project. Use for loading "
                "LEDGER.md, REQUIREMENTS.md, AGENTS.md, or any governance file "
                "to understand current project state."
            ),
            params=[
                ToolParam("path", "File path relative to project root"),
                ToolParam("lines", "Optional line range e.g. '1-100'", required=False),
            ],
            handler=lambda path, lines="": _read_file_handler(pd, path, lines),
        ),
    ]

    return tools


def _read_file_handler(project_dir: str, path: str, lines: str = "") -> str:
    """Read a file from the project directory."""
    root = Path(project_dir).resolve()
    target = (root / path).resolve()

    # Safety: must be within project dir
    try:
        target.relative_to(root)
    except ValueError:
        return f"[ERROR] Path '{path}' is outside the project directory"

    if not target.exists():
        return f"[NOT FOUND] {path}"

    try:
        content = target.read_text(encoding="utf-8")
        if lines:
            parts = lines.split("-")
            start = int(parts[0]) - 1 if parts[0] else 0
            end = int(parts[1]) if len(parts) > 1 and parts[1] else None
            content_lines = content.splitlines()
            content = "\n".join(content_lines[start:end])
        if len(content) > 8000:
            content = content[:8000] + "\n...(truncated at 8000 chars, file has more)"
        return content
    except Exception as e:  # noqa: BLE001
        return f"[ERROR] {e}"


def get_tool_by_name(tools: list[Tool], name: str) -> Tool | None:
    return next((t for t in tools if t.name == name), None)
