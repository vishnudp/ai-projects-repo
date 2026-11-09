from app.ingestion.base import RawDocument
from app.db.repositories.document_repository import DocumentRepository


class DocumentDeduplicator:

    def __init__(
        self,
        document_repository: DocumentRepository | None = None,
    ):
        self.document_repository = (
            document_repository
            or DocumentRepository()
        )

        # Batch-level duplicate detection.
        #
        # These sets prevent duplicates within
        # the same ingestion execution.
        self._seen_external_ids: set[str] = set()
        self._seen_content_hashes: set[str] = set()

    def is_duplicate(
        self,
        document: RawDocument,
    ) -> bool:

        external_id = document.external_id

        content_hash = (
            document.metadata.get("content_hash")
            if document.metadata
            else None
        )

        # -------------------------------------------------
        # 1. Batch-level external ID check
        # -------------------------------------------------

        if (
            external_id
            and external_id in self._seen_external_ids
        ):
            return True

        # -------------------------------------------------
        # 2. Batch-level content hash check
        # -------------------------------------------------

        if (
            content_hash
            and content_hash in self._seen_content_hashes
        ):
            return True

        # -------------------------------------------------
        # 3. Persistent database external ID check
        # -------------------------------------------------

        if (
            external_id
            and self.document_repository.exists_by_external_id(
                external_id
            )
        ):
            return True

        # -------------------------------------------------
        # 4. Persistent database content hash check
        # -------------------------------------------------

        if (
            content_hash
            and self.document_repository.exists_by_content_hash(
                content_hash
            )
        ):
            return True

        # -------------------------------------------------
        # 5. Remember for current batch
        # -------------------------------------------------

        if external_id:
            self._seen_external_ids.add(
                external_id
            )

        if content_hash:
            self._seen_content_hashes.add(
                content_hash
            )

        return False