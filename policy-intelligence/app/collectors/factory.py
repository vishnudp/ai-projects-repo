from typing import Any

from app.sources.registry import get_source

from app.collectors.base import BaseCollector
from app.collectors.web_collector import WebCollector
from app.collectors.rss_collector import RSSCollector
from app.collectors.api_collector import APICollector
from app.collectors.search_collector import SearchCollector
from app.collectors.sdmx_collector import (
    SDMXCollector,
)

COLLECTOR_TYPES = {
    "web": WebCollector,
    "rss": RSSCollector,
    "api": APICollector,
    "search": SearchCollector,
    "sdmx": SDMXCollector,
}


def create_collector(
    source_id: str,
    config: dict[str, Any],
) -> BaseCollector:
    """
    Create a collector from an explicit source configuration.
    """

    collection = config.get("collection", {})

    method = collection.get("method")

    if not method:
        raise ValueError(
            f"Collection method not configured for source: {source_id}"
        )

    method = method.strip().lower()

    collector_class = COLLECTOR_TYPES.get(method)

    if collector_class is None:
        raise ValueError(
            f"Unsupported collection method '{method}' "
            f"for source '{source_id}'"
        )

    return collector_class(
        source_id=source_id,
        config=config,
    )


def create_collector_from_source(
    source_id: str,
) -> BaseCollector:
    """
    Create a collector directly from the global source registry.
    """

    normalized_source_id = source_id.strip().lower()

    source = get_source(normalized_source_id)

    if source is None:
        raise ValueError(
            f"Source not found in registry: {normalized_source_id}"
        )

    if source.get("enabled") is not True:
        raise ValueError(
            f"Source is disabled: {normalized_source_id}"
        )

    return create_collector(
        source_id=normalized_source_id,
        config=source,
    )