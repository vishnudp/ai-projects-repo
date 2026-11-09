from pathlib import Path
from typing import Any

import yaml


BASE_DIR = Path(__file__).resolve().parents[2]

SOURCES_FILE = (
    BASE_DIR
    / "config"
    / "sources"
    / "sources.yaml"
)


def load_registry() -> dict[str, Any]:
    """
    Load the global source registry.
    """

    if not SOURCES_FILE.exists():
        raise FileNotFoundError(
            f"Source registry not found: {SOURCES_FILE}"
        )

    with SOURCES_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        data = yaml.safe_load(file) or {}

    registry = data.get("registry")

    if not isinstance(registry, dict):
        raise ValueError(
            "'registry' must be an object"
        )

    return registry


def load_sources() -> list[dict[str, Any]]:
    """
    Return all registered sources.
    """

    registry = load_registry()

    sources = registry.get("sources", [])

    if not isinstance(sources, list):
        raise ValueError(
            "'registry.sources' must be a list"
        )

    return sources


def get_source(
    source_id: str,
) -> dict[str, Any] | None:
    """
    Find a source by source ID.
    """

    normalized_id = source_id.strip().lower()

    for source in load_sources():
        if source.get("source_id") == normalized_id:
            return source

    return None


def source_exists(
    source_id: str,
) -> bool:
    """
    Check whether a source exists.
    """

    return get_source(source_id) is not None


def get_enabled_sources() -> list[dict[str, Any]]:
    """
    Return sources that are enabled for collection.
    """

    return [
        source
        for source in load_sources()
        if source.get("enabled", False) is True
    ]


def get_sources_by_country(
    country_code: str,
) -> list[dict[str, Any]]:
    """
    Return sources covering a country.

    GLOBAL sources are considered applicable
    to every country.
    """

    normalized_code = country_code.strip().upper()

    matching_sources = []

    for source in load_sources():

        scope = [
            code.upper()
            for code in source.get(
                "country_scope",
                [],
            )
        ]

        if (
            "GLOBAL" in scope
            or normalized_code in scope
        ):
            matching_sources.append(source)

    return matching_sources


def get_sources_by_sector(
    sector_code: str,
) -> list[dict[str, Any]]:
    """
    Return sources covering a sector.

    GLOBAL sources are considered applicable
    to every sector.
    """

    normalized_code = sector_code.strip().lower()

    matching_sources = []

    for source in load_sources():

        scope = [
            code.lower()
            for code in source.get(
                "sector_scope",
                [],
            )
        ]

        if (
            "global" in scope
            or normalized_code in scope
        ):
            matching_sources.append(source)

    return matching_sources


def get_registry_version() -> str:
    """
    Return source registry version.
    """

    registry = load_registry()

    return str(
        registry.get(
            "version",
            "unknown",
        )
    )