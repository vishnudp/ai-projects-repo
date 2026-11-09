from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed,
)

from dataclasses import dataclass, field

from time import perf_counter

from app.ingestion.collection_controller import (
    CollectionController,
    CollectionResult,
)

from app.sources.registry import (
    get_enabled_sources,
)


# =========================================================
# Multi Source Collection Result
# =========================================================

@dataclass
class MultiSourceCollectionResult:
    """
    Aggregated result of collecting from multiple sources.

    Wave 2 collection metrics:

        requested_sources
        successful_sources
        failed_sources

        discovered
        candidates
        selected
        retrieved

        duration_ms

    This represents COLLECTION only.

    It does not perform:

        - normalization
        - metadata extraction
        - deduplication
        - persistence
        - classification
        - LLM processing
        - scheduling
    """

    # -----------------------------------------------------
    # Source metrics
    # -----------------------------------------------------

    requested_sources: int = 0

    successful_sources: int = 0

    failed_sources: int = 0

    # -----------------------------------------------------
    # Collection metrics
    # -----------------------------------------------------

    discovered: int = 0

    candidates: int = 0

    selected: int = 0

    retrieved: int = 0

    # -----------------------------------------------------
    # Per-source results
    # -----------------------------------------------------

    source_results: dict[
        str,
        CollectionResult
    ] = field(
        default_factory=dict
    )

    # -----------------------------------------------------
    # Errors
    # -----------------------------------------------------

    errors: dict[
        str,
        str
    ] = field(
        default_factory=dict
    )

    # -----------------------------------------------------
    # Execution timing
    # -----------------------------------------------------

    duration_ms: float = 0.0


# =========================================================
# Multi Source Collection Controller
# =========================================================

class MultiSourceCollectionController:
    """
    Collect documents from multiple sources in parallel.

    Flow:

        Source Registry
              ↓
        Enabled Sources
              ↓
        MultiSourceCollectionController
              ↓
        CollectionController
              ↓
        Collector Factory
              ↓
        Individual Collector
              ↓
        CollectionResult

    This controller does NOT:

        - normalize documents
        - extract metadata
        - deduplicate
        - persist documents
        - classify documents
        - call LLMs
        - schedule jobs
    """

    def __init__(
        self,
        max_workers: int = 5,
        collection_controller=None,
    ) -> None:

        if max_workers < 1:

            raise ValueError(
                "max_workers must be >= 1"
            )

        self.max_workers = max_workers

        self.collection_controller = (
            collection_controller
            or CollectionController()
        )

    # =====================================================
    # Enabled Sources
    # =====================================================

    def collect_enabled_sources(
        self,
    ) -> MultiSourceCollectionResult:
        """
        Collect all currently enabled sources.
        """

        sources = get_enabled_sources()

        source_ids = [
            source["source_id"]
            for source in sources
            if source.get("source_id")
        ]

        return self.collect_sources(
            source_ids
        )

    # =====================================================
    # Collect Sources
    # =====================================================

    def collect_sources(
        self,
        source_ids: list[str],
    ) -> MultiSourceCollectionResult:
        """
        Collect multiple sources in parallel.

        A failure in one source does not stop
        the remaining sources.
        """

        started = perf_counter()

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
        # Remove duplicates while preserving order
        # -------------------------------------------------

        normalized_source_ids = list(
            dict.fromkeys(
                normalized_source_ids
            )
        )

        result = MultiSourceCollectionResult(
            requested_sources=len(
                normalized_source_ids
            )
        )

        # -------------------------------------------------
        # No sources
        # -------------------------------------------------

        if not normalized_source_ids:

            result.duration_ms = round(
                (
                    perf_counter()
                    - started
                )
                * 1000,
                2,
            )

            return result

        # -------------------------------------------------
        # Worker count
        # -------------------------------------------------

        worker_count = min(
            self.max_workers,
            len(
                normalized_source_ids
            ),
        )

        # -------------------------------------------------
        # Parallel collection
        # -------------------------------------------------

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

            for future in as_completed(
                futures
            ):

                source_id = futures[
                    future
                ]

                try:

                    collection_result = (
                        future.result()
                    )

                    # -------------------------------------
                    # Store source result
                    # -------------------------------------

                    result.source_results[
                        source_id
                    ] = collection_result

                    # -------------------------------------
                    # Aggregate Wave 2 metrics
                    # -------------------------------------

                    result.discovered += (
                        collection_result.discovered
                    )

                    result.candidates += (
                        collection_result.candidates
                    )

                    result.selected += (
                        collection_result.selected
                    )

                    result.retrieved += (
                        collection_result.retrieved
                    )

                    # -------------------------------------
                    # Source success / failure
                    # -------------------------------------

                    if collection_result.errors:

                        result.failed_sources += 1

                        result.errors[
                            source_id
                        ] = "; ".join(
                            collection_result.errors
                        )

                    else:

                        result.successful_sources += 1

                # -----------------------------------------
                # Failure isolation
                # -----------------------------------------

                except Exception as exc:

                    result.failed_sources += 1

                    result.errors[
                        source_id
                    ] = (
                        f"{type(exc).__name__}: "
                        f"{exc}"
                    )

        # -------------------------------------------------
        # Overall execution timing
        # -------------------------------------------------

        result.duration_ms = round(
            (
                perf_counter()
                - started
            )
            * 1000,
            2,
        )

        return result

    # =====================================================
    # Single Source
    # =====================================================

    def _collect_source(
        self,
        source_id: str,
    ) -> CollectionResult:
        """
        Collect one source.

        Executed inside a worker thread.
        """

        return (
            self.collection_controller.collect(
                source_id
            )
        )