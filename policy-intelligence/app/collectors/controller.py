from dataclasses import dataclass, field

from app.collectors.base import BaseCollector
from app.collectors.factory import create_collector_from_source
from app.ingestion.base import RawDocument


@dataclass
class CollectionResult:
    """
    Result of a collection operation.

    This represents COLLECTION only.

    Persistence, normalization, deduplication and
    classification are handled by downstream stages.
    """

    source_id: str

    collector_type: str

    collected: int = 0

    documents: list[RawDocument] = field(
        default_factory=list
    )

    errors: list[str] = field(
        default_factory=list
    )


class CollectionController:
    """
    Orchestrates source collection.

    Flow:

        Source Registry
              ↓
        Collector Factory
              ↓
        Collector
              ↓
        RawDocument[]

    This controller does NOT:
        - normalize documents
        - extract metadata
        - deduplicate
        - persist
        - classify countries
        - classify sectors
        - discover sectors
        - classify topics
        - classify policy domains
        - calculate relevance
        - call LLMs
    """

    def collect(
        self,
        source_id: str,
    ) -> CollectionResult:

        collector: BaseCollector = (
            create_collector_from_source(
                source_id
            )
        )

        try:
            documents = collector.collect()

        except Exception as exc:
            return CollectionResult(
                source_id=source_id,
                collector_type=type(collector).__name__,
                collected=0,
                documents=[],
                errors=[
                    f"{type(exc).__name__}: {exc}"
                ],
            )

        if not isinstance(documents, list):
            raise TypeError(
                "Collector must return "
                "list[RawDocument]"
            )

        for document in documents:

            if not isinstance(
                document,
                RawDocument,
            ):
                raise TypeError(
                    "Collector returned an "
                    "invalid document type: "
                    f"{type(document).__name__}"
                )

        return CollectionResult(
            source_id=source_id,
            collector_type=type(
                collector
            ).__name__,
            collected=len(documents),
            documents=documents,
        )
