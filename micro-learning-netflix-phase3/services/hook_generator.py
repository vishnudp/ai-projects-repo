from services.ollama_service import ollama
from services.json_parser import parse_llm_json


def generate_hook(summary):

    print("RUNNING HOOK")

    prompt = f"""
You are a world-class Netflix documentary director.

Create a viral reel hook.

Rules:
- Max 12 words
- Must create curiosity
- Must include a surprising fact, number, or insight
- Never return empty fields

Return ONLY JSON.

Example:

{{
  "hook": "250 Million Indians Escaped Poverty. Here's What Happened.",
  "pattern": "surprising_stat",
  "strength": 95
}}

CONTENT:

{summary}
"""

    response = ollama.generate(
        prompt,
        "qwen3:4b"
    )

    result = parse_llm_json(response)

    # Fallback if model returns blanks

    if not result.get("hook"):

        return {
            "hook": "This Changes Everything About India's Future.",
            "pattern": "curiosity",
            "strength": 70
        }

    return result