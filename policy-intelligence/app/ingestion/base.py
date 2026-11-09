from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional


@dataclass
class RawDocument:
    """
    Common document representation returned by collectors.

    Collectors should only be responsible for collecting data.
    They should not perform policy classification or intelligence.
    """

    external_id: Optional[str] = None

    title: str = ""

    source_url: Optional[str] = None

    source_id: Optional[str] = None

    source_name: Optional[str] = None

    content: Optional[str] = None

    published_at: Optional[datetime] = None

    retrieved_at: Optional[datetime] = None

    metadata: dict[str, Any] = field(
        default_factory=dict
    )


@dataclass
class IngestionResult:
    """
    Result of processing a single raw document.
    """

    status: str

    document_id: Optional[str] = None

    external_id: Optional[str] = None

    message: str = ""

    duplicate: bool = False

    metadata: dict[str, Any] = field(
        default_factory=dict
    )