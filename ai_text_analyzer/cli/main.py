"""
ai_text_analyzer.cli.main
~~~~~~~~~~~~~~~~~~~~~~~~~~
Entry point: wires together args → analyzer → renderer.
Handles all user-facing errors and exit codes.
"""

import os
import sys
import time

from ..analyzer import TextAnalyzer, AnalyzerError
from ..models import AnalysisResult
from ..utils.formatting import Color, banner, spinner_frame, clear_line
from ..utils.io import read_file, read_stdin, save_report
from .args import build_parser
from .renderer import render_result, render_narrative


def _resolve_text(args) -> str:
    if args.text:
        return args.text.strip()
    if args.file:
        try:
            return read_file(args.file)
        except FileNotFoundError as exc:
            print(f"{Color.RED}Error: {exc}{Color.RESET}")
            sys.exit(1)
    stdin = read_stdin()
    if stdin:
        return stdin
    print(f"{Color.YELLOW}No input. Use --text, --file, or pipe text via stdin.{Color.RESET}")
    sys.exit(0)


def _show_spinner(message: str) -> None:
    """Block for a single spinner tick to signal activity (non-blocking style)."""
    sys.stdout.write(
        f"\r{Color.CYAN}{spinner_frame(0)}{Color.RESET}  {message}"
    )
    sys.stdout.flush()


def main() -> None:
    parser = build_parser()
    args   = parser.parse_args()

    if not args.no_banner:
        banner()

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print(
            f"{Color.RED}Error: GROQ_API_KEY environment variable is not set.{Color.RESET}\n"
            f"{Color.DIM}  export GROQ_API_KEY='gsk_...' {Color.RESET}"
        )
        sys.exit(1)

    text = _resolve_text(args)

    if len(text) < 10:
        print(f"{Color.YELLOW}Text too short for meaningful analysis (min 10 characters).{Color.RESET}")
        sys.exit(0)

    analyzer = TextAnalyzer(api_key=api_key)

    _show_spinner(f"Analyzing {len(text)} characters with Claude…")
    t0 = time.perf_counter()

    try:
        raw = analyzer.analyze(text)
    except AnalyzerError as exc:
        clear_line()
        print(f"{Color.RED}Analysis failed: {exc}{Color.RESET}")
        sys.exit(1)

    elapsed = time.perf_counter() - t0
    clear_line()
    print(f"  {Color.GREEN}✓{Color.RESET}  Done in {elapsed:.1f}s\n")

    result = AnalysisResult.from_dict(raw)
    render_result(result)

    if args.stream:
        render_narrative(analyzer.stream_narrative(raw))

    if args.save:
        path = save_report(raw, text)
        print(f"  {Color.GREEN}✓{Color.RESET}  Report saved → {Color.CYAN}{path}{Color.RESET}")

    print(f"\n{Color.DIM}{'─' * 54}{Color.RESET}\n")
