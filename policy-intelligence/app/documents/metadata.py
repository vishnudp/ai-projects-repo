from app.ingestion.base import RawDocument


def extract_metadata(
    document: RawDocument,
) -> dict:

    metadata = dict(
        document.metadata or {}
    )

    metadata.update(
        {
            "source_id": document.source_id,
            "source_name": document.source_name,
            "source_url": document.source_url,
            "external_id": document.external_id,
            "title": document.title,
        }
    )

    return metadata