from services.ollama_service import ollama
from services.json_parser import parse_llm_json


def generate_insight(summary):

    prompt = f"""
You are a Netflix documentary writer.

Extract ONE powerful insight.

Return ONLY JSON.

{{
  "insight":"",
  "reason":""
}}

CONTENT:

{summary}
"""

    response = ollama.generate(
        prompt,
        "qwen3:4b"
    )

    return parse_llm_json(response)