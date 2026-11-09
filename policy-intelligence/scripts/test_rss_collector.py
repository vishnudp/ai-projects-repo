from app.collectors.rss_collector import RSSCollector


def main():

    config = {
        "source_id": "test-rss",

        "name": "Test RSS",

        "collection": {
            "method": "rss",

            "rss_url": (
                "https://feeds.bbci.co.uk/news/"
                "world/rss.xml"
            ),

            "timeout": 15,

            "retries": 3,
        },
    }

    collector = RSSCollector(
        source_id="test-rss",
        config=config,
    )

    documents = collector.collect()

    print(
        "DOCUMENT COUNT:",
        len(documents),
    )

    assert documents

    document = documents[0]

    print("\nFIRST DOCUMENT:")
    print("TITLE:", document.title)
    print("URL:", document.source_url)
    print("SOURCE:", document.source_id)
    print("PUBLISHED:", document.published_at)
    print("CONTENT LENGTH:", len(document.content or ""))
    print("METADATA:", document.metadata)

    assert document.source_id == "test-rss"
    assert document.source_url
    assert document.title

    assert (
        document.metadata["collector"]
        == "rss"
    )

    print("\nRSS COLLECTOR TEST: OK")


if __name__ == "__main__":
    main()