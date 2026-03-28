"""
ai_text_analyzer.utils.io
~~~~~~~~~~~~~~~~~~~~~~~~~~
File reading, stdin detection, and JSON report persistence.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


def read_file(path: str) -> str:
    """Read a text file and return its contents. Raises FileNotFoundError if missing."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return p.read_text(encoding="utf-8").strip()


def read_stdin() -> Optional[str]:
    """Return stdin contents if data is piped, else None."""
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    return None


def save_report(analysis_dict: dict, text: str, output_dir: Path = Path(".")) -> Path:
    """
    Persist a JSON analysis report to disk.
    Returns the path of the created file.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = output_dir / f"analysis_{timestamp}.json"

    report = {
        "generated_at": datetime.now().isoformat(),
        "input_preview": text[:200] + ("…" if len(text) > 200 else ""),
        "analysis": analysis_dict,
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    return path
