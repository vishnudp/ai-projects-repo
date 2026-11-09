from app.collection.multi_source_controller import (
    MultiSourceCollectionController,
)


def main():

    controller = MultiSourceCollectionController(
        max_workers=3
    )

    source_ids = [
        "world_bank",
        "oecd",
        "who",
    ]

    print("MULTI-SOURCE COLLECTION")
    print("=======================")

    result = controller.collect(
        source_ids
    )

    # -------------------------------------------------
    # SUMMARY
    # -------------------------------------------------

    print()
    print("SUMMARY")
    print("-------")

    print(
        "Requested sources:",
        result.total_sources,
    )

    print(
        "Successful sources:",
        result.successful_sources,
    )

    print(
        "Failed sources:",
        result.failed_sources,
    )

    print(
        "Total documents:",
        result.total_documents,
    )

    print(
        "Total duration ms:",
        result.duration_ms,
    )

    # -------------------------------------------------
    # AGGREGATED METRICS
    # -------------------------------------------------

    print()
    print("AGGREGATED METRICS")
    print("-------------------")

    for key, value in result.metrics.items():
        print(
            f"{key}: {value}"
        )

    # -------------------------------------------------
    # SOURCE RESULTS
    # -------------------------------------------------

    print()
    print("SOURCE RESULTS")
    print("--------------")

    for source_result in result.results:

        print()
        print(
            "Source:",
            source_result.source_id,
        )

        print(
            "Collector:",
            source_result.collector_type,
        )

        print(
            "Documents:",
            source_result.collected,
        )

        print(
            "Duration ms:",
            source_result.duration_ms,
        )

        print(
            "Errors:",
            source_result.errors,
        )

    # -------------------------------------------------
    # ERRORS
    # -------------------------------------------------

    print()
    print("ERRORS")
    print("------")

    if result.errors:

        for error in result.errors:
            print(error)

    else:
        print("None")

    # =================================================
    # TEST CONTRACT
    # =================================================

    print()
    print("VALIDATING CONTRACT")
    print("-------------------")

    # ---------------------------------------------
    # 1. Every requested source must produce a result
    # ---------------------------------------------

    assert (
        result.total_sources
        == len(source_ids)
    )

    assert (
        len(result.results)
        == len(source_ids)
    )

    # ---------------------------------------------
    # 2. Every source must be classified as either
    #    successful or failed.
    # ---------------------------------------------

    assert (
        result.successful_sources
        + result.failed_sources
        == result.total_sources
    )

    # ---------------------------------------------
    # 3. Document count must never be negative.
    # ---------------------------------------------

    assert result.total_documents >= 0

    # ---------------------------------------------
    # 4. Duration must be recorded.
    # ---------------------------------------------

    assert result.duration_ms >= 0

    # ---------------------------------------------
    # 5. Metrics must match the actual result.
    # ---------------------------------------------

    assert (
        result.metrics["total_sources"]
        == result.total_sources
    )

    assert (
        result.metrics["successful_sources"]
        == result.successful_sources
    )

    assert (
        result.metrics["failed_sources"]
        == result.failed_sources
    )

    assert (
        result.metrics["total_documents"]
        == result.total_documents
    )

    assert (
        result.metrics["duration_ms"]
        == result.duration_ms
    )

    # ---------------------------------------------
    # 6. Every requested source must appear exactly
    #    once in the result.
    # ---------------------------------------------

    returned_source_ids = {
        source_result.source_id
        for source_result in result.results
    }

    assert (
        returned_source_ids
        == set(source_ids)
    )

    # ---------------------------------------------
    # 7. Every source must have timing information.
    # ---------------------------------------------

    for source_result in result.results:

        assert (
            source_result.duration_ms >= 0
        )

        assert (
            source_result.collected >= 0
        )

    # ---------------------------------------------
    # 8. Validate source failure isolation.
    #
    #    If OECD fails with 403, that is a valid
    #    source-level failure. It must NOT make the
    #    entire multi-source controller fail.
    # ---------------------------------------------

    if "oecd" in result.errors:

        print()
        print(
            "OECD returned HTTP 403."
        )

        print(
            "Treating OECD as a source-level failure."
        )

        print(
            "Other sources were allowed to continue."
        )

        # OECD must be represented as failed.
        assert result.failed_sources >= 1

        # The failed source must have a result.
        oecd_result = next(
            item
            for item in result.results
            if item.source_id == "oecd"
        )

        assert (
            oecd_result.source_id
            == "oecd"
        )

        assert (
            len(oecd_result.errors)
            > 0
        )

    # ---------------------------------------------
    # 9. If there are no errors, all sources succeeded.
    # ---------------------------------------------

    else:

        assert (
            result.failed_sources
            == 0
        )

        assert (
            result.successful_sources
            == result.total_sources
        )

    print()
    print(
        "MULTI-SOURCE COLLECTION TEST: OK"
    )


if __name__ == "__main__":
    main()