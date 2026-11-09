from app.db.database import initialize_database
from app.db.repositories import DocumentRepository
from app.ingestion.base import RawDocument
from app.ingestion.controller import IngestionController


def main() -> None:

    # -------------------------------------------------
    # Initialize database
    # -------------------------------------------------

    initialize_database()

    repository = DocumentRepository()

    # -------------------------------------------------
    # Controller
    # -------------------------------------------------

    controller = IngestionController(
        document_repository=repository
    )

    # -------------------------------------------------
    # Test document
    # -------------------------------------------------

    raw_document = RawDocument(
        external_id="controller-test-001",

        title="   Global AI Policy   ",

        source_url=(
            "https://example.org/"
            "controller-test"
        ),

        source_id="test-oecd",

        source_name="Test OECD",

        content="""
            Artificial intelligence policy
            is becoming increasingly important
            for national policy planning.
        """,
    )

    # -------------------------------------------------
    # First ingestion
    # -------------------------------------------------

    result = controller.ingest(
        source_id="test-oecd",
        raw_documents=[
            raw_document
        ],
    )

    print("FIRST INGESTION:")
    print(result)

    assert result.collected == 1
    assert result.normalized == 1
    assert result.inserted == 1
    assert result.duplicates == 0
    assert result.failed == 0

    # -------------------------------------------------
    # Verify document
    # -------------------------------------------------

    document = repository.get_by_id(
        "controller-test-001"
    )

    assert document is not None

    print()
    print("DOCUMENT:")
    print(document)

    print()
    print("TITLE:", document.title)
    print("SOURCE:", document.source_id)
    print("CONTENT:", document.content)
    print("CONTENT HASH:", document.content_hash)

    # Classification must NOT happen here.
    assert document.countries == []
    assert document.sectors == []
    assert document.policy_domains == []
    assert document.topics == []

    # -------------------------------------------------
    # Second ingestion
    # -------------------------------------------------

    duplicate_document = RawDocument(
        external_id="controller-test-001",

        title="Global AI Policy",

        source_url=(
            "https://example.org/"
            "controller-test"
        ),

        source_id="test-oecd",

        source_name="Test OECD",

        content="""
            Artificial intelligence policy
            is becoming increasingly important
            for national policy planning.
        """,
    )

    duplicate_result = controller.ingest(
        source_id="test-oecd",
        raw_documents=[
            duplicate_document
        ],
    )

    print()
    print("SECOND INGESTION:")
    print(duplicate_result)

    assert duplicate_result.collected == 1
    assert duplicate_result.normalized == 1
    assert duplicate_result.inserted == 0
    assert duplicate_result.duplicates == 1
    assert duplicate_result.failed == 0

    # -------------------------------------------------
    # Database count
    # -------------------------------------------------

    count = repository.count()

    print()
    print("DOCUMENT COUNT:", count)

    print()
    print("INGESTION CONTROLLER TEST: OK")


if __name__ == "__main__":
    main()