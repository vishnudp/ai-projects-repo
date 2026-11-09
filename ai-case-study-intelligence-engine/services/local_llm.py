from ollama import chat

MODEL = "qwen3:4b"

def generate(prompt):

    response = chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]