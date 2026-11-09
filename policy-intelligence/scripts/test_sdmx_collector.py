from app.collectors.factory import (
    create_collector_from_source,
)


def main():

    print("SDMX COLLECTOR TEST")
    print("===================")

    for source_id in [
        "oecd",
        "imf",
    ]:

        print()
        print(
            f"SOURCE: {source_id}"
        )

        collector = (
            create_collector_from_source(
                source_id
            )
        )

        print(
            "Collector:",
            type(collector).__name__,
        )

        documents = collector.collect()

        print(
            "Documents:",
            len(documents),
        )

        assert isinstance(
            documents,
            list,
        )

        for document in documents[:5]:

            print()
            print(
                "External ID:",
                document.external_id,
            )

            print(
                "Title:",
                document.title,
            )

            print(
                "Source:",
                document.source_id,
            )

            print(
                "URL:",
                document.source_url,
            )

            print(
                "Artifact:",
                document.metadata.get(
                    "artifact_type"
                ),
            )

        assert len(documents) > 0

        for document in documents:

            assert document.source_id == source_id

            assert document.title

            assert document.content

            assert (
                document.metadata[
                    "collector"
                ]
                == "sdmx"
            )

            assert (
                document.metadata[
                    "artifact_type"
                ]
                == "sdmx_dataflow"
            )

    print()
    print(
        "SDMX COLLECTOR TEST: OK"
    )


if __name__ == "__main__":
    main()