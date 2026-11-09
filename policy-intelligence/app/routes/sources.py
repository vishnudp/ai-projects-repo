from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.collection.multi_source_controller import (
    MultiSourceCollectionController,
)
from app.sources.registry import (
    get_enabled_sources,
    get_registry_version,
)


router = APIRouter(
    prefix="/sources",
    tags=["Sources"],
)


# ---------------------------------------------------------
# Request Schema
# ---------------------------------------------------------

class CollectionRequest(BaseModel):

    source_ids: list[str]


# ---------------------------------------------------------
# Source Registry
# ---------------------------------------------------------

@router.get("")
def list_sources() -> dict[str, Any]:

    sources = get_enabled_sources()

    return {
        "registry_version": get_registry_version(),
        "count": len(sources),
        "sources": sources,
    }


# ---------------------------------------------------------
# Multi-source Collection
# ---------------------------------------------------------

@router.post("/collect")
def collect_sources(
    request: CollectionRequest,
) -> dict[str, Any]:

    if not request.source_ids:

        raise HTTPException(
            status_code=400,
            detail="At least one source_id is required.",
        )

    controller = (
        MultiSourceCollectionController(
            max_workers=min(
                5,
                len(request.source_ids),
            )
        )
    )

    result = controller.collect(
        request.source_ids
    )

    return {
        "total_sources": (
            result.total_sources
        ),
        "successful_sources": (
            result.successful_sources
        ),
        "failed_sources": (
            result.failed_sources
        ),
        "total_documents": (
            result.total_documents
        ),
        "duration_ms": (
            result.duration_ms
        ),
        "metrics": result.metrics,
        "results": [
            {
                "source_id": item.source_id,
                "collector_type": (
                    item.collector_type
                ),
                "collected": item.collected,
                "duration_ms": getattr(
                    item,
                    "duration_ms",
                    0.0,
                ),
                "errors": item.errors,
            }
            for item in result.results
        ],
        "errors": result.errors,
    }
