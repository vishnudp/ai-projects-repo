from dataclasses import dataclass, field
from typing import Any


@dataclass
class CollectionConfig:
    method: str
    base_url: str | None = None
    rss_url: str | None = None
    api_url: str | None = None


@dataclass
class Source:
    source_id: str
    name: str
    organization: str | None = None
    source_type: str | None = None

    country_scope: list[str] = field(default_factory=list)
    sector_scope: list[str] = field(default_factory=list)

    collection: CollectionConfig | None = None

    language: list[str] = field(default_factory=list)

    publication_frequency: str | None = None

    reliability_tier: int | None = None
    reliability_score: float | None = None

    enabled: bool = True

    metadata: dict[str, Any] = field(
        default_factory=dict
    )
