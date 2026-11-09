from app.collectors.base import BaseCollector
from app.ingestion.base import RawDocument


class SearchCollector(BaseCollector):
    """
    Collector for search-based discovery.

    Real search integration will be added later.
    """

    def collect(self) -> list[RawDocument]:

        documents: list[RawDocument] = []

        # Real search integration will be implemented
        # in the search collection stage.

        return self._validate_documents(
            documents
        )