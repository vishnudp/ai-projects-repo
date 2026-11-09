from services.ollama_service import ollama
from services.json_parser import parse_llm_json


def generate_visual_plan(storyboard):

    prompt = f"""
You are a Netflix cinematographer.

For every storyboard scene generate:

- camera angle
- transition
- motion
- visual effects

Return ONLY JSON.

{{
  "visual_plan": [
    {{
      "scene": 1,
      "camera": "",
      "transition": "",
      "motion": "",
      "effects": ""
    }}
  ]
}}

STORYBOARD:

{storyboard}
"""

    response = ollama.generate(
        prompt,
        "qwen3:4b"
    )

    return parse_llm_json(response)