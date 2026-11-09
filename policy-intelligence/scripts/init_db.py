from app.documents.repository import (
    initialize_database,
)


if __name__ == "__main__":
    initialize_database()

    print(
        "Database initialized successfully."
    )