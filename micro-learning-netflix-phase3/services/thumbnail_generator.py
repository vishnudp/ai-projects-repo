from services.ollama_service import ollama
from services.json_parser import parse_llm_json


def generate_thumbnail(summary):

    prompt = f"""
Create an image prompt.

Return ONLY JSON.

{{
  "thumbnail_prompt": ""
}}

STYLE:
- Netflix documentary
- Cinematic
- Ultra realistic
- Dramatic lighting
- 4k

CONTENT:

{summary}
"""

    response = ollama.generate(
        prompt,
        "qwen3:4b"
    )

    return parse_llm_json(response)