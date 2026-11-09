from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Source:
    """
    Canonical source domain model.

    Source scope is used for collection/discovery.
    It must NOT be treated as document classification.
    """

    source_id: str

    name: str = ""

    organization: Optional[str] = None
    source_type: Optional[str] = None

    url: Optional[str] = None

    # Collection/discovery hints.
    #
    # These do NOT determine the classification of
    # individual documents collected from the source.
    country_scope: list[str] = field(default_factory=list)
    sector_scope: list[str] = field(default_factory=list)

    collection_methods: list[str] = field(default_factory=list)

    reliability: Optional[float] = None

    enabled: bool = True

    metadata: dict = field(default_factory=dict)
