from pathlib import Path
from typing import Any

import yaml


BASE_DIR = Path(__file__).resolve().parents[2]
COUNTRIES_FILE = BASE_DIR / "config" / "countries.yaml"


def load_countries() -> list[dict[str, Any]]:
    if not COUNTRIES_FILE.exists():
        raise FileNotFoundError(
            f"Countries configuration not found: {COUNTRIES_FILE}"
        )

    with COUNTRIES_FILE.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}

    countries = data.get("countries", [])

    if not isinstance(countries, list):
        raise ValueError(
            "'countries' must be a list"
        )

    return countries


def get_country(code: str) -> dict[str, Any] | None:
    code = code.upper()

    for country in load_countries():
        if country.get("code") == code:
            return country

    return None


def get_enabled_countries() -> list[dict[str, Any]]:
    return [
        country
        for country in load_countries()
        if country.get("enabled", False)
    ]