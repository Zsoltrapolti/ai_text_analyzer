"""
ai_text_analyzer.utils.formatting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ANSI terminal helpers and display utilities.
Nothing in here knows about the domain — just strings and colors.
"""

import sys


# ── ANSI escape codes ──────────────────────────────────────────────────────────

class Color:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    CYAN    = "\033[96m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    RED     = "\033[91m"
    MAGENTA = "\033[95m"
    WHITE   = "\033[97m"
    BLUE    = "\033[94m"


# ── Generic components ─────────────────────────────────────────────────────────

def section_header(title: str, width: int = 54) -> None:
    print(f"\n{Color.BOLD}{Color.WHITE}{'─' * width}{Color.RESET}")
    print(f"{Color.BOLD}{Color.CYAN}  {title}{Color.RESET}")
    print(f"{Color.WHITE}{'─' * width}{Color.RESET}")


def progress_bar(score: int, max_score: int = 100, width: int = 20) -> str:
    filled = int((score / max_score) * width)
    bar    = "█" * filled + "░" * (width - filled)
    color  = Color.GREEN if score >= 70 else (Color.YELLOW if score >= 40 else Color.RED)
    return f"{color}[{bar}] {score}/{max_score}{Color.RESET}"


def mini_bar(score: int, width: int = 10) -> str:
    filled = int((score / 100) * width)
    return "█" * filled + "░" * (width - filled)


def banner() -> None:
    print(f"""
{Color.CYAN}{Color.BOLD}╔══════════════════════════════════════════════════════╗
║          AI TEXT ANALYZER  ·  powered by Claude      ║
╚══════════════════════════════════════════════════════╝{Color.RESET}
""")


def spinner_frame(frame_index: int) -> str:
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    return frames[frame_index % len(frames)]


def clear_line() -> None:
    sys.stdout.write("\r\033[K")
    sys.stdout.flush()
