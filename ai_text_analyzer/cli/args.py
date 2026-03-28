

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="text-analyzer",
        description="AI Text Analyzer — multi-dimensional text analysis via Claude.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  text-analyzer --text "Your text here"
  text-analyzer --file essay.txt --save --stream
  cat article.txt | text-analyzer
        """,
    )

    source = parser.add_mutually_exclusive_group()
    source.add_argument("--text", metavar="TEXT",  help="Inline text to analyze")
    source.add_argument("--file", metavar="PATH",  help="Path to a .txt file")

    parser.add_argument(
        "--save",
        action="store_true",
        help="Save a JSON report to the current directory",
    )
    parser.add_argument(
        "--stream",
        action="store_true",
        help="Stream an editorial narrative after the main analysis",
    )
    parser.add_argument(
        "--no-banner",
        action="store_true",
        help="Suppress the ASCII banner",
    )
    return parser
