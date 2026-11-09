from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Document:
    """
    Canonical document domain model.

    A document is the primary unit of policy intelligence.
    Source metadata describes provenance; document-level
    classification is determined independently.
    """

    document_id: str
    external_id: Optional[str] = None

    source_id: Optional[str] = None

    title: str = ""
    source_url: Optional[str] = None
    source_name: Optional[str] = None

    content: Optional[str] = None

    published_at: Optional[datetime] = None
    retrieved_at: Optional[datetime] = None

    content_hash: Optional[str] = None

    # Document-level intelligence.
    #
    # These are intentionally multi-valued because one
    # document can apply to multiple countries/sectors/topics.
    countries: list[str] = field(default_factory=list)
    sectors: list[str] = field(default_factory=list)
    policy_domains: list[str] = field(default_factory=list)
    topics: list[str] = field(default_factory=list)

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
