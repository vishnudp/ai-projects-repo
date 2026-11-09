from services.ollama_service import ollama
from services.json_parser import parse_llm_json
from config import MODELS

def generate_mini_summary(summary):

    prompt = f"""
Return ONLY valid JSON.

Do NOT explain.
Do NOT think.
Do NOT analyze.
Do NOT describe your steps.
Do NOT write any text before JSON.
Do NOT write any text after JSON.

Output format:

{{
  "topic": "",
  "key_ideas": [],
  "facts": [],
  "numbers": [],
  "quotes": []
}}

IMPORTANT:
If no quote exists return:

"quotes": []

CONTENT:
{summary}

JSON:
"""

    response = ollama.generate(
        prompt,
        MODELS["summary"]
    )

    return parse_llm_json(response)