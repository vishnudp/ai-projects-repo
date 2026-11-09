from services.local_llm import generate

def generate_ias_report(data):

    prompt = open(
        "prompts/ias_case_study_prompt.txt"
    ).read()

    prompt = prompt.replace(
        "{domain_data}",
        str(data)
    )

    return generate(prompt)