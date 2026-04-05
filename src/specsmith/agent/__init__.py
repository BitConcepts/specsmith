# SPDX-License-Identifier: MIT
# Copyright (c) 2026 BitConcepts, LLC. All rights reserved.
"""specsmith agentic client — AEE-integrated, multi-provider Python agent.

    pip install specsmith[anthropic]    # for Claude
    pip install specsmith[openai]       # for GPT / O-series / any OpenAI-compat
    pip install specsmith[gemini]       # for Gemini
    # Ollama: no extra needed, uses stdlib urllib

    specsmith run                       # start interactive REPL
    specsmith run --task "run audit"    # single-shot task
    specsmith run --provider ollama --model qwen2.5:14b  # local LLM

Providers auto-detected from environment:
    ANTHROPIC_API_KEY → Anthropic (Claude)
    OPENAI_API_KEY    → OpenAI (GPT/O-series)
    GOOGLE_API_KEY    → Google (Gemini)
    Ollama running    → local models (zero config)
    SPECSMITH_PROVIDER=<name> → explicit override
"""

from __future__ import annotations

from specsmith.agent.core import (
    CompletionResponse,
    Message,
    ModelTier,
    Role,
    Tool,
    ToolParam,
    ToolResult,
)
from specsmith.agent.runner import AgentRunner

__all__ = [
    "AgentRunner",
    "Message",
    "Role",
    "Tool",
    "ToolParam",
    "ToolResult",
    "CompletionResponse",
    "ModelTier",
]
