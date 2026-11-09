from abc import ABC, abstractmethod
from typing import Any

from app.ingestion.base import RawDocument


class BaseCollector(ABC):
    """
    Base contract for all document collectors.

    Collectors are responsible ONLY for acquiring
    raw source material and converting it into
    RawDocument objects.

    They must NOT:
        - classify sectors
        - classify countries
        - classify topics
        - classify policy domains
        - calculate relevance
        - deduplicate documents
        - persist documents
        - call LLMs
    """

    def __init__(
        self,
        source_id: str,
        config: dict[str, Any] | None = None,
    ) -> None:

        if not source_id or not source_id.strip():
            raise ValueError(
                "source_id is required"
            )

        self.source_id = source_id.strip().lower()
        self.config = config or {}

    @abstractmethod
    def collect(self) -> list[RawDocument]:
        """
        Collect documents from the configured source.

        Contract:
            - Return list[RawDocument]
            - Never persist documents
            - Never classify documents
            - Never perform deduplication
        """
        raise NotImplementedError

    def _validate_documents(
        self,
        documents: list[RawDocument],
    ) -> list[RawDocument]:
        """
        Validate collector output.

        This validates the collector contract only.
        It does not perform business classification.
        """

        if not isinstance(documents, list):
            raise TypeError(
                f"{type(self).__name__}.collect() "
                "must return list[RawDocument]"
            )

        for document in documents:

            if not isinstance(document, RawDocument):
                raise TypeError(
                    f"{type(self).__name__}.collect() "
                    "returned an invalid object: "
                    f"{type(document).__name__}"
                )

            # Ensure source identity is always available.
            if not document.source_id:
                document.source_id = self.source_id

            if document.source_id != self.source_id:
                raise ValueError(
                    "RawDocument source_id does not match "
                    f"collector source_id: "
                    f"{document.source_id} != {self.source_id}"
                )

        return documents