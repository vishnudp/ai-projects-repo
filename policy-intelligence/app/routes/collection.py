from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.ingestion.multi_source_controller import (
    MultiSourceCollectionController,
)


router = APIRouter(
    prefix="/collection",
    tags=["Collection"],
)


# =========================================================
# Request Model
# =========================================================

class CollectionRequest(BaseModel):
    """
    Collection request.

    Example:

        {
            "source_ids": [
                "oecd",
                "who",
                "world_bank"
            ]
        }
    """

    source_ids: list[str] = Field(
        default_factory=list
    )


# =========================================================
# Candidate Serialization
# =========================================================

def _serialize_candidate(
    filter_result,
) -> dict[str, Any]:
    """
    Serialize a DataflowFilterResult.

    This exposes the actual candidate information
    required by the UI.

    Collection remains responsible only for discovery
    and filtering. Dataset retrieval comes later.
    """

    document = (
        filter_result.document
    )

    metadata = (
        document.metadata
        or {}
    )

    return {
        # -------------------------------------------------
        # Document identity
        # -------------------------------------------------

        "external_id": (
            document.external_id
        ),

        "title": (
            document.title
        ),

        # -------------------------------------------------
        # Source
        # -------------------------------------------------

        "source_id": (
            metadata.get(
                "source_id"
            )
            or metadata.get(
                "source"
            )
        ),

        "source_url": (
            document.source_url
        ),

        # -------------------------------------------------
        # SDMX metadata
        # -------------------------------------------------

        "dataflow_id": (
            metadata.get(
                "dataflow_id"
            )
        ),

        "agency_id": (
            metadata.get(
                "agency_id"
            )
        ),

        "version": (
            metadata.get(
                "version"
            )
        ),

        # -------------------------------------------------
        # Country metadata
        #
        # This may be [] during Wave 2 because the
        # discovered dataflow itself may not contain
        # country dimensions.
        # -------------------------------------------------

        "countries": (
            metadata.get(
                "countries",
                []
            )
        ),

        # -------------------------------------------------
        # Filter results
        # -------------------------------------------------

        "matched_countries": (
            filter_result.matched_countries
        ),

        "matched_sectors": (
            filter_result.matched_sectors
        ),

        "matched_terms": (
            filter_result.matched_terms
        ),

        "relevance_score": (
            filter_result.score
        ),

        "reasons": (
            filter_result.reasons
        ),
    }


# =========================================================
# Source Serialization
# =========================================================

def _serialize_collection_result(
    result,
) -> dict[str, Any]:
    """
    Serialize one source CollectionResult.
    """

    return {
        "source_id": (
            result.source_id
        ),

        "collector": (
            result.collector_type
        ),

        "discovered": (
            result.discovered
        ),

        "candidates": (
            result.candidates
        ),

        "selected": (
            result.selected
        ),

        "retrieved": (
            result.retrieved
        ),

        "duration_ms": (
            result.duration_ms
        ),

        # -------------------------------------------------
        # Counts
        # -------------------------------------------------

        "documents": len(
            result.documents
        ),

        "candidate_count": len(
            result.candidate_documents
        ),

        # -------------------------------------------------
        # Actual candidate objects
        # -------------------------------------------------

        "candidate_documents": [
            _serialize_candidate(
                candidate
            )
            for candidate
            in result.candidate_documents
        ],

        # -------------------------------------------------
        # Errors
        # -------------------------------------------------

        "errors": (
            result.errors
        ),
    }


# =========================================================
# Collection Endpoint
# =========================================================

@router.post(
    "",
)
def collect(
    request: CollectionRequest,
) -> dict[str, Any]:
    """
    Execute collection for requested sources.

    Wave 2 flow:

        Source
          ↓
        Discovery
          ↓
        Source-specific filtering
          ↓
        Candidate Dataflows
          ↓
        Dataset retrieval
              [NEXT]

    The endpoint currently performs collection and
    candidate selection only.
    """

    # =====================================================
    # Validate request
    # =====================================================

    source_ids = [
        source_id.strip().lower()
        for source_id
        in request.source_ids
        if source_id
        and source_id.strip()
    ]

    # Remove duplicates

    source_ids = list(
        dict.fromkeys(
            source_ids
        )
    )

    if not source_ids:

        return {
            "status": "no_sources",

            "requested_sources": 0,

            "successful_sources": 0,

            "failed_sources": 0,

            "discovered": 0,

            "candidates": 0,

            "selected": 0,

            "retrieved": 0,

            "duration_ms": 0,

            "sources": [],

            "errors": {},
        }

    # =====================================================
    # Controller
    # =====================================================

    controller = (
        MultiSourceCollectionController(
            max_workers=min(
                5,
                len(source_ids),
            )
        )
    )

    # =====================================================
    # Execute
    # =====================================================

    result = (
        controller.collect_sources(
            source_ids
        )
    )

    # =====================================================
    # Serialize source results
    # =====================================================

    source_results = [
        _serialize_collection_result(
            collection_result
        )
        for collection_result
        in result.source_results.values()
    ]

    # =====================================================
    # Determine status
    # =====================================================

    if (
        result.failed_sources
        == result.requested_sources
    ):

        status = "failed"

    elif result.failed_sources > 0:

        status = "partial"

    else:

        status = "completed"

    # =====================================================
    # Response
    # =====================================================

    return {
        "status": status,

        "requested_sources": (
            result.requested_sources
        ),

        "successful_sources": (
            result.successful_sources
        ),

        "failed_sources": (
            result.failed_sources
        ),

        # -------------------------------------------------
        # Aggregated metrics
        # -------------------------------------------------

        "discovered": (
            result.discovered
        ),

        "candidates": (
            result.candidates
        ),

        "selected": (
            result.selected
        ),

        "retrieved": (
            result.retrieved
        ),

        "duration_ms": (
            result.duration_ms
        ),

        # -------------------------------------------------
        # Per-source details
        # -------------------------------------------------

        "sources": source_results,

        # -------------------------------------------------
        # Errors
        # -------------------------------------------------

        "errors": (
            result.errors
        ),
    }