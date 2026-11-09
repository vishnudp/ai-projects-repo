from app.ingestion.pipeline import IngestionPipeline
from app.ingestion.collection_controller import (
    CollectionController,
    CollectionResult,
)
from app.ingestion.base import RawDocument


class MockCollectionController:

    def collect(
        self,
        source_id: str,
    ) -> CollectionResult:

        document = RawDocument(
            external_id="pipeline-test-001",

            title="Global AI Policy Test",

            source_url=(
                "https://example.org/"
                "pipeline-test"
            ),

            source_id=source_id,

            source_name="Pipeline Test Source",

            content=(
                "Artificial intelligence "
                "policy is becoming increasingly "
                "important for national policy "
                "planning."
            ),
        )

        return CollectionResult(
            source_id=source_id,

            collector_type="MockCollector",

            collected=1,

            documents=[
                document
            ],

            errors=[],
        )


def main():

    pipeline = IngestionPipeline(
        collection_controller=(
            MockCollectionController()
        )
    )

    print(
        "RUNNING INGESTION PIPELINE..."
    )

    print()

    result = pipeline.run(
        source_id="test-oecd"
    )

    print(
        "SOURCE:",
        result.source_id
    )

    print()
    print("COLLECTION")
    print("----------")

    print(
        "Collector:",
        result.collection.collector_type
    )

    print(
        "Collected:",
        result.collection.collected
    )

    print(
        "Errors:",
        result.collection.errors
    )

    if result.ingestion is not None:

        print()
        print("INGESTION")
        print("---------")

        print(
            "Normalized:",
            result.ingestion.normalized
        )

        print(
            "Inserted:",
            result.ingestion.inserted
        )

        print(
            "Duplicates:",
            result.ingestion.duplicates
        )

        print(
            "Failed:",
            result.ingestion.failed
        )

        print(
            "Errors:",
            result.ingestion.errors
        )

    else:

        print()
        print("INGESTION: SKIPPED")

    # -----------------------------------------
    # Assertions
    # -----------------------------------------

    assert (
        result.source_id
        == "test-oecd"
    )

    assert (
        result.collection.errors
        == []
    )

    assert (
        result.collection.collected
        == 1
    )

    assert (
        result.ingestion is not None
    )

    assert (
        result.ingestion.normalized
        == 1
    )

    assert (
        result.ingestion.failed
        == 0
    )

    assert (
        result.ingestion.inserted
        + result.ingestion.duplicates
        == 1
    )

    print()
    print(
        "INGESTION PIPELINE TEST: OK"
    )


if __name__ == "__main__":
    main()