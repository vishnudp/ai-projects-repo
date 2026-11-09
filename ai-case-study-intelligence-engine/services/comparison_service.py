import json

from services.local_llm import generate

def compare_case_studies(cases):

    prompt = open(
        "prompts/comparison_prompt.txt"
    ).read()

    prompt = prompt.replace(
        "{cases}",
        json.dumps(cases)
    )

    return generate(prompt)