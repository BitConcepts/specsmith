# SPDX-License-Identifier: MIT
# Copyright (c) 2026 BitConcepts, LLC. All rights reserved.
"""Hook system — trigger-based automations on agent lifecycle events.

Inspired by ECC's hook system (PreToolUse, PostToolUse, Stop, etc.).
Hooks run automatically at defined trigger points with zero user interaction.

Built-in hooks:
  - pre_tool: Epistemic boundary check (H13 enforcement)
  - post_tool: Ledger update suggestion, credit recording
  - session_start: Sync + update-check reminder
  - session_end: Seal trace vault, summarize session
  - context_budget: Warn when estimated token usage is high
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class HookTrigger(str, Enum):
    PRE_TOOL = "pre_tool"
    POST_TOOL = "post_tool"
    SESSION_START = "session_start"
    SESSION_END = "session_end"
    CONTEXT_BUDGET = "context_budget"


@dataclass
class HookContext:
    """Context passed to hook handlers."""

    trigger: HookTrigger
    tool_name: str = ""
    tool_input: dict[str, Any] = field(default_factory=dict)
    tool_output: str = ""
    project_dir: str = "."
    session_tokens: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class HookResult:
    """Result from a hook handler."""

    action: str = "continue"  # continue | block | warn
    message: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


HookHandler = Callable[[HookContext], HookResult]


@dataclass
class Hook:
    """A registered hook."""

    trigger: HookTrigger
    handler: HookHandler
    name: str = ""
    description: str = ""
    enabled: bool = True


class HookRegistry:
    """Registry of active hooks.

    Usage::

        registry = HookRegistry()
        registry.register(Hook(
            trigger=HookTrigger.PRE_TOOL,
            handler=my_handler,
            name="epistemic-check",
        ))
        result = registry.fire(HookTrigger.PRE_TOOL, ctx)
    """

    def __init__(self) -> None:
        self._hooks: list[Hook] = []
        self._install_defaults()

    def register(self, hook: Hook) -> None:
        self._hooks.append(hook)

    def fire(self, trigger: HookTrigger, ctx: HookContext) -> list[HookResult]:
        results: list[HookResult] = []
        for hook in self._hooks:
            if hook.trigger == trigger and hook.enabled:
                try:
                    result = hook.handler(ctx)
                    results.append(result)
                except Exception as e:  # noqa: BLE001
                    results.append(HookResult(action="continue", message=f"[hook error] {e}"))
        return results

    def has_blocking_result(self, results: list[HookResult]) -> tuple[bool, str]:
        """Check if any hook result blocks execution."""
        for r in results:
            if r.action == "block":
                return True, r.message
        return False, ""

    def _install_defaults(self) -> None:
        """Install the built-in default hooks."""
        self.register(
            Hook(
                trigger=HookTrigger.PRE_TOOL,
                handler=_epistemic_boundary_check,
                name="epistemic-boundary-check",
                description=(
                    "H13 enforcement: warn when a tool call may affect P1 belief artifacts "
                    "without an explicit epistemic boundary in the proposal."
                ),
            )
        )
        self.register(
            Hook(
                trigger=HookTrigger.POST_TOOL,
                handler=_post_tool_ledger_hint,
                name="ledger-hint",
                description=(
                    "After significant tool calls (commit, push, epistemic-audit), "
                    "remind the agent to add a ledger entry."
                ),
            )
        )
        self.register(
            Hook(
                trigger=HookTrigger.CONTEXT_BUDGET,
                handler=_context_budget_warning,
                name="context-budget-warning",
                description=(
                    "Warn when estimated session token usage exceeds 80% of the "
                    "context window. Recommend using /save-session."
                ),
            )
        )
        self.register(
            Hook(
                trigger=HookTrigger.SESSION_START,
                handler=_session_start_reminder,
                name="session-start",
                description="Remind to sync and check specsmith updates at session start.",
            )
        )


# ---------------------------------------------------------------------------
# Default hook handlers
# ---------------------------------------------------------------------------


def _epistemic_boundary_check(ctx: HookContext) -> HookResult:
    """H13: warn if epistemic boundary is not declared for tool calls that affect beliefs."""
    aee_tools = {"epistemic_audit", "stress_test", "belief_graph", "trace_seal"}
    if ctx.tool_name not in aee_tools:
        return HookResult(action="continue")

    # Check if there are P1 requirements with low confidence
    req_file = __import__("pathlib").Path(ctx.project_dir) / "docs" / "REQUIREMENTS.md"
    if req_file.exists():
        content = req_file.read_text(encoding="utf-8")
        import re

        p1_count = len(re.findall(r"\*\*Priority\*\*:\s*P1", content, re.IGNORECASE))
        if p1_count > 0:
            return HookResult(
                action="warn",
                message=(
                    f"[H13] This project has {p1_count} P1 requirement(s). "
                    "Ensure epistemic boundaries are declared for critical beliefs "
                    "before running epistemic tools."
                ),
            )
    return HookResult(action="continue")


def _post_tool_ledger_hint(ctx: HookContext) -> HookResult:
    """Remind agent to add ledger entry after significant operations."""
    significant_tools = {
        "commit",
        "push",
        "epistemic_audit",
        "stress_test",
        "trace_seal",
        "create_pr",
        "create_branch",
    }
    if (
        ctx.tool_name in significant_tools
        and "[exit" not in ctx.tool_output
        and "[ERROR]" not in ctx.tool_output
    ):
        return HookResult(
            action="continue",
            message=f"[ledger-hint] Consider adding a LEDGER.md entry for: {ctx.tool_name}",
        )
    return HookResult(action="continue")


def _context_budget_warning(ctx: HookContext) -> HookResult:
    """Warn when context window is getting full."""
    # Rough estimate: 200k token context, warn at 80%
    budget_limit = 160_000
    if ctx.session_tokens > budget_limit:
        return HookResult(
            action="warn",
            message=(
                f"[context-budget] Session tokens ~{ctx.session_tokens:,} "
                f"(>{budget_limit // 1000}k). Consider /save-session and starting fresh. "
                "Load only the last 300 lines of LEDGER.md next session."
            ),
        )
    return HookResult(action="continue")


def _session_start_reminder(ctx: HookContext) -> HookResult:
    """Remind agent to run sync and update-check at session start."""
    return HookResult(
        action="continue",
        message=(
            "[session-start] Recommended start protocol:\n"
            "  1. Run sync to pull latest\n"
            "  2. Read AGENTS.md + last 300 lines of LEDGER.md\n"
            "  3. Check for specsmith updates\n"
            "  4. Load belief artifacts and check epistemic status"
        ),
    )
