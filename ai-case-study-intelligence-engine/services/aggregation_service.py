import json
from services.local_llm import generate

def aggregate(summaries):

    prompt = open(
        "prompts/aggregation_prompt.txt"
    ).read()

    prompt = prompt.replace(
        "{summaries}",
        json.dumps(summaries)
    )

    return generate(prompt)