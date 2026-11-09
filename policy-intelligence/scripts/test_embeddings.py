from app.embeddings.service import (
    embedding_service,
)


if __name__ == "__main__":

    text = """
    Renewable energy investment is increasing
    globally as countries pursue energy security,
    decarbonization and economic development.
    """

    vector = embedding_service.embed(text)

    print(
        "Embedding dimensions:",
        len(vector),
    )

    print(
        "First 5 values:",
        vector[:5],
    )