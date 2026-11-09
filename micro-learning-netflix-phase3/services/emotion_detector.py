from services.ollama_service import ollama
from services.json_parser import parse_llm_json


def detect_emotion(summary):

    prompt = f"""
You are an emotion classifier.

Return ONLY JSON.

{{
  "primary_emotion": "",
  "secondary_emotion": "",
  "confidence": 0,
  "tone": ""
}}

SUMMARY:

{summary}
"""

    response = ollama.generate(
        prompt,
        "qwen3:4b"
    )

    return parse_llm_json(response) 