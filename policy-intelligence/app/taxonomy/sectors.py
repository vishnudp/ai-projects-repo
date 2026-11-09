from pathlib import Path
from typing import Any

import yaml


BASE_DIR = Path(__file__).resolve().parents[2]

SECTORS_FILE = (
    BASE_DIR
    / "config"
    / "global"
    / "sectors.yaml"
)


def load_taxonomy() -> dict[str, Any]:
    """
    Load the complete global policy taxonomy.
    """

    if not SECTORS_FILE.exists():
        raise FileNotFoundError(
            f"Taxonomy configuration not found: {SECTORS_FILE}"
        )

    with SECTORS_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        data = yaml.safe_load(file) or {}

    taxonomy = data.get("taxonomy")

    if not isinstance(taxonomy, dict):
        raise ValueError(
            "'taxonomy' must be an object"
        )

    return taxonomy


def load_sectors() -> list[dict[str, Any]]:
    """
    Return all taxonomy nodes.
    """

    taxonomy = load_taxonomy()

    sectors = taxonomy.get("sectors", [])

    if not isinstance(sectors, list):
        raise ValueError(
            "'taxonomy.sectors' must be a list"
        )

    return sectors


def get_sector(
    code: str,
) -> dict[str, Any] | None:
    """
    Find a taxonomy node by code.
    """

    normalized_code = code.strip().lower()

    for sector in load_sectors():
        if sector.get("code") == normalized_code:
            return sector

    return None


def sector_exists(code: str) -> bool:
    """
    Check whether a taxonomy node exists.
    """

    return get_sector(code) is not None


def get_root_sectors() -> list[dict[str, Any]]:
    """
    Return top-level sectors.
    """

    return [
        sector
        for sector in load_sectors()
        if sector.get("parent") is None
    ]


def get_children(
    parent_code: str,
) -> list[dict[str, Any]]:
    """
    Return direct children of a taxonomy node.
    """

    normalized_code = parent_code.strip().lower()

    return [
        sector
        for sector in load_sectors()
        if sector.get("parent") == normalized_code
    ]


def get_parent(
    code: str,
) -> dict[str, Any] | None:
    """
    Return the parent taxonomy node.
    """

    sector = get_sector(code)

    if sector is None:
        return None

    parent_code = sector.get("parent")

    if parent_code is None:
        return None

    return get_sector(parent_code)


def get_descendants(
    parent_code: str,
) -> list[dict[str, Any]]:
    """
    Return all descendants of a taxonomy node.
    """

    descendants = []

    children = get_children(parent_code)

    for child in children:
        descendants.append(child)

        descendants.extend(
            get_descendants(child["code"])
        )

    return descendants


def get_sector_codes() -> list[str]:
    """
    Return all taxonomy codes.
    """

    return [
        sector["code"]
        for sector in load_sectors()
        if sector.get("code")
    ]


def get_taxonomy_version() -> str:
    """
    Return taxonomy version.
    """

    taxonomy = load_taxonomy()

    return str(
        taxonomy.get("version", "unknown")
    )