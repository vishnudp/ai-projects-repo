from services.ollama_service import ollama
from services.json_parser import parse_llm_json
from config import MODELS


def generate_summary(text):

    prompt = f"""
Return ONLY JSON.
{{
  "title":"",
  "overview":"",
  "key_points":[],
  "important_quotes":[]
}}

CONTENT:
{text}
""" 

    print("TEXT SIZE:", len(text))
    print("PROMPT SIZE:", len(prompt))

    response = ollama.generate(
        prompt,
        MODELS["summary"]
    )
   
    return parse_llm_json(response)