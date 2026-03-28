

ANALYSIS_SYSTEM_PROMPT = (
    "You are an expert text analyst. "
    "Return ONLY valid JSON — no markdown fences, no preamble, no extra text."
)

ANALYSIS_SCHEMA = """\
{
  "sentiment": {
    "label": "Positive | Negative | Neutral | Mixed",
    "score": <integer 0-100>,
    "confidence": <integer 0-100>
  },
  "readability": {
    "score": <integer 0-100>,
    "grade_level": "<e.g. University, High School, Elementary>",
    "avg_sentence_length": <integer>,
    "complex_word_ratio": <float 0.0-1.0>
  },
  "themes": [
    {"theme": "<name>", "relevance": <integer 0-100>, "keywords": ["w1","w2","w3"]}
  ],
  "tone": ["<tone1>", "<tone2>"],
  "summary": "<one sentence, max 30 words>",
  "strengths": ["<strength>"],
  "suggestions": ["<suggestion>", "<suggestion>", "<suggestion>"],
  "word_count": <integer>,
  "language": "<detected language name>"
}"""

NARRATIVE_SYSTEM_PROMPT = (
    "You are a sharp editorial analyst. "
    "Be concise, insightful, and direct. "
    "Write in second person ('Your text…'). "
    "Max 120 words."
)


def build_analysis_prompt(text: str) -> str:
    return (
        f"Analyze the following text and return ONLY valid JSON "
        f"matching this schema:\n{ANALYSIS_SCHEMA}\n\n"
        f'Text to analyze:\n"""\n{text}\n"""'
    )


def build_narrative_prompt(analysis_json: str) -> str:
    return (
        f"Given this analysis data:\n{analysis_json}\n\n"
        "Write a brief editorial paragraph about the text quality, "
        "tone, and key takeaways."
    )
