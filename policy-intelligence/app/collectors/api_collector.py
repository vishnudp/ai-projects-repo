from app.collectors.base import BaseCollector
from app.ingestion.base import RawDocument


class APICollector(BaseCollector):
    """
    Collector for API-based sources.

    Real API integration will be added later.
    """

    def collect(self) -> list[RawDocument]:

        documents: list[RawDocument] = []

        # Real API collection will be implemented
        # in the API collection stage.

        return self._validate_documents(
            documents
        )