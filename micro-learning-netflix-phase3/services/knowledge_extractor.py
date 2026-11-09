from services.ollama_service import ollama
from services.json_parser import parse_llm_json


def extract_knowledge(summary):

    prompt = f"""
Return ONLY valid JSON.

{{
  "concepts": [
    {{
      "name": "",
      "description": ""
    }}
  ],
  "frameworks": [],
  "principles": [],
  "examples": []
}}

SUMMARY:

{summary}
"""

    response = ollama.generate(
        prompt,
        "qwen3:4b"
    )

    return parse_llm_json(response)