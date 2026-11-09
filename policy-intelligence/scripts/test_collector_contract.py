from app.collectors.factory import create_collector
from app.ingestion.base import RawDocument


def main():

    methods = [
        "web",
        "rss",
        "api",
        "search",
    ]

    for method in methods:

        config = {
            "source_id": "test-source",
            "name": "Test Source",
            "collection": {
                "method": method,
            },
        }

        collector = create_collector(
            source_id="test-source",
            config=config,
        )

        assert collector.source_id == "test-source"

        print(
            method.upper(),
            "->",
            type(collector).__name__,
            "CONTRACT CREATED"
        )

    # -------------------------------------------------
    # Explicit contract validation
    # -------------------------------------------------

    collector = create_collector(
        source_id="test-source",
        config={
            "collection": {
                "method": "api",
            }
        },
    )

    documents = collector.collect()

    assert isinstance(
        documents,
        list,
    )

    assert all(
        isinstance(
            document,
            RawDocument,
        )
        for document in documents
    )

    print(
        "API OUTPUT:",
        type(documents).__name__,
        "VALID"
    )

    # -------------------------------------------------
    # Source identity
    # -------------------------------------------------

    collector = create_collector(
        source_id="TEST-SOURCE",
        config={
            "collection": {
                "method": "search",
            }
        },
    )

    assert collector.source_id == "test-source"

    print(
        "SOURCE NORMALIZATION: OK"
    )

    print()
    print(
        "COLLECTOR CONTRACT TEST: OK"
    )


if __name__ == "__main__":
    main()
