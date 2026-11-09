from dataclasses import dataclass, field

from app.documents.deduplicator import DocumentDeduplicator
from app.documents.metadata import extract_metadata
from app.documents.normalizer import normalize_document
from app.db.models import Document
from app.db.repositories import DocumentRepository
from app.ingestion.base import RawDocument


@dataclass
class IngestionResult:
    source_id: str

    collected: int = 0
    normalized: int = 0
    inserted: int = 0
    duplicates: int = 0
    failed: int = 0

    errors: list[str] = field(default_factory=list)


class IngestionController:
    """
    Orchestrates the ingestion pipeline.

    Collector
        ↓
    RawDocument
        ↓
    Normalization
        ↓
    Metadata
        ↓
    Deduplication
        ↓
    Domain Document
        ↓
    Persistence

    Classification is intentionally NOT performed here.

    Country, sector, topic, policy-domain and relevance
    classification belong to downstream intelligence stages.
    """

    def __init__(
        self,
        document_repository: DocumentRepository | None = None,
        deduplicator: DocumentDeduplicator | None = None,
    ) -> None:

        self.document_repository = (
            document_repository
            or DocumentRepository()
        )

        self.deduplicator = (
            deduplicator
            or DocumentDeduplicator()
        )

    def ingest(
        self,
        source_id: str,
        raw_documents: list[RawDocument],
    ) -> IngestionResult:

        result = IngestionResult(
            source_id=source_id
        )

        for raw_document in raw_documents:

            result.collected += 1

            try:

                # -----------------------------------------
                # Ensure source identity
                # -----------------------------------------

                if not raw_document.source_id:
                    raw_document.source_id = source_id

                # -----------------------------------------
                # Normalize
                # -----------------------------------------

                normalized = normalize_document(
                    raw_document
                )

                result.normalized += 1

                # -----------------------------------------
                # Extract metadata
                # -----------------------------------------

                metadata = extract_metadata(
                    normalized
                )

                # -----------------------------------------
                # Deduplication
                # -----------------------------------------

                if self.deduplicator.is_duplicate(
                    normalized
                ):
                    result.duplicates += 1
                    continue

                # -----------------------------------------
                # Generate stable document ID
                # -----------------------------------------

                document_id = (
                    normalized.external_id
                    or metadata.get("content_hash")
                )

                if not document_id:
                    raise ValueError(
                        "Document requires either "
                        "external_id or content_hash"
                    )

                # -----------------------------------------
                # Convert RawDocument → Document
                # -----------------------------------------

                document = Document(
                    document_id=document_id,

                    external_id=(
                        normalized.external_id
                    ),

                    source_id=(
                        normalized.source_id
                    ),

                    title=(
                        normalized.title
                    ),

                    source_url=(
                        normalized.source_url
                    ),

                    source_name=(
                        normalized.source_name
                    ),

                    content=(
                        normalized.content
                    ),

                    published_at=(
                        normalized.published_at
                    ),

                    retrieved_at=(
                        normalized.retrieved_at
                    ),

                    content_hash=(
                        metadata.get("content_hash")
                    ),

                    # Classification intentionally
                    # remains empty at ingestion stage.
                    countries=[],
                    sectors=[],
                    policy_domains=[],
                    topics=[],
                )

                # -----------------------------------------
                # Persist
                # -----------------------------------------

                self.document_repository.create(
                    document
                )

                result.inserted += 1

            except Exception as exc:

                result.failed += 1

                result.errors.append(
                    f"{type(exc).__name__}: {exc}"
                )

        return result