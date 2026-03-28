# AI Text Analyzer

Multi-dimensional text analysis via the **Anthropic Claude API**.
Analyzes sentiment, readability, key themes, and tone — and streams
an editorial narrative in real time.

## Project structure

```
ai_text_analyzer/
├── ai_text_analyzer/
│   ├── analyzer/
│   │   ├── core.py        # Anthropic API wrapper (analyze + stream)
│   │   └── prompts.py     # Prompt templates & builders
│   ├── cli/
│   │   ├── args.py        # argparse definition
│   │   ├── main.py        # Entry point — wires everything together
│   │   └── renderer.py    # Terminal rendering (no API knowledge)
│   ├── models/
│   │   └── __init__.py    # Typed dataclasses: AnalysisResult, Theme, …
│   └── utils/
│       ├── formatting.py  # ANSI helpers, progress bars
│       └── io.py          # File reading, stdin, JSON report saving
├── tests/
│   ├── test_formatting.py
│   ├── test_models.py
│   └── test_prompts.py
├── pyproject.toml
└── README.md
```

## Setup

```bash
pip install -e ".[dev]"
export ANTHROPIC_API_KEY="sk-ant-..."
```

## Usage

```bash
# Inline text
text-analyzer --text "Your text here"

# From a file, with streaming narrative
text-analyzer --file essay.txt --stream

# Save JSON report
text-analyzer --file essay.txt --save

# Pipe from stdin
cat article.txt | text-analyzer
```

## Run tests

```bash
pytest
```

## Tech stack

| Layer | Technology |
|---|---|
| AI | Anthropic Claude API (structured JSON + streaming) |
| Language | Python 3.10+ |
| Packaging | `pyproject.toml` / setuptools |
| Testing | pytest |
| CLI | argparse |
| Dependencies | `anthropic` only |
