from app.collectors.test_collector import TestCollector
from app.db.database import initialize_database
from app.db.repositories import DocumentRepository
from app.ingestion.controller import IngestionController


def main() -> None:

    initialize_database()

    collector = TestCollector(
        source_id="test-oecd",
        config={
            "source_name": "Test OECD"
        },
    )

    raw_documents = collector.collect()

    print("COLLECTOR:")
    print(f"Collected: {len(raw_documents)}")

    controller = IngestionController(
        document_repository=DocumentRepository()
    )

    result = controller.ingest(
        source_id="test-oecd",
        raw_documents=raw_documents,
    )

    print()
    print("INGESTION RESULT:")
    print(result)

    assert result.collected == 1
    assert result.normalized == 1
    assert result.failed == 0

    print()
    print("COLLECTOR → CONTROLLER: OK")


if __name__ == "__main__":
    main()