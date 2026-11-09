from services.gemini_service import generate


def generate_case_study(all_cases):

    prompt = open(
        "prompts/case_study_prompt.txt"
    ).read()

    prompt = prompt.replace(
        "{input_data}",
        str(all_cases)
    )

    return generate(prompt)