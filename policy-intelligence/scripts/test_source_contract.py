from app.sources.repository import SourceRepository


def main():

    repository = SourceRepository()

    source = repository.get_by_id(
        "oecd"
    )

    assert source is not None

    print("SOURCE:")
    print(source)

    print()
    print("SOURCE ID:", source.source_id)
    print("NAME:", source.name)
    print("ORGANIZATION:", source.organization)

    print(
        "COUNTRY SCOPE:",
        source.country_scope,
    )

    print(
        "SECTOR SCOPE:",
        source.sector_scope,
    )

    print(
        "COLLECTION METHOD:",
        source.collection.method,
    )

    print(
        "BASE URL:",
        source.collection.base_url,
    )

    print(
        "RELIABILITY:",
        source.reliability_score,
    )

    print(
        "ENABLED:",
        source.enabled,
    )

    assert source.source_id == "oecd"

    assert source.collection is not None

    assert source.collection.method == "web"

    assert source.enabled is True

    assert source.reliability_score == 0.98

    print()
    print("SOURCE CONTRACT TEST: OK")


if __name__ == "__main__":
    main()
