"""Tests for AnalysisResult.from_dict() deserialization."""

import pytest
from ai_text_analyzer.models import AnalysisResult, SentimentResult, ReadabilityResult, Theme

SAMPLE = {
    "sentiment": {"label": "Positive", "score": 80, "confidence": 90},
    "readability": {
        "score": 65,
        "grade_level": "High School",
        "avg_sentence_length": 14,
        "complex_word_ratio": 0.12,
    },
    "themes": [
        {"theme": "Technology", "relevance": 85, "keywords": ["AI", "model", "data"]},
    ],
    "tone": ["informative", "optimistic"],
    "summary": "A well-structured overview of modern AI capabilities.",
    "strengths": ["Clear structure", "Concise language"],
    "suggestions": ["Add more examples", "Vary sentence length", "Cite sources"],
    "word_count": 320,
    "language": "English",
}


def test_from_dict_returns_correct_types():
    result = AnalysisResult.from_dict(SAMPLE)
    assert isinstance(result, AnalysisResult)
    assert isinstance(result.sentiment, SentimentResult)
    assert isinstance(result.readability, ReadabilityResult)
    assert all(isinstance(t, Theme) for t in result.themes)


def test_sentiment_values():
    result = AnalysisResult.from_dict(SAMPLE)
    assert result.sentiment.label == "Positive"
    assert result.sentiment.score == 80
    assert result.sentiment.confidence == 90


def test_readability_values():
    result = AnalysisResult.from_dict(SAMPLE)
    assert result.readability.score == 65
    assert result.readability.grade_level == "High School"
    assert result.readability.complex_word_ratio == pytest.approx(0.12)


def test_themes_parsed():
    result = AnalysisResult.from_dict(SAMPLE)
    assert len(result.themes) == 1
    assert result.themes[0].theme == "Technology"
    assert "AI" in result.themes[0].keywords


def test_missing_themes_defaults_to_empty():
    data = {**SAMPLE, "themes": []}
    result = AnalysisResult.from_dict(data)
    assert result.themes == []


def test_word_count_and_language():
    result = AnalysisResult.from_dict(SAMPLE)
    assert result.word_count == 320
    assert result.language == "English"
