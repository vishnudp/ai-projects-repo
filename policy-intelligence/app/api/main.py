from fastapi import FastAPI

from app.core.logging import configure_logging
from app.core.metrics import metrics
from app.core.progress import progress_state
from app.db.database import (
    database_health,
    initialize_database,
)
from app.llm.ollama_client import ollama_client
from app.routes.sources import (
    router as sources_router,
)

from app.routes.collection import (
    router as collection_router,
)

# ---------------------------------------------------------
# Logging
# ---------------------------------------------------------

configure_logging()


# ---------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------

app = FastAPI(
    title="Global Policy Intelligence",
    description=(
        "AI-powered global policy intelligence and "
        "knowledge digest platform."
    ),
    version="0.1.0",
)

app.include_router(
    sources_router
)

app.include_router(
    collection_router
)

# ---------------------------------------------------------
# Startup
# ---------------------------------------------------------

@app.on_event("startup")
def startup() -> None:
    initialize_database()


# ---------------------------------------------------------
# Health
# ---------------------------------------------------------

@app.get("/health")
def health() -> dict:

    # ---------------------------------------------
    # Ollama
    # ---------------------------------------------

    try:
        models = ollama_client.list_models()

        ollama_status = "connected"

    except Exception as exc:

        models = []

        ollama_status = (
            f"error: {type(exc).__name__}"
        )

    # ---------------------------------------------
    # Database
    # ---------------------------------------------

    try:

        database = database_health()

    except Exception as exc:

        database = {
            "status": (
                f"error: {type(exc).__name__}"
            )
        }

    # ---------------------------------------------
    # Response
    # ---------------------------------------------

    return {
        "status": "ok",

        "database": database,

        "ollama": {
            "status": ollama_status,
            "models": models,
        },

        "progress": (
            progress_state.snapshot()
        ),

        "metrics": (
            metrics.snapshot()
        ),
    }


# ---------------------------------------------------------
# Root
# ---------------------------------------------------------

@app.get("/")
def root() -> dict:

    return {
        "application": (
            "Global Policy Intelligence"
        ),
        "version": "0.1.0",
        "status": "running",
    }