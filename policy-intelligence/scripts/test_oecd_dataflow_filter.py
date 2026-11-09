from app.collection.collection_controller import (
    CollectionController,
)


def main():

    print()
    print("OECD DATAFLOW FILTER INTEGRATION TEST")
    print("=====================================")
    print()

    controller = CollectionController()

    print("Collecting OECD dataflows...")
    print()

    result = controller.collect(
        "oecd"
    )

    print(
        "Source:",
        result.source_id,
    )

    print(
        "Collector:",
        result.collector_type,
    )

    print(
        "Dataflows discovered:",
        result.discovered,
    )

    print(
        "Candidate dataflows:",
        result.candidates,
    )

    print(
        "Selected:",
        result.selected,
    )

    print(
        "Retrieved:",
        result.retrieved,
    )

    print(
        "Duration:",
        result.duration_ms,
        "ms",
    )

    print()

    # -----------------------------------------------------
    # Errors
    # -----------------------------------------------------

    if result.errors:

        print("ERRORS:")

        for error in result.errors:

            print(
                f"  - {error}"
            )

        raise RuntimeError(
            "OECD collection failed"
        )

    # -----------------------------------------------------
    # Assertions
    # -----------------------------------------------------

    assert (
        result.collector_type
        == "SDMXCollector"
    ), (
        "Expected SDMXCollector"
    )

    assert (
        result.discovered > 0
    ), (
        "No OECD dataflows discovered"
    )

    assert (
        result.candidates > 0
    ), (
        "No OECD candidate dataflows"
    )

    assert (
        result.candidates
        <= result.discovered
    ), (
        "Candidate count exceeds "
        "discovered count"
    )

    assert (
        len(result.documents)
        == result.discovered
    ), (
        "Discovered document count "
        "does not match result.documents"
    )

    assert (
        len(result.candidate_documents)
        == result.candidates
    ), (
        "Candidate document count "
        "does not match candidates"
    )

    # -----------------------------------------------------
    # Inspect top candidates
    # -----------------------------------------------------

    print(
        "TOP CANDIDATES"
    )
    print(
        "--------------"
    )

    for index, document in enumerate(
        result.candidate_documents[:10],
        start=1,
    ):

        print(
            f"{index}. "
            f"{document.title}"
        )

        print(
            f"   Dataflow ID: "
            f"{document.metadata.get('dataflow_id')}"
        )

        print(
            f"   Artifact: "
            f"{document.metadata.get('artifact_type')}"
        )

        print()

    print(
        "PASS: OECD SDMX discovery"
    )

    print(
        "PASS: DataflowFilter integration"
    )

    print(
        "PASS: discovery/candidate counts"
    )

    print(
        "PASS: candidate documents retained"
    )

    print()

    print(
        "OECD DATAFLOW FILTER INTEGRATION TEST PASSED"
    )

    print(
        "============================================="
    )


if __name__ == "__main__":
    main()