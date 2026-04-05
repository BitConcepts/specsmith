# SPDX-License-Identifier: MIT
# Copyright (c) 2026 BitConcepts, LLC. All rights reserved.
"""Core types and BaseProvider protocol for the specsmith agentic client.

All LLM providers are optional. Import this module freely — it has no
external dependencies beyond Python's stdlib.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Protocol, runtime_checkable


class Role(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


@dataclass
class Message:
    role: Role
    content: str
    tool_call_id: str = ""
    tool_calls: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"role": self.role.value, "content": self.content}
        if self.tool_call_id:
            d["tool_call_id"] = self.tool_call_id
        if self.tool_calls:
            d["tool_calls"] = self.tool_calls
        return d


@dataclass
class ToolParam:
    name: str
    description: str
    type: str = "string"
    required: bool = True
    enum: list[str] | None = None


@dataclass
class Tool:
    """A callable tool that can be invoked by the LLM.

    Tools are the primary way the agentic client interacts with the system.
    specsmith commands are registered as tools so the agent can call them
    directly during a session.
    """

    name: str
    description: str
    params: list[ToolParam] = field(default_factory=list)
    handler: Callable[..., str] | None = field(default=None, repr=False)
    # AEE metadata
    epistemic_claims: list[str] = field(default_factory=list)  # what this tool asserts
    uncertainty_bounds: str = ""  # what this tool cannot detect

    def to_anthropic_schema(self) -> dict[str, Any]:
        props: dict[str, Any] = {}
        required: list[str] = []
        for p in self.params:
            prop: dict[str, Any] = {"type": p.type, "description": p.description}
            if p.enum:
                prop["enum"] = p.enum
            props[p.name] = prop
            if p.required:
                required.append(p.name)
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": {
                "type": "object",
                "properties": props,
                "required": required,
            },
        }

    def to_openai_schema(self) -> dict[str, Any]:
        props: dict[str, Any] = {}
        required: list[str] = []
        for p in self.params:
            prop: dict[str, Any] = {"type": p.type, "description": p.description}
            if p.enum:
                prop["enum"] = p.enum
            props[p.name] = prop
            if p.required:
                required.append(p.name)
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": props,
                    "required": required,
                },
            },
        }


@dataclass
class ToolResult:
    tool_name: str
    tool_call_id: str
    content: str
    error: bool = False
    elapsed_ms: float = 0.0


@dataclass
class CompletionResponse:
    content: str
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    stop_reason: str = "end_turn"

    @property
    def has_tool_calls(self) -> bool:
        return len(self.tool_calls) > 0

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens

    @property
    def estimated_cost_usd(self) -> float:
        """Very rough estimate — override with actual pricing data."""
        return (self.input_tokens * 3.0 + self.output_tokens * 15.0) / 1_000_000


@dataclass
class StreamToken:
    text: str
    is_final: bool = False
    tool_call: dict[str, Any] | None = None


class ModelTier(str, Enum):
    """Model capability tier for routing decisions (ECC-inspired)."""

    FAST = "fast"  # cheap/fast (haiku, gpt-4o-mini, gemini-flash, llama-3.1-8b)
    BALANCED = "balanced"  # best value (sonnet, gpt-4o, gemini-pro)
    POWERFUL = "powerful"  # max capability (opus, o3, gemini-ultra)


# Default model names per provider/tier
MODEL_DEFAULTS: dict[str, dict[ModelTier, str]] = {
    "anthropic": {
        ModelTier.FAST: "claude-haiku-4-5",
        ModelTier.BALANCED: "claude-sonnet-4-5",
        ModelTier.POWERFUL: "claude-opus-4-5",
    },
    "openai": {
        ModelTier.FAST: "gpt-4o-mini",
        ModelTier.BALANCED: "gpt-4o",
        ModelTier.POWERFUL: "o3",
    },
    "gemini": {
        ModelTier.FAST: "gemini-2.5-flash",
        ModelTier.BALANCED: "gemini-2.5-pro",
        ModelTier.POWERFUL: "gemini-2.5-ultra",
    },
    "ollama": {
        ModelTier.FAST: "llama3.2:3b",
        ModelTier.BALANCED: "qwen2.5:14b",
        ModelTier.POWERFUL: "qwen2.5:72b",
    },
}


@runtime_checkable
class BaseProvider(Protocol):
    """Protocol that all LLM providers must implement."""

    provider_name: str
    model: str

    def complete(
        self,
        messages: list[Message],
        tools: list[Tool] | None = None,
        max_tokens: int = 4096,
    ) -> CompletionResponse: ...

    def stream(
        self,
        messages: list[Message],
        tools: list[Tool] | None = None,
        max_tokens: int = 4096,
    ) -> Iterator[StreamToken]: ...

    def is_available(self) -> bool: ...


class ProviderNotAvailable(RuntimeError):
    """Raised when a provider SDK is not installed."""

    def __init__(self, provider: str, extra: str) -> None:
        super().__init__(
            f"Provider '{provider}' is not available. "
            f"Install it with: pip install specsmith[{extra}]"
        )
