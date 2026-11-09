from app.collectors.web_collector import WebCollector


def main():

    config = {
        "source_id": "test-oecd",
        "name": "Test OECD",
        "collection": {
            "method": "web",
            "base_url": "https://example.org",
            "timeout": 15,
        },
    }

    collector = WebCollector(
        source_id="test-oecd",
        config=config,
    )

    documents = collector.collect()

    print("DOCUMENT COUNT:")
    print(len(documents))

    document = documents[0]

    print("\nTITLE:")
    print(document.title)

    print("\nSOURCE:")
    print(document.source_id)

    print("\nURL:")
    print(document.source_url)

    print("\nCONTENT LENGTH:")
    print(len(document.content or ""))

    print("\nMETADATA:")
    print(document.metadata)

    assert len(documents) == 1
    assert document.source_id == "test-oecd"
    assert document.source_url == "https://example.org"
    assert document.content

    print("\nWEB COLLECTOR TEST: OK")


if __name__ == "__main__":
    main()