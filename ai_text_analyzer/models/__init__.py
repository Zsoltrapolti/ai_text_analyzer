"""
ai_text_analyzer.models
~~~~~~~~~~~~~~~~~~~~~~~
Typed data models for analysis results.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class SentimentResult:
    label: str          # "Positive" | "Negative" | "Neutral" | "Mixed"
    score: int          # 0–100 (0 = very negative, 100 = very positive)
    confidence: int     # 0–100


@dataclass
class ReadabilityResult:
    score: int
    grade_level: str
    avg_sentence_length: int
    complex_word_ratio: float


@dataclass
class Theme:
    theme: str
    relevance: int      # 0–100
    keywords: List[str] = field(default_factory=list)


@dataclass
class AnalysisResult:
    sentiment: SentimentResult
    readability: ReadabilityResult
    themes: List[Theme]
    tone: List[str]
    summary: str
    strengths: List[str]
    suggestions: List[str]
    word_count: int
    language: str

    @classmethod
    def from_dict(cls, data: dict) -> "AnalysisResult":
        return cls(
            sentiment=SentimentResult(**data["sentiment"]),
            readability=ReadabilityResult(**data["readability"]),
            themes=[Theme(**t) for t in data.get("themes", [])],
            tone=data.get("tone", []),
            summary=data.get("summary", ""),
            strengths=data.get("strengths", []),
            suggestions=data.get("suggestions", []),
            word_count=data.get("word_count", 0),
            language=data.get("language", "Unknown"),
        )
