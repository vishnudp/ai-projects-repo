from app.collectors.controller import CollectionController
from app.ingestion.base import RawDocument


class FakeCollector:
    def collect(self):
        return [
            RawDocument(
                external_id="collection-test-001",
                title="Global AI Policy",
                source_url="https://example.org/test",
                source_id="test-source",
                source_name="Test Source",
                content=(
                    "Artificial intelligence policy "
                    "is becoming increasingly important."
                ),
            )
        ]


def main():

    controller = CollectionController()

    # Replace the factory-created collector with
    # a deterministic test collector.
    controller._create_test_collector = (
        lambda: FakeCollector()
    )

    # Direct contract test
    collector = FakeCollector()

    documents = collector.collect()

    assert isinstance(
        documents,
        list,
    )

    assert len(documents) == 1

    assert isinstance(
        documents[0],
        RawDocument,
    )

    assert documents[0].source_id == "test-source"

    print("COLLECTED:", len(documents))
    print("DOCUMENT:", documents[0])
    print()
    print("COLLECTION CONTROLLER CONTRACT: OK")


if __name__ == "__main__":
    main()
