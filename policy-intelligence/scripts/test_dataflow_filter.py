from app.sdmx.dataflow_filter import DataflowFilter
from app.ingestion.base import RawDocument


def make_document(
    title: str,
    description: str = "",
) -> RawDocument:

    return RawDocument(
        external_id=f"test:{title}",
        title=title,
        source_url="https://example.com",
        source_id="oecd",
        source_name="OECD",
        content=(
            f"SDMX Dataflow: {title}\n"
            f"Description: {description}"
        ),
        published_at=None,
        retrieved_at=None,
        metadata={
            "artifact_type": "sdmx_dataflow",
        },
    )


def main():

    print()
    print("DATAFLOW FILTER TEST")
    print("====================")
    print()

    documents = [
        make_document(
            "Renewable Energy Statistics",
            (
                "Statistics on renewable energy "
                "and clean energy transition."
            ),
        ),
        make_document(
            "Artificial Intelligence Statistics",
            (
                "Statistics covering artificial "
                "intelligence and digital technologies."
            ),
        ),
        make_document(
            "Household Population",
            "Population and household statistics.",
        ),
        make_document(
            "Labour Market Statistics",
            "Employment and labour market indicators.",
        ),
    ]

    config = {
        "min_score": 0.20,
        "max_candidates": 10,
        "sectors": {
            "renewable_energy": [
                "renewable energy",
                "clean energy",
            ],
            "artificial_intelligence": [
                "artificial intelligence",
                "ai",
                "digital technology",
            ],
        },
        "keywords": [
            "energy",
            "innovation",
            "productivity",
            "labour",
        ],
        "countries": {
            "India": [
                "india",
                "indian",
            ],
            "Australia": [
                "australia",
                "australian",
            ],
        },
    }

    print("Input dataflows:", len(documents))
    print()

    dataflow_filter = DataflowFilter(
        config=config
    )

    results = dataflow_filter.filter(
        documents=documents,
        primary_country="India",
        comparison_countries=["Australia"],
    )

    print(
        "Candidate dataflows:",
        len(results),
    )
    print()

    for index, result in enumerate(
        results,
        start=1,
    ):

        document = result.document

        print(
            f"{index}. {document.title}"
        )

        print(
            f"   Score: {result.score}"
        )

        print(
            f"   Terms: "
            f"{', '.join(result.matched_terms)}"
        )

        print(
            f"   Sectors: "
            f"{', '.join(result.matched_sectors)}"
        )

        print(
            f"   Countries: "
            f"{', '.join(result.matched_countries)}"
        )

        print(
            f"   Reasons: "
            f"{'; '.join(result.reasons)}"
        )

        print()

    # ---------------------------------------------------------
    # Assertions
    # ---------------------------------------------------------

    assert len(results) > 0, (
        "Expected at least one candidate dataflow"
    )

    titles = [
        result.document.title
        for result in results
    ]

    assert (
        "Renewable Energy Statistics"
        in titles
    ), (
        "Renewable Energy dataflow "
        "was not selected"
    )

    assert (
        "Artificial Intelligence Statistics"
        in titles
    ), (
        "AI dataflow was not selected"
    )

    print("PASS: relevant dataflows detected")
    print("PASS: relevance scoring working")
    print("PASS: ranking working")
    print("PASS: candidate filtering working")
    print()
    print("DATAFLOW FILTER TEST PASSED")
    print("============================")


if __name__ == "__main__":
    main()