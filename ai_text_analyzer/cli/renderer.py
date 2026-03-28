"""
ai_text_analyzer.cli.renderer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Renders an AnalysisResult to the terminal.
Knows about both domain models and formatting utilities.
Does not know about argparse or the Anthropic client.
"""

import sys
from typing import Iterator

from ..models import AnalysisResult
from ..utils.formatting import (
    Color,
    section_header,
    progress_bar,
    mini_bar,
)


def _sentiment_color(label: str) -> str:
    low = label.lower()
    if "positive" in low:
        return Color.GREEN
    if "negative" in low:
        return Color.RED
    if "neutral" in low:
        return Color.YELLOW
    return Color.WHITE


def render_result(result: AnalysisResult) -> None:
    """Print the full analysis report."""

    # Overview
    section_header("OVERVIEW")
    print(f"  {Color.DIM}Language:{Color.RESET}   {Color.WHITE}{result.language}{Color.RESET}")
    print(f"  {Color.DIM}Words:{Color.RESET}      {Color.WHITE}{result.word_count}{Color.RESET}")
    print(f"  {Color.DIM}Tone:{Color.RESET}       {Color.WHITE}{', '.join(result.tone)}{Color.RESET}")
    print(f"\n  {Color.DIM}Summary:{Color.RESET}")
    print(f"  {Color.YELLOW}» {result.summary}{Color.RESET}")

    # Sentiment
    section_header("SENTIMENT ANALYSIS")
    sc = _sentiment_color(result.sentiment.label)
    print(f"  {Color.DIM}Result:{Color.RESET}     {sc}{Color.BOLD}{result.sentiment.label}{Color.RESET}")
    print(f"  {Color.DIM}Score:{Color.RESET}      {progress_bar(result.sentiment.score)}")
    print(f"  {Color.DIM}Confidence:{Color.RESET} {Color.WHITE}{result.sentiment.confidence}%{Color.RESET}")

    # Readability
    section_header("READABILITY")
    r = result.readability
    print(f"  {Color.DIM}Score:{Color.RESET}        {progress_bar(r.score)}")
    print(f"  {Color.DIM}Grade level:{Color.RESET}  {Color.WHITE}{r.grade_level}{Color.RESET}")
    print(f"  {Color.DIM}Avg sentence:{Color.RESET} {Color.WHITE}{r.avg_sentence_length} words{Color.RESET}")
    print(f"  {Color.DIM}Complex words:{Color.RESET}{Color.WHITE} {int(r.complex_word_ratio * 100)}%{Color.RESET}")

    # Themes
    section_header("KEY THEMES")
    for theme in result.themes[:4]:
        bar = mini_bar(theme.relevance)
        kw  = ", ".join(theme.keywords)
        print(f"  {Color.CYAN}{theme.theme:<22}{Color.RESET}{Color.DIM}[{bar}] {theme.relevance}%{Color.RESET}")
        print(f"  {Color.DIM}  keywords: {kw}{Color.RESET}")

    # Strengths
    section_header("STRENGTHS")
    for s in result.strengths:
        print(f"  {Color.GREEN}✓{Color.RESET}  {s}")

    # Suggestions
    section_header("IMPROVEMENT SUGGESTIONS")
    for i, sg in enumerate(result.suggestions, 1):
        print(f"  {Color.YELLOW}{i}.{Color.RESET}  {sg}")


def render_narrative(chunks: Iterator[str]) -> None:
    """Stream and print the editorial narrative."""
    section_header("EDITORIAL INSIGHT  (streaming)")
    print(f"\n  {Color.DIM}", end="", flush=True)
    for chunk in chunks:
        sys.stdout.write(chunk)
        sys.stdout.flush()
    print(f"{Color.RESET}\n")
