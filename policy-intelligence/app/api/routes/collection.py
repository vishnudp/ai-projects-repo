from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.ingestion.multi_source_controller import (
    MultiSourceCollectionController,
)


router = APIRouter(
    prefix="/collection",
    tags=["Collection"],
)


class CollectionRequest(BaseModel):

    source_ids: list[str] = Field(
        ...,
        min_length=1,
    )

    max_workers: int = Field(
        default=5,
        ge=1,
        le=20,
    )


@router.post("")
def collect(
    request: CollectionRequest,
):

    controller = MultiSourceCollectionController(
        max_workers=request.max_workers,
    )

    try:

        result = controller.collect(
            request.source_ids
        )

        return {
            "status": (
                "failed"
                if result.failed_sources
                == result.total_sources
                else "completed"
            ),

            "summary": {
                "total_sources":
                    result.total_sources,

                "successful_sources":
                    result.successful_sources,

                "failed_sources":
                    result.failed_sources,

                "total_documents":
                    result.total_documents,

                "duration_ms":
                    result.duration_ms,
            },

            "metrics":
                result.metrics,

            "errors":
                result.errors,

        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )