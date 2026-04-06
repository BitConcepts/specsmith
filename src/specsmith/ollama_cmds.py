# SPDX-License-Identifier: MIT
# Copyright (c) 2026 BitConcepts, LLC. All rights reserved.
"""Ollama model management helpers for specsmith.

Provides GPU detection, a curated model catalog, and utilities for
listing, recommending, and pulling local Ollama models.
"""

from __future__ import annotations

import json
import platform
import shutil
import subprocess
import urllib.request
from typing import Any

OLLAMA_API = "http://localhost:11434"

# ---------------------------------------------------------------------------
# Curated model catalog
# ---------------------------------------------------------------------------
# Each entry: id, name, vram_gb (min VRAM for comfortable inference),
# size_gb (download size), best_for (task tags), notes.

MODEL_CATALOG: list[dict[str, Any]] = [
    {
        "id": "llama3.2:latest",
        "name": "Llama 3.2 3B",
        "vram_gb": 2.0,
        "size_gb": 2.0,
        "ctx_k": 128,
        "best_for": ["chat", "quick tasks", "summaries"],
        "notes": "Tiny, very fast. Good for quick Q&A.",
        "tier": "Tiny",
    },
    {
        "id": "mistral:latest",
        "name": "Mistral 7B",
        "vram_gb": 4.5,
        "size_gb": 4.1,
        "ctx_k": 32,
        "best_for": ["chat", "writing", "summaries"],
        "notes": "Fast, good general-purpose model.",
        "tier": "Balanced",
    },
    {
        "id": "qwen2.5:7b",
        "name": "Qwen 2.5 7B",
        "vram_gb": 5.0,
        "size_gb": 4.7,
        "ctx_k": 32,
        "best_for": ["coding", "analysis", "requirements"],
        "notes": "Best 7B for technical and analytical work.",
        "tier": "Balanced",
    },
    {
        "id": "qwen2.5-coder:7b-instruct",
        "name": "Qwen 2.5 Coder 7B",
        "vram_gb": 4.8,
        "size_gb": 4.7,
        "ctx_k": 32,
        "best_for": ["code generation", "code review", "debugging"],
        "notes": "Specialized coding model. Top 7B coder.",
        "tier": "Balanced",
    },
    {
        "id": "gemma3:12b",
        "name": "Gemma 3 12B (Google)",
        "vram_gb": 8.0,
        "size_gb": 7.8,
        "ctx_k": 128,
        "best_for": ["general", "chat", "writing", "analysis"],
        "notes": "Google's open model. Strong 128K context.",
        "tier": "Capable",
    },
    {
        "id": "phi4:latest",
        "name": "Phi-4 14B (Microsoft)",
        "vram_gb": 9.0,
        "size_gb": 8.5,
        "ctx_k": 16,
        "best_for": ["reasoning", "math", "analysis", "requirements"],
        "notes": "Outstanding reasoning for its size.",
        "tier": "Capable",
    },
    {
        "id": "qwen2.5:14b",
        "name": "Qwen 2.5 14B",
        "vram_gb": 9.0,
        "size_gb": 8.9,
        "ctx_k": 32,
        "best_for": ["coding", "complex reasoning", "requirements engineering"],
        "notes": "Excellent for AEE/specsmith workflows.",
        "tier": "Capable",
    },
    {
        "id": "deepseek-coder-v2:latest",
        "name": "DeepSeek Coder v2 16B",
        "vram_gb": 11.0,
        "size_gb": 9.1,
        "ctx_k": 128,
        "best_for": ["code generation", "code review", "debugging"],
        "notes": "Top local coding model. 128K context.",
        "tier": "Capable",
    },
    {
        "id": "qwen2.5:32b",
        "name": "Qwen 2.5 32B",
        "vram_gb": 20.0,
        "size_gb": 19.0,
        "ctx_k": 32,
        "best_for": ["complex reasoning", "requirements engineering", "architecture"],
        "notes": "Best local quality for high-VRAM systems.",
        "tier": "Powerful",
    },
]

# Task → relevant model tags (for suggest command)
TASK_TAGS: dict[str, list[str]] = {
    "coding":           ["code generation", "code review", "debugging", "coding"],
    "requirements":     ["requirements", "requirements engineering", "analysis"],
    "architecture":     ["complex reasoning", "architecture", "requirements engineering"],
    "chat":             ["chat", "summaries", "writing", "general"],
    "analysis":         ["analysis", "reasoning", "requirements"],
    "reasoning":        ["complex reasoning", "reasoning", "math"],
}


