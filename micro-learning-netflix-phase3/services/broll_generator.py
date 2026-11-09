from services.ollama_service import ollama
from services.json_parser import parse_llm_json


def generate_broll(summary):

    prompt = f"""
You are a Netflix visual director.

Generate cinematic B-roll ideas.

Return ONLY JSON.

{{
  "broll":[
    {{
      "scene":"",
      "visual":"",
      "search_keywords":[]
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