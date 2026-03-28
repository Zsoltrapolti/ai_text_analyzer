"""
ai_text_analyzer.analyzer.core
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Thin wrapper around the Anthropic API.
Responsible for making API calls and returning raw dicts.
All business logic lives in the caller.
"""

import json
from typing import Iterator

from groq import Groq, APIError

from .prompts import (
    ANALYSIS_SYSTEM_PROMPT,
    NARRATIVE_SYSTEM_PROMPT,
    build_analysis_prompt,
    build_narrative_prompt,
)

MODEL = "llama-3.3-70b-versatile"
MAX_TOKENS_ANALYSIS = 1024
MAX_TOKENS_NARRATIVE = 220


class AnalyzerError(Exception):
    """Raised when the Groq API call or JSON parsing fails."""


class TextAnalyzer:
    def __init__(self, api_key: str) -> None:
        self._client = Groq(api_key=api_key)

    def analyze(self, text: str) -> dict:
        """
        Send text to Claude and return the raw analysis dict.
        Raises AnalyzerError on API or parse failure.
        """
        try:
            message = self._client.chat.completions.create(
                model=MODEL,
                max_tokens=MAX_TOKENS_ANALYSIS,
                messages=[
                    {"role": "system", "content": ANALYSIS_SYSTEM_PROMPT},
                    {"role": "user", "content": build_analysis_prompt(text)},
                ],
            )
        except APIError as exc:
            raise AnalyzerError(f"Groq API error: {exc}") from exc

        raw = message.choices[0].message.content.strip()

        # Strip accidental markdown fences
        if raw.startswith("```"):
            parts = raw.split("```")
            raw = parts[1].lstrip("json").strip() if len(parts) > 1 else raw

        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            raise AnalyzerError(f"Failed to parse Claude response as JSON: {exc}") from exc

    def stream_narrative(self, analysis_dict: dict) -> Iterator[str]:
        """
        Yield text chunks for the streaming narrative summary.
        Caller is responsible for printing / accumulating.
        """
        analysis_json = json.dumps(analysis_dict, indent=2)
        stream = self._client.chat.completions.create(
            model=MODEL,
            max_tokens=MAX_TOKENS_NARRATIVE,
            stream=True,
            messages=[
                {"role": "system", "content": NARRATIVE_SYSTEM_PROMPT},
                {"role": "user", "content": build_narrative_prompt(analysis_json)},
            ],
        )
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta
