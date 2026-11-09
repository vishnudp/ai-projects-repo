from services.ollama_service import ollama
from services.json_parser import parse_llm_json


def extract_learning_moments(summary):

    prompt = f"""
Return ONLY valid JSON.

{{
  "moments": [
    {{
      "title": "",
      "reason": "",
      "importance": 0
    }}
  ]
}}

SUMMARY:

{summary}
"""

    response = ollama.generate(
        prompt,
        "qwen3:4b"
    )

    return parse_llm_json(response)