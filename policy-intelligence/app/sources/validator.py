from typing import Any

from app.sources.registry import load_sources
from app.taxonomy.sectors import sector_exists


VALID_SOURCE_TYPES = {
    "government",
    "international_organization",
    "research_institution",
    "think_tank",
    "academic",
    "journal",
    "ngo",
    "multilateral",
    "news",
}

VALID_COLLECTION_METHODS = {
    "rss",
    "api",
    "web",
    "sitemap",
    "pdf",
    "manual",
}


def _load_country_codes() -> set[str]:
    """
    Load valid country codes from the global
    country configuration.
    """

    from app.countries.config import load_countries

    countries = load_countries()

    codes = set()

    for country in countries:
        code = country.get("code")

        if code:
            codes.add(code.upper())

    return codes


def validate_source(
    source: dict[str, Any],
    country_codes: set[str],
) -> list[str]:
    """
    Validate a single source.

    Returns a list of validation errors.
    Empty list means the source is valid.
    """

    errors = []

    source_id = source.get("source_id")

    # -------------------------------------------------
    # Required fields
    # -------------------------------------------------

    required_fields = [
        "source_id",
        "name",
        "organization",
        "source_type",
        "country_scope",
        "sector_scope",
        "collection",
        "language",
        "publication_frequency",
        "reliability",
        "enabled",
    ]

    for field in required_fields:
        if field not in source:
            errors.append(
                f"{source_id or '<unknown>'}: "
                f"missing required field '{field}'"
            )

    if not source_id:
        return errors

    # -------------------------------------------------
    # source_id
    # -------------------------------------------------

    if not isinstance(source_id, str):
        errors.append(
            f"{source_id}: source_id must be a string"
        )

    # -------------------------------------------------
    # source_type
    # -------------------------------------------------

    source_type = source.get("source_type")

    if source_type not in VALID_SOURCE_TYPES:
        errors.append(
            f"{source_id}: invalid source_type "
            f"'{source_type}'"
        )

    # -------------------------------------------------
    # country scope
    # -------------------------------------------------

    country_scope = source.get("country_scope", [])

    if not isinstance(country_scope, list):
        errors.append(
            f"{source_id}: country_scope must be a list"
        )
    else:
        for country in country_scope:

            if not isinstance(country, str):
                errors.append(
                    f"{source_id}: country scope values "
                    "must be strings"
                )
                continue

            normalized_country = country.upper()

            if normalized_country == "GLOBAL":
                continue

            if normalized_country not in country_codes:
                errors.append(
                    f"{source_id}: unknown country code "
                    f"'{country}'"
                )

    # -------------------------------------------------
    # sector scope
    # -------------------------------------------------

    sector_scope = source.get("sector_scope", [])

    if not isinstance(sector_scope, list):
        errors.append(
            f"{source_id}: sector_scope must be a list"
        )
    else:
        for sector in sector_scope:

            if not isinstance(sector, str):
                errors.append(
                    f"{source_id}: sector scope values "
                    "must be strings"
                )
                continue

            if sector.lower() == "global":
                continue

            if not sector_exists(sector):
                errors.append(
                    f"{source_id}: unknown sector "
                    f"'{sector}'"
                )

    # -------------------------------------------------
    # collection
    # -------------------------------------------------

    collection = source.get("collection")

    if not isinstance(collection, dict):
        errors.append(
            f"{source_id}: collection must be an object"
        )

    else:

        method = collection.get("method")

        if method not in VALID_COLLECTION_METHODS:
            errors.append(
                f"{source_id}: invalid collection method "
                f"'{method}'"
            )

    # -------------------------------------------------
    # language
    # -------------------------------------------------

    languages = source.get("language")

    if not isinstance(languages, list):
        errors.append(
            f"{source_id}: language must be a list"
        )

    # -------------------------------------------------
    # reliability
    # -------------------------------------------------

    reliability = source.get("reliability")

    if not isinstance(reliability, dict):
        errors.append(
            f"{source_id}: reliability must be an object"
        )

    else:

        tier = reliability.get("tier")
        score = reliability.get("score")

        if not isinstance(tier, int):
            errors.append(
                f"{source_id}: reliability.tier "
                "must be an integer"
            )

        if (
            not isinstance(score, (int, float))
            or isinstance(score, bool)
        ):
            errors.append(
                f"{source_id}: reliability.score "
                "must be numeric"
            )

        elif not 0 <= score <= 1:
            errors.append(
                f"{source_id}: reliability.score "
                "must be between 0 and 1"
            )

    # -------------------------------------------------
    # enabled
    # -------------------------------------------------

    enabled = source.get("enabled")

    if not isinstance(enabled, bool):
        errors.append(
            f"{source_id}: enabled must be boolean"
        )

    return errors


def validate_registry() -> list[str]:
    """
    Validate the complete source registry.

    Returns all validation errors.
    """

    errors = []

    sources = load_sources()
    country_codes = _load_country_codes()

    # -------------------------------------------------
    # Empty registry
    # -------------------------------------------------

    if not sources:
        errors.append(
            "Source registry contains no sources"
        )

        return errors

    # -------------------------------------------------
    # Duplicate source IDs
    # -------------------------------------------------

    seen_ids = set()

    for source in sources:

        source_id = source.get("source_id")

        if source_id in seen_ids:
            errors.append(
                f"{source_id}: duplicate source_id"
            )

        seen_ids.add(source_id)

    # -------------------------------------------------
    # Validate individual sources
    # -------------------------------------------------

    for source in sources:

        errors.extend(
            validate_source(
                source,
                country_codes,
            )
        )

    return errors


def main() -> None:
    """
    CLI entry point.
    """

    print()
    print("Source Registry Validation")
    print("=" * 30)
    print()

    sources = load_sources()

    errors = validate_registry()

    print(
        f"Sources checked: {len(sources)}"
    )

    print(
        f"Errors:          {len(errors)}"
    )

    print()

    if errors:

        print("VALIDATION FAILED")
        print()

        for error in errors:
            print(f"✗ {error}")

        raise SystemExit(1)

    print("VALIDATION PASSED")
    print()

    for source in sources:
        print(
            f"✓ {source['source_id']}"
        )

    print()


if __name__ == "__main__":
    main()