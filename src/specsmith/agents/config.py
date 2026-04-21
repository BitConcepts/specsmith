# SPDX-License-Identifier: MIT
# Copyright (c) 2026 BitConcepts, LLC. All rights reserved.
"""Agent configuration — loaded from scaffold.yml ``agents:`` key."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class AgentConfig:
    """Configuration for the AG2 agent shell."""

    primary_model: str = "qwen2.5:14b"
    utility_model: str = ""  # empty = same as primary_model
    ollama_base_url: str = "http://localhost:11434"
    max_iterations: int = 10
    stream: bool = False
    num_ctx: int = 4096
    tools_enabled: list[str] = field(
        default_factory=lambda: ["filesystem", "shell", "git", "tests", "docs"]
    )

    @property
    def effective_utility_model(self) -> str:
        """Utility model, defaulting to primary if not set."""
        return self.utility_model or self.primary_model

    @property
    def effective_max_iterations(self) -> int:
        """0 means unlimited (use 999 as practical ceiling)."""
        return self.max_iterations if self.max_iterations > 0 else 999

    def llm_config_dict(self, model: str | None = None) -> dict[str, Any]:
        """Return an AG2-compatible LLM config dict for Ollama."""
        return {
            "model": model or self.primary_model,
            "api_type": "ollama",
            "client_host": self.ollama_base_url,
            "stream": self.stream,
            "num_ctx": self.num_ctx,
            "native_tool_calls": True,
            "hide_tools": "if_any_run",
        }


def load_agent_config(project_dir: str | Path) -> AgentConfig:
    """Load agent config from scaffold.yml ``agents:`` section.

    Falls back to defaults if scaffold.yml doesn't exist or has no agents key.
    """
    scaffold_path = Path(project_dir) / "scaffold.yml"
    if not scaffold_path.exists():
        return AgentConfig()

    try:
        import yaml

        with open(scaffold_path, encoding="utf-8") as f:
            raw = yaml.safe_load(f) or {}
        agents_raw = raw.get("agents", {}) or {}
        return AgentConfig(
            primary_model=agents_raw.get("primary_model", AgentConfig.primary_model),
            utility_model=agents_raw.get("utility_model", AgentConfig.utility_model),
            ollama_base_url=agents_raw.get("ollama_base_url", AgentConfig.ollama_base_url),
            max_iterations=agents_raw.get("max_iterations", AgentConfig.max_iterations),
            stream=agents_raw.get("stream", AgentConfig.stream),
            num_ctx=agents_raw.get("num_ctx", AgentConfig.num_ctx),
            tools_enabled=agents_raw.get("tools_enabled", AgentConfig().tools_enabled),
        )
    except Exception:  # noqa: BLE001
        return AgentConfig()
