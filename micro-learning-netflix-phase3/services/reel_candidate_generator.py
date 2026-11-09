from services.ollama_service import ollama
from services.json_parser import parse_llm_json
from config import MODELS


def generate_reel_candidate(context):

    prompt = f"""
You are a Netflix-style micro-learning reel strategist.
Generate ONE highly engaging reel.
Return ONLY JSON.

{{
  "hook": "",
  "insight": "",
  "script": "",
  "cta": "",
  "reel_score": 0,
  "target_duration": 45,
  "viral_factors": []
}}

CONTEXT:
{context}
"""

    response = ollama.generate(
        prompt,
        MODELS["reel_candidate"]
    )

    return parse_llm_json(response)