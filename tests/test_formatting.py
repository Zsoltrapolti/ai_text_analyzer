"""Tests for terminal formatting helpers."""

from ai_text_analyzer.utils.formatting import progress_bar, mini_bar


def test_progress_bar_contains_score():
    bar = progress_bar(75)
    assert "75" in bar


def test_progress_bar_green_for_high_score():
    bar = progress_bar(80)
    assert "\033[92m" in bar  # Color.GREEN


def test_progress_bar_red_for_low_score():
    bar = progress_bar(20)
    assert "\033[91m" in bar  # Color.RED


def test_progress_bar_yellow_for_mid_score():
    bar = progress_bar(50)
    assert "\033[93m" in bar  # Color.YELLOW


def test_mini_bar_length():
    bar = mini_bar(50)
    assert len(bar) == 10  # default width


def test_mini_bar_full():
    bar = mini_bar(100)
    assert bar == "█" * 10


def test_mini_bar_empty():
    bar = mini_bar(0)
    assert bar == "░" * 10
