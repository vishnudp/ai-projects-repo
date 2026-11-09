import httpx
import streamlit as st


st.set_page_config(
    page_title="Global Policy Intelligence",
    page_icon="🌍",
    layout="wide",
)


API_URL = "http://localhost:8000"


st.title(
    "🌍 Global Policy Intelligence"
)

st.caption(
    "Global Policy Intelligence Platform"
)


# ---------------------------------------------------------
# API Health
# ---------------------------------------------------------

def get_health() -> dict:

    response = httpx.get(
        f"{API_URL}/health",
        timeout=10,
    )

    response.raise_for_status()

    return response.json()


# ---------------------------------------------------------
# System Status
# ---------------------------------------------------------

st.subheader(
    "System Status"
)


if st.button(
    "Check System Health",
    type="primary",
):

    try:

        health = get_health()

        st.success(
            "Foundation services are responding."
        )

        col1, col2, col3 = st.columns(3)

        # -------------------------------------------------
        # API / Database
        # -------------------------------------------------

        with col1:

            st.metric(
                "API",
                "Connected",
            )

            st.metric(
                "Database",
                health["database"]["status"],
            )

        # -------------------------------------------------
        # Ollama
        # -------------------------------------------------

        with col2:

            st.metric(
                "Ollama",
                health["ollama"]["status"],
            )

            st.write(
                "**Available Models**"
            )

            for model in health["ollama"]["models"]:

                st.write(
                    f"• {model}"
                )

        # -------------------------------------------------
        # Cache Metrics
        # -------------------------------------------------

        with col3:

            counters = health[
                "metrics"
            ][
                "counters"
            ]

            st.metric(
                "LLM Cache Hits",
                counters.get(
                    "llm_cache_hits",
                    0,
                ),
            )

            st.metric(
                "Embedding Cache Hits",
                counters.get(
                    "embedding_cache_hits",
                    0,
                ),
            )

        # -------------------------------------------------
        # Pipeline Progress
        # -------------------------------------------------

        st.subheader(
            "Pipeline Progress"
        )

        progress = health.get(
            "progress",
            {},
        )

        progress_value = progress.get(
            "progress",
            0,
        )

        st.progress(
            progress_value / 100,
            text=(
                f"{progress.get('stage', 'unknown').upper()} — "
                f"{progress_value}% — "
                f"{progress.get('message', '')}"
            ),
        )

        # -------------------------------------------------
        # Runtime Metrics
        # -------------------------------------------------

        st.subheader(
            "Runtime Metrics"
        )

        st.json(
            health["metrics"]
        )

    except Exception as exc:

        st.error(
            "FastAPI is not reachable. "
            "Start it with: "
            "`uvicorn app.api.main:app --reload`"
        )

        st.exception(exc)

else:

    st.info(
        "Click **Check System Health** "
        "to validate the local foundation."
    )


st.divider()


# ---------------------------------------------------------
# Development Pipeline
# ---------------------------------------------------------

st.subheader(
    "Development Pipeline"
)


waves = [
    (
        "Wave 1",
        "Foundation & Local AI Infrastructure",
        "Completed",
    ),
    (
        "Wave 2",
        "Source Registry & Collection",
        "In Progress",
    ),
    (
        "Wave 3",
        "Document Intelligence & Deduplication",
        "Next",
    ),
    (
        "Wave 4",
        "Embeddings + Vector Search + RAG",
        "Planned",
    ),
    (
        "Wave 5",
        "Knowledge Graph + Claims + Relationships",
        "Planned",
    ),
    (
        "Wave 6",
        "Discovery + Trends + Country Benchmarking",
        "Planned",
    ),
    (
        "Wave 7",
        "Evidence + Outcomes + Transferability",
        "Planned",
    ),
    (
        "Wave 8",
        "Policy Options + Impact/Risk Analysis",
        "Planned",
    ),
    (
        "Wave 9",
        "Policy Digest + Editorial + Human Review",
        "Planned",
    ),
    (
        "Wave 10",
        "End-to-End Orchestration + Metrics + Demo",
        "Planned",
    ),
]


for wave, description, status in waves:

    col1, col2, col3 = st.columns(
        [1, 5, 2]
    )

    with col1:

        st.write(
            f"**{wave}**"
        )

    with col2:

        st.write(
            description
        )

    with col3:

        if status == "Completed":

            st.success(
                status
            )

        elif status == "In Progress":

            st.info(
                status
            )

        elif status == "Next":

            st.warning(
                status
            )

        else:

            st.write(
                status
            )
