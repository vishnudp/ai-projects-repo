from services.ollama_service import ollama
from services.json_parser import parse_llm_json
from config import MODELS


def extract_metadata(summary):

    prompt = f"""
You are a metadata extraction engine.

Return ONLY JSON.

JSON FORMAT:

{{
  "topics": [],
  "keywords": [],
  "entities": [],
  "difficulty": "",
  "category": "",
  "estimated_audience": ""
}}

SUMMARY:

{summary}
"""

    response = ollama.generate(
        prompt,
        MODELS["metadata"]
    )

    return parse_llm_json(response)