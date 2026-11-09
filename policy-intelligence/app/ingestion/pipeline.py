from dataclasses import dataclass, field

from app.ingestion.controller import (
    IngestionController,
    IngestionResult,
)
from app.ingestion.collection_controller import (
    CollectionController,
    CollectionResult,
)


@dataclass
class PipelineResult:

    source_id: str

    collection: CollectionResult

    ingestion: IngestionResult | None = None

    errors: list[str] = field(
        default_factory=list
    )


class IngestionPipeline:

    def __init__(
        self,
        collection_controller=None,
        ingestion_controller=None,
    ):

        self.collection_controller = (
            collection_controller
            or CollectionController()
        )

        self.ingestion_controller = (
            ingestion_controller
            or IngestionController()
        )

    def run(
        self,
        source_id: str,
    ) -> PipelineResult:

        collection = (
            self.collection_controller.collect(
                source_id
            )
        )

        if collection.errors:

            return PipelineResult(
                source_id=source_id,
                collection=collection,
                ingestion=None,
                errors=collection.errors,
            )

        ingestion = (
            self.ingestion_controller.ingest(
                source_id=source_id,
                raw_documents=collection.documents,
            )
        )

        return PipelineResult(
            source_id=source_id,
            collection=collection,
            ingestion=ingestion,
        )