# ---------------------------------------------------------------------------
# Ollama API helpers
# ---------------------------------------------------------------------------

def is_running() -> bool:
    """Return True if the Ollama API is reachable."""
    try:
        urllib.request.urlopen(f"{OLLAMA_API}/api/version", timeout=3)  # noqa: S310
        return True
    except Exception:  # noqa: BLE001
        return False


def get_installed_models() -> list[dict[str, Any]]:
    """Return list of locally installed Ollama models from /api/tags."""
    try:
        with urllib.request.urlopen(f"{OLLAMA_API}/api/tags", timeout=5) as resp:  # noqa: S310
            data: dict[str, Any] = json.loads(resp.read())
        return data.get("models", [])
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"Cannot reach Ollama at {OLLAMA_API} — is it running?") from exc


def get_installed_ids() -> list[str]:
    """Return just the model name strings of installed models."""
    return [m.get("name", "") for m in get_installed_models()]


# ---------------------------------------------------------------------------
# GPU detection
# ---------------------------------------------------------------------------

def detect_gpu() -> list[dict[str, Any]]:
    """Detect GPU(s) and VRAM. Returns list of {name, vram_gb} dicts.

    Detection order:
      1. NVIDIA nvidia-smi (most accurate)
      2. Windows WMI via PowerShell (covers AMD / Intel / any GPU)
      3. Returns [] if no GPU found
    """
    gpus: list[dict[str, Any]] = []

    # ── NVIDIA ─────────────────────────────────────────────────────────────
    if shutil.which("nvidia-smi"):
        try:
            result = subprocess.run(
                [
                    "nvidia-smi",
                    "--query-gpu=name,memory.total",
                    "--format=csv,noheader,nounits",
                ],
                capture_output=True,
                text=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    parts = [p.strip() for p in line.split(",")]
                    if len(parts) == 2 and parts[1].isdigit():
                        gpus.append(
                            {"name": parts[0], "vram_gb": round(int(parts[1]) / 1024, 1)}
                        )
                if gpus:
                    return gpus
        except Exception:  # noqa: BLE001
            pass

    # ── Windows WMI (AMD, Intel, any WDDM GPU) ─────────────────────────────
    if platform.system() == "Windows":
        try:
            result = subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-Command",
                    "Get-WmiObject Win32_VideoController | "
                    "ForEach-Object { \"$($_.Name),$($_.AdapterRAM)\" }",
                ],
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    line = line.strip()
                    if "," in line:
                        parts = line.rsplit(",", 1)
                        name = parts[0].strip()
                        try:
                            vram_bytes = int(parts[1].strip())
                            vram_gb = vram_bytes / (1024**3)
                            if vram_gb > 0.5:
                                gpus.append({"name": name, "vram_gb": round(vram_gb, 1)})
                        except (ValueError, IndexError):
                            pass
                if gpus:
                    return gpus
        except Exception:  # noqa: BLE001
            pass

    return []


def gpu_tier(vram_gb: float) -> str:
    """Return a human-readable GPU tier label."""
    if vram_gb >= 20:
        return "Powerful (20GB+)"
    if vram_gb >= 10:
        return "Capable (10-20GB)"
    if vram_gb >= 5:
        return "Balanced (5-10GB)"
    if vram_gb >= 2:
        return "Tiny (2-5GB)"
    return "CPU only"


# ---------------------------------------------------------------------------
# Recommendations
# ---------------------------------------------------------------------------

def recommend_models(vram_gb: float) -> list[dict[str, Any]]:
    """Return catalog models that fit within the VRAM budget (90% usable)."""
    budget = vram_gb * 0.90
    return [m for m in MODEL_CATALOG if m["vram_gb"] <= budget]


def suggest_for_task(task_key: str, vram_gb: float = 999) -> list[dict[str, Any]]:
    """Return models sorted by relevance for a given task, within VRAM budget."""
    tags = TASK_TAGS.get(task_key.lower(), [])
    budget = vram_gb * 0.90

    def _score(model: dict[str, Any]) -> int:
        if model["vram_gb"] > budget:
            return -1
        return sum(1 for t in tags if t in model["best_for"])

    scored = [(m, _score(m)) for m in MODEL_CATALOG if _score(m) >= 0]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [m for m, _ in scored]
