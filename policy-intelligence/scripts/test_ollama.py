from app.llm.ollama_client import (
    ollama_client,
)


if __name__ == "__main__":

    result = ollama_client.chat(
        """
        Return exactly one sentence explaining
        why renewable energy is important for
        national policy planning.
        """,
        model="qwen3:4b",
        temperature=0.1,
    )

    print("\nMODEL:")
    print(result["model"])

    print("\nRESPONSE:")
    print(result["content"])