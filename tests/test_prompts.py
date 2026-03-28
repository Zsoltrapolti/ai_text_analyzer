
from ai_text_analyzer.analyzer.prompts import build_analysis_prompt, build_narrative_prompt


def test_analysis_prompt_contains_text():
    prompt = build_analysis_prompt("Hello world")
    assert "Hello world" in prompt


def test_analysis_prompt_contains_schema_keys():
    prompt = build_analysis_prompt("test")
    for key in ("sentiment", "readability", "themes", "suggestions"):
        assert key in prompt


def test_narrative_prompt_contains_analysis():
    prompt = build_narrative_prompt('{"sentiment": "positive"}')
    assert "positive" in prompt
