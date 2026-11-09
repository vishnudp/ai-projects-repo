from app.documents.deduplicator import (
    DocumentDeduplicator,
)
from app.documents.metadata import (
    extract_metadata,
)
from app.documents.normalizer import (
    normalize_document,
)
from app.ingestion.base import RawDocument


def main():

    raw = RawDocument(
        external_id="test-001",
        source_id="test-oecd",
        source_name="Test OECD",
        title="   Global AI Policy   ",
        source_url="https://example.org/test",
        content="""
            Artificial intelligence policy
            is becoming increasingly important.
        """,
    )

    print("RAW DOCUMENT:")
    print(raw)

    normalized = normalize_document(raw)

    print()
    print("NORMALIZED:")
    print(normalized)

    metadata = extract_metadata(
        normalized
    )

    print()
    print("METADATA:")
    print(metadata)

    deduplicator = DocumentDeduplicator()

    first = deduplicator.is_duplicate(
        normalized
    )

    second = deduplicator.is_duplicate(
        normalized
    )

    print()
    print("FIRST DUPLICATE CHECK:", first)
    print("SECOND DUPLICATE CHECK:", second)

    assert normalized.title == (
        "Global AI Policy"
    )

    assert normalized.content == (
        "Artificial intelligence policy "
        "is becoming increasingly important."
    )

    assert normalized.metadata.get(
        "content_hash"
    )

    assert first is False
    assert second is True

    print()
    print("INGESTION CONTRACT TEST: OK")


if __name__ == "__main__":
    main()