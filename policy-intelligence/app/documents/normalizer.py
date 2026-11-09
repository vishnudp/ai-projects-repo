import hashlib
import re
from datetime import datetime, timezone

from app.ingestion.base import RawDocument


def _clean_text(value: str | None) -> str | None:
    if not value:
        return None

    value = re.sub(r"\s+", " ", value)

    return value.strip()


def _generate_content_hash(
    content: str | None,
) -> str | None:

    if not content:
        return None

    normalized = content.strip().lower()

    return hashlib.sha256(
        normalized.encode("utf-8")
    ).hexdigest()


def normalize_document(
    document: RawDocument,
) -> RawDocument:

    document.title = (
        _clean_text(document.title)
        or "Untitled document"
    )

    document.content = _clean_text(
        document.content
    )

    document.source_url = (
        document.source_url.strip()
        if document.source_url
        else None
    )

    document.source_name = (
        document.source_name.strip()
        if document.source_name
        else None
    )

    if document.retrieved_at is None:
        document.retrieved_at = datetime.now(
            timezone.utc
        )

    document.metadata = dict(
        document.metadata or {}
    )

    document.metadata[
        "content_hash"
    ] = _generate_content_hash(
        document.content
    )

    return document