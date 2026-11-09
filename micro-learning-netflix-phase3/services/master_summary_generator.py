from services.ollama_service import ollama
from services.json_parser import parse_llm_json
from config import MODELS


def generate_master_summary(content):

    prompt = f"""
You are an expert instructional designer.

Create a clean learning summary.

Return ONLY valid JSON.

Do NOT explain.
Do NOT think.
Do NOT analyze.
Do NOT describe your steps.
Do NOT write any text before JSON.
Do NOT write any text after JSON.

JSON FORMAT:

{{
  "title": "",
  "overview": "",
  "key_ideas": [],
  "key_insights": [],
  "important_numbers": [],
  "important_quotes": [],
  "learning_outcome": ""
}}

MINI SUMMARIES:

{content}
"""

    response = ollama.generate(
        prompt,
        MODELS["master_summary"]
    )

    return parse_llm_json(response)