from services.ollama_service import ollama
from services.json_parser import parse_llm_json


def generate_storyboard(reel_context):

    prompt = f"""
You are a Netflix documentary director.

Create a 45 second viral reel storyboard.

Create 6-8 scenes.

Return ONLY JSON.

{{
  "scenes": [
    {{
      "scene_no": 1,
      "start": 0,
      "end": 5,
      "purpose": "",
      "visual": "",
      "voiceover": ""
    }}
  ]
}}

REEL CONTEXT:

{reel_context}
"""

    response = ollama.generate(
        prompt,
        "qwen3:4b"
    )

    return parse_llm_json(response)