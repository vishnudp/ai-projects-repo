from typing import Any

from app.sources.models import (
    CollectionConfig,
    Source,
)


def source_from_dict(
    data: dict[str, Any],
) -> Source:

    collection_data = data.get(
        "collection",
        {},
    )

    reliability_data = data.get(
        "reliability",
        {},
    )

    collection = CollectionConfig(
        method=str(
            collection_data.get(
                "method",
                "web",
            )
        ).lower(),

        base_url=collection_data.get(
            "base_url"
        ),

        rss_url=collection_data.get(
            "rss_url"
        ),

        api_url=collection_data.get(
            "api_url"
        ),
    )

    return Source(
        source_id=data["source_id"],
        name=data["name"],

        organization=data.get(
            "organization"
        ),

        source_type=data.get(
            "source_type"
        ),

        country_scope=[
            str(value).upper()
            for value in data.get(
                "country_scope",
                [],
            )
        ],

        sector_scope=[
            str(value).lower()
            for value in data.get(
                "sector_scope",
                [],
            )
        ],

        collection=collection,

        language=[
            str(value).lower()
            for value in data.get(
                "language",
                [],
            )
        ],

        publication_frequency=data.get(
            "publication_frequency"
        ),

        reliability_tier=reliability_data.get(
            "tier"
        ),

        reliability_score=reliability_data.get(
            "score"
        ),

        enabled=bool(
            data.get(
                "enabled",
                False,
            )
        ),

        metadata={
            "registry_source": True,
        },
    )


def get_source(
    source_id: str,
) -> Source | None:

    from app.sources.registry import (
        get_source as registry_get_source,
    )

    data = registry_get_source(
        source_id
    )

    if data is None:
        return None

    return source_from_dict(data)


def get_enabled_sources() -> list[Source]:

    from app.sources.registry import (
        get_enabled_sources as registry_get_enabled_sources,
    )

    return [
        source_from_dict(source)
        for source in registry_get_enabled_sources()
    ]
