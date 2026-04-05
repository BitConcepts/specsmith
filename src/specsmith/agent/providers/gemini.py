# SPDX-License-Identifier: MIT
# Copyright (c) 2026 BitConcepts, LLC. All rights reserved.
"""Google Gemini provider for the specsmith agentic client.

Requires: pip install specsmith[gemini]
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from specsmith.agent.core import (
    CompletionResponse,
    Message,
    Role,
    StreamToken,
    Tool,
)


class GeminiProvider:
    """Google Gemini provider. Supports gemini-2.5-pro, gemini-2.5-flash."""

    provider_name = "gemini"

    def __init__(self, model: str = "gemini-2.5-pro", api_key: str = "") -> None:
        self.model = model
        self._api_key = api_key
        self._genai: Any = None
        self._ensure_client()

    def _ensure_client(self) -> None:
        try:
            import google.generativeai as genai

            genai.configure(api_key=self._api_key)
            self._genai = genai
        except ImportError as e:
            from specsmith.agent.core import ProviderNotAvailable

            raise ProviderNotAvailable("gemini", "gemini") from e

    def is_available(self) -> bool:
        try:
            import google.generativeai  # noqa: F401

            return bool(self._api_key)
        except ImportError:
            return False

    def complete(
        self,
        messages: list[Message],
        tools: list[Tool] | None = None,
        max_tokens: int = 4096,
    ) -> CompletionResponse:
        gemini_model = self._genai.GenerativeModel(
            model_name=self.model,
            generation_config={"max_output_tokens": max_tokens},
        )

        # Build conversation history
        history: list[dict[str, Any]] = []
        system_text = ""
        for m in messages:
            if m.role == Role.SYSTEM:
                system_text = m.content
            elif m.role == Role.USER:
                history.append({"role": "user", "parts": [m.content]})
            elif m.role == Role.ASSISTANT:
                history.append({"role": "model", "parts": [m.content]})

        if system_text and history and history[0]["role"] == "user":
            history[0]["parts"] = [f"[SYSTEM]\n{system_text}\n\n{history[0]['parts'][0]}"]

        if not history:
            return CompletionResponse(content="", model=self.model)

        last_msg = history.pop()
        chat = gemini_model.start_chat(history=history)
        response = chat.send_message(last_msg["parts"][0])
        content = response.text or ""

        return CompletionResponse(
            content=content,
            model=self.model,
            input_tokens=0,  # Gemini doesn't always expose token counts
            output_tokens=0,
            stop_reason="stop",
        )

    def stream(
        self,
        messages: list[Message],
        tools: list[Tool] | None = None,
        max_tokens: int = 4096,
    ) -> Iterator[StreamToken]:
        gemini_model = self._genai.GenerativeModel(
            model_name=self.model,
            generation_config={"max_output_tokens": max_tokens},
        )
        history: list[dict[str, Any]] = []
        system_text = ""
        for m in messages:
            if m.role == Role.SYSTEM:
                system_text = m.content
            elif m.role == Role.USER:
                history.append({"role": "user", "parts": [m.content]})
            elif m.role == Role.ASSISTANT:
                history.append({"role": "model", "parts": [m.content]})

        if system_text and history and history[0]["role"] == "user":
            history[0]["parts"] = [f"[SYSTEM]\n{system_text}\n\n{history[0]['parts'][0]}"]

        if not history:
            yield StreamToken(text="", is_final=True)
            return

        last_msg = history.pop()
        chat = gemini_model.start_chat(history=history)
        for chunk in chat.send_message(last_msg["parts"][0], stream=True):
            if chunk.text:
                yield StreamToken(text=chunk.text)
        yield StreamToken(text="", is_final=True)
