"""
server.py
~~~~~~~~~
Lightweight Flask API that wraps the TextAnalyzer for the web frontend.
Run with: python server.py
"""

import os
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from ai_text_analyzer.analyzer import TextAnalyzer, AnalyzerError

app = Flask(__name__, static_folder="frontend", static_url_path="")
CORS(app)

api_key = os.environ.get("GROQ_API_KEY", "")
analyzer = TextAnalyzer(api_key=api_key) if api_key else None


@app.route("/")
def index():
    return send_from_directory("frontend", "index.html")


@app.route("/api/analyze", methods=["POST"])
def analyze():
    if not analyzer:
        return jsonify({"error": "GROQ_API_KEY is not set on the server."}), 500

    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()

    if len(text) < 10:
        return jsonify({"error": "Text too short (minimum 10 characters)."}), 400

    try:
        result = analyzer.analyze(text)
        return jsonify(result)
    except AnalyzerError as exc:
        return jsonify({"error": str(exc)}), 502


if __name__ == "__main__":
    if not api_key:
        print("⚠  GROQ_API_KEY not set — /api/analyze will return 500.")
    print("→  http://localhost:5000")
    app.run(debug=True, port=5000)
