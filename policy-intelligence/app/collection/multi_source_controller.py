import time

from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed,
)

from dataclasses import dataclass, field
from typing import Any

from app.collection.collection_controller import (
    CollectionController,
)
from app.ingestion.base import RawDocument

from app.core.progress import (
    JobStage,
    progress_state,
)

@dataclass
class MultiSourceCollectionResult:
    """
    Aggregated result of collecting from multiple sources.
    """

    total_sources: int = 0

    successful_sources: int = 0

    failed_sources: int = 0

    # Discovery
    total_documents: int = 0

    total_discovered: int = 0

    # Relevance filtering
    total_candidates: int = 0

    # Future stages
    total_selected: int = 0

    total_retrieved: int = 0

    duration_ms: float = 0.0

    metrics: dict[str, Any] = field(
        default_factory=dict
    )

    results: list = field(
        default_factory=list
    )

    errors: list[str] = field(
        default_factory=list
    )


class MultiSourceCollectionController:
    """
    Orchestrates collection across multiple sources.

    Each source is collected independently.

    Sources are processed in parallel.

    Flow:

        Source IDs
             ↓
        MultiSourceCollectionController
             ↓
        CollectionController
             ↓
        Collector Factory
             ↓
        Individual Collector
             ↓
        RawDocument[]

    This controller does NOT:
        - normalize documents
        - extract metadata
        - deduplicate
        - persist
        - classify
        - call LLMs
        - schedule jobs
    """

    def __init__(
        self,
        collection_controller: CollectionController | None = None,
        max_workers: int = 5,
    ) -> None:

        self.collection_controller = (
            collection_controller
            or CollectionController()
        )

        if max_workers < 1:
            raise ValueError(
                "max_workers must be at least 1"
            )

        self.max_workers = max_workers

    def collect(
        self,
        source_ids: list[str],
    ) -> MultiSourceCollectionResult:
        """
        Collect documents from multiple sources.

        Sources are collected in parallel.

        A failure in one source does not stop
        collection from other sources.
        """

        progress_state.update(
            JobStage.COLLECTING,
            0,
            "Starting multi-source collection",
        )

        start_time = time.perf_counter()

        result = MultiSourceCollectionResult()

        if not source_ids:
            return result

        # -------------------------------------------------
        # Normalize source IDs
        # -------------------------------------------------

        normalized_source_ids = [
            source_id.strip().lower()
            for source_id in source_ids
            if source_id
            and source_id.strip()
        ]

        # -------------------------------------------------
        # Remove duplicate source IDs while preserving
        # input order.
        # -------------------------------------------------

        normalized_source_ids = list(
            dict.fromkeys(
                normalized_source_ids
            )
        )

        result.total_sources = len(
            normalized_source_ids
        )

        if not normalized_source_ids:
            return result

        # -------------------------------------------------
        # Parallel collection
        # -------------------------------------------------

        worker_count = min(
            self.max_workers,
            len(normalized_source_ids),
        )

        with ThreadPoolExecutor(
            max_workers=worker_count
        ) as executor:

            futures = {
                executor.submit(
                    self._collect_source,
                    source_id,
                ): source_id
                for source_id in normalized_source_ids
            }
            completed_sources = 0

            for future in as_completed(
                futures
            ):


                

                completed_sources += 1

                progress_percent = (
                    completed_sources
                    / result.total_sources
                ) * 100

                progress_state.update(
                    JobStage.COLLECTING,
                    progress_percent,
                    (
                        f"Collected "
                        f"{completed_sources}/"
                        f"{result.total_sources} sources"
                    ),
                )

                source_id = futures[
                    future
                ]

                try:

                    collection_result = (
                        future.result()
                    )

                    result.results.append(
                        collection_result
                    )

                    result.total_discovered += (
                        collection_result.discovered
                    )

                    result.total_candidates += (
                        collection_result.candidates
                    )

                    result.total_selected += (
                        collection_result.selected
                    )

                    result.total_retrieved += (
                        collection_result.retrieved
                    )

                    result.total_documents = (
                        result.total_discovered
                    )
                    # -------------------------------------
                    # Source success / failure
                    # -------------------------------------

                    if collection_result.errors:

                        result.failed_sources += 1

                        for error in (
                            collection_result.errors
                        ):
                            result.errors.append(
                                f"{source_id}: {error}"
                            )

                    else:

                        result.successful_sources += 1

                except Exception as exc:

                    # -------------------------------------
                    # Failure isolation
                    #
                    # A failed source must not prevent
                    # other sources from completing.
                    # -------------------------------------

                    result.failed_sources += 1

                    result.errors.append(
                        f"{source_id}: "
                        f"{type(exc).__name__}: {exc}"
                    )

            if result.failed_sources == result.total_sources:
                progress_state.update(
                    JobStage.FAILED,
                    100,
                    "Collection failed for all requested sources",
                )
            else:
                progress_state.update(
                    JobStage.COMPLETED,
                    100,
                    (
                        f"Collection completed: "
                        f"{result.successful_sources}/"
                        f"{result.total_sources} sources successful"
                    ),
                )

        # -------------------------------------------------
        # Overall execution timing
        # -------------------------------------------------

        result.duration_ms = round(
            (
                time.perf_counter()
                - start_time
            )
            * 1000,
            2,
        )

        # -------------------------------------------------
        # Aggregated metrics
        # -------------------------------------------------

        result.metrics = {
            "total_sources": (
                result.total_sources
            ),

            "successful_sources": (
                result.successful_sources
            ),

            "failed_sources": (
                result.failed_sources
            ),

            "total_discovered": (
                result.total_discovered
            ),

            "total_candidates": (
                result.total_candidates
            ),

            "total_selected": (
                result.total_selected
            ),

            "total_retrieved": (
                result.total_retrieved
            ),

            "duration_ms": (
                result.duration_ms
            ),
        }

        return result

    def _collect_source(
        self,
        source_id: str,
    ):
        """
        Collect a single source.

        This method is executed inside a worker thread.
        """

        start_time = time.perf_counter()

        collection_result = (
            self.collection_controller.collect(
                source_id
            )
        )

        duration_ms = round(
            (
                time.perf_counter()
                - start_time
            )
            * 1000,
            2,
        )

        # CollectionResult is intentionally enriched
        # with execution timing here rather than putting
        # timing/orchestration logic inside collectors.

        collection_result.duration_ms = (
            duration_ms
        )

        return collection_result