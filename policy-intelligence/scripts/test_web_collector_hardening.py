from app.collectors.web_collector import WebCollector


def main():

    config = {
        "source_id": "test-oecd",
        "name": "Test OECD",

        "collection": {
            "method": "web",
            "base_url": "https://example.org",

            "timeout": 15,
            "retries": 3,

            "max_content_size": 5 * 1024 * 1024,
        },
    }

    collector = WebCollector(
        source_id="test-oecd",
        config=config,
    )

    documents = collector.collect()

    assert len(documents) == 1

    document = documents[0]

    print("COLLECTED:", len(documents))

    print("SOURCE:", document.source_id)

    print("URL:", document.source_url)

    print(
        "CONTENT LENGTH:",
        len(document.content or ""),
    )

    print(
        "METADATA:",
        document.metadata,
    )

    assert document.source_id == "test-oecd"

    assert (
        document.source_url
        == "https://example.org"
    )

    assert document.content

    assert (
        document.metadata["collector"]
        == "web"
    )

    assert (
        document.metadata["http_status"]
        == 200
    )

    print()
    print("WEB COLLECTOR HARDENING TEST: OK")


if __name__ == "__main__":
    main()