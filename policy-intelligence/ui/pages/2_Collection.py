import httpx
import streamlit as st


# =========================================================
# Configuration
# =========================================================

API_URL = "http://localhost:8000"


st.set_page_config(
    page_title="Collection | Global Policy Intelligence",
    page_icon="🌍",
    layout="wide",
)


# =========================================================
# Helpers
# =========================================================

def get_health() -> dict:
    response = httpx.get(
        f"{API_URL}/health",
        timeout=10,
    )

    response.raise_for_status()

    return response.json()


def collect_sources(
    source_ids: list[str],
) -> dict:

    response = httpx.post(
        f"{API_URL}/collection",
        json={
            "source_ids": source_ids,
        },
        timeout=300,
    )

    response.raise_for_status()

    return response.json()


def get_sources() -> list[dict]:
    """
    Fetch source registry from FastAPI.

    If the endpoint is not available yet,
    return an empty list so the UI remains usable.
    """

    try:

        response = httpx.get(
            f"{API_URL}/sources",
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        if isinstance(data, list):
            return data

        if isinstance(data, dict):

            return data.get(
                "sources",
                [],
            )

        return []

    except Exception:

        return []


# =========================================================
# Header
# =========================================================

st.title(
    "🌍 Source & Collection"
)

st.caption(
    "Wave 2 — Source Registry & Collection"
)


# =========================================================
# System status
# =========================================================

st.subheader(
    "System Status"
)

try:

    health = get_health()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.success(
            "🟢 API Connected"
        )

    with col2:

        database_status = (
            health
            .get("database", {})
            .get("status", "unknown")
        )

        if database_status == "connected":

            st.success(
                "🟢 Database Connected"
            )

        else:

            st.warning(
                f"Database: {database_status}"
            )

    with col3:

        ollama_status = (
            health
            .get("ollama", {})
            .get("status", "unknown")
        )

        if ollama_status == "connected":

            st.success(
                "🟢 Ollama Connected"
            )

        else:

            st.warning(
                f"Ollama: {ollama_status}"
            )

except Exception as exc:

    st.error(
        "FastAPI is not reachable."
    )

    st.code(
        "uvicorn app.api.main:app --reload"
    )

    st.exception(exc)

    st.stop()


st.divider()


# =========================================================
# Source selection
# =========================================================

st.subheader(
    "1. Select Sources"
)


sources = get_sources()


# ---------------------------------------------------------
# Fallback
# ---------------------------------------------------------

if not sources:

    st.warning(
        "Source Registry endpoint did not return "
        "source metadata."
    )

    st.info(
        "Using configured source IDs as fallback."
    )

    source_options = [
        "oecd",
        "world_bank",
        "who",
        "imf",
    ]

    source_labels = {
        "oecd": "OECD",
        "world_bank": "World Bank",
        "who": "WHO",
        "imf": "IMF",
    }

    selected_sources = st.multiselect(
        "Sources",
        options=source_options,
        default=["oecd"],
        format_func=lambda x: source_labels.get(
            x,
            x,
        ),
    )

else:

    source_ids = []

    source_labels = {}

    for source in sources:

        source_id = source.get(
            "source_id"
        )

        if not source_id:
            continue

        source_ids.append(
            source_id
        )

        source_labels[source_id] = (
            source.get(
                "name",
                source_id,
            )
        )

    selected_sources = st.multiselect(
        "Sources",
        options=source_ids,
        default=(
            ["oecd"]
            if "oecd" in source_ids
            else source_ids[:1]
        ),
        format_func=lambda x: source_labels.get(
            x,
            x,
        ),
    )


if selected_sources:

    st.write(
        "**Selected:** "
        + ", ".join(
            source_labels.get(
                source_id,
                source_id,
            )
            for source_id in selected_sources
        )
    )

else:

    st.info(
        "Select at least one source."
    )


# =========================================================
# Collection execution
# =========================================================

st.subheader(
    "2. Execute Collection"
)


collect_clicked = st.button(
    "🚀 Start Collection",
    type="primary",
    disabled=not selected_sources,
    use_container_width=True,
)


if collect_clicked:

    st.session_state["collection_result"] = None

    progress_placeholder = st.empty()

    status_placeholder = st.empty()

    progress_placeholder.progress(
        0,
        text="Starting collection...",
    )

    status_placeholder.info(
        "Connecting to collection controller..."
    )

    try:

        result = collect_sources(
            selected_sources
        )

        progress_placeholder.progress(
            100,
            text="Collection completed",
        )

        status_placeholder.success(
            "Collection execution completed."
        )

        st.session_state[
            "collection_result"
        ] = result

    except httpx.HTTPStatusError as exc:

        progress_placeholder.empty()

        status_placeholder.error(
            "Collection API returned an error."
        )

        st.code(
            exc.response.text
        )

    except Exception as exc:

        progress_placeholder.empty()

        status_placeholder.error(
            "Collection failed."
        )

        st.exception(exc)


# =========================================================
# Results
# =========================================================

result = st.session_state.get(
    "collection_result"
)


if not result:

    st.divider()

    st.info(
        "Run a collection to see discovery, "
        "filtering and retrieval results."
    )

    st.stop()


st.divider()


# =========================================================
# Collection Summary
# =========================================================

st.subheader(
    "3. Collection Summary"
)


requested = result.get(
    "requested_sources",
    0,
)

successful = result.get(
    "successful_sources",
    0,
)

failed = result.get(
    "failed_sources",
    0,
)

discovered = result.get(
    "discovered",
    0,
)

candidates = result.get(
    "candidates",
    0,
)

selected = result.get(
    "selected",
    0,
)

retrieved = result.get(
    "retrieved",
    0,
)

duration = result.get(
    "duration_ms",
    0,
)


col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Sources",
        requested,
    )

with col2:

    st.metric(
        "Successful",
        successful,
    )

with col3:

    st.metric(
        "Failed",
        failed,
    )

with col4:

    st.metric(
        "Duration",
        f"{duration:,.0f} ms",
    )


# =========================================================
# Collection Funnel
# =========================================================

st.subheader(
    "4. Collection Funnel"
)


funnel_col1, funnel_col2, funnel_col3, funnel_col4 = (
    st.columns(4)
)


with funnel_col1:

    st.metric(
        "Discovered",
        f"{discovered:,}",
        help=(
            "Total artifacts discovered "
            "from source collectors."
        ),
    )


with funnel_col2:

    st.metric(
        "Candidates",
        f"{candidates:,}",
        help=(
            "Artifacts passing source-specific "
            "relevance filtering."
        ),
    )


with funnel_col3:

    st.metric(
        "Selected",
        f"{selected:,}",
        help=(
            "Artifacts selected for retrieval."
        ),
    )


with funnel_col4:

    st.metric(
        "Retrieved",
        f"{retrieved:,}",
        help=(
            "Documents successfully retrieved."
        ),
    )


# =========================================================
# Funnel visualization
# =========================================================

if discovered > 0:

    candidate_ratio = (
        candidates / discovered
    ) * 100

    selected_ratio = (
        selected / candidates * 100
        if candidates > 0
        else 0
    )

    retrieved_ratio = (
        retrieved / selected * 100
        if selected > 0
        else 0
    )

    st.write(
        f"Candidate rate: "
        f"**{candidate_ratio:.2f}%**"
    )

    st.progress(
        min(
            candidate_ratio / 100,
            1.0,
        ),
        text=(
            f"{candidates:,} / "
            f"{discovered:,} candidates"
        ),
    )

    if candidates > 0:

        st.write(
            f"Selection rate: "
            f"**{selected_ratio:.2f}%**"
        )

    if selected > 0:

        st.write(
            f"Retrieval rate: "
            f"**{retrieved_ratio:.2f}%**"
        )


# =========================================================
# Per-source results
# =========================================================

st.subheader(
    "5. Source Results"
)


source_results = result.get(
    "source_results",
    {},
)


for source_id, source_result in (
    source_results.items()
):

    source_name = source_labels.get(
        source_id,
        source_id.upper(),
    )

    errors = source_result.get(
        "errors",
        [],
    )

    if errors:

        status = "🔴 Failed"

    else:

        status = "🟢 Successful"

    with st.expander(
        f"{status}  {source_name}",
        expanded=True,
    ):

        col1, col2 = st.columns(
            [1, 1]
        )

        with col1:

            st.write(
                f"**Source ID:** `{source_id}`"
            )

            st.write(
                "**Collector:** "
                f"`{source_result.get('collector_type', 'unknown')}`"
            )

            st.metric(
                "Duration",
                f"{source_result.get('duration_ms', 0):,.0f} ms",
            )

        with col2:

            m1, m2 = st.columns(2)

            with m1:

                st.metric(
                    "Discovered",
                    f"{source_result.get('discovered', 0):,}",
                )

                st.metric(
                    "Selected",
                    f"{source_result.get('selected', 0):,}",
                )

            with m2:

                st.metric(
                    "Candidates",
                    f"{source_result.get('candidates', 0):,}",
                )

                st.metric(
                    "Retrieved",
                    f"{source_result.get('retrieved', 0):,}",
                )

        if errors:

            st.error(
                "Collection errors"
            )

            for error in errors:

                st.write(
                    f"• {error}"
                )


# =========================================================
# SDMX Candidate Dataflows
# =========================================================

st.subheader(
    "6. Candidate Dataflows"
)


candidate_documents = []

for source_id, source_result in (
    source_results.items()
):

    documents = source_result.get(
        "candidate_documents",
        [],
    )

    for document in documents:

        candidate_documents.append(
            (
                source_id,
                document,
            )
        )


if not candidate_documents:

    if candidates > 0:

        st.info(
            f"{candidates} candidate dataflow(s) "
            "were detected, but candidate document "
            "details are not included in the API response."
        )

    else:

        st.info(
            "No candidate dataflows."
        )

else:

    for source_id, document in candidate_documents:

        metadata = document.get(
            "metadata",
            {},
        )

        title = document.get(
            "title",
            "Untitled",
        )

        score = metadata.get(
            "relevance_score"
        )

        sectors = metadata.get(
            "sectors",
            [],
        )

        terms = metadata.get(
            "matched_terms",
            [],
        )

        reasons = metadata.get(
            "reasons",
            [],
        )

        with st.container(
            border=True
        ):

            st.markdown(
                f"### {title}"
            )

            col1, col2, col3 = st.columns(
                3
            )

            with col1:

                st.write(
                    f"**Source:** `{source_id}`"
                )

            with col2:

                if score is not None:

                    st.write(
                        f"**Relevance Score:** "
                        f"`{score:.2f}`"
                    )

            with col3:

                if sectors:

                    st.write(
                        "**Sectors:** "
                        + ", ".join(sectors)
                    )

            if terms:

                st.write(
                    "**Matched Terms:** "
                    + ", ".join(terms)
                )

            if reasons:

                st.write(
                    "**Reasons:** "
                    + "; ".join(reasons)
                )

            external_id = document.get(
                "external_id"
            )

            if external_id:

                st.caption(
                    f"External ID: {external_id}"
                )


# =========================================================
# Errors
# =========================================================

errors = result.get(
    "errors",
    {},
)


if errors:

    st.subheader(
        "7. Collection Errors"
    )

    for source_id, error in errors.items():

        st.error(
            f"{source_id}: {error}"
        )


# =========================================================
# Raw API Response
# =========================================================

with st.expander(
    "Developer: Raw API Response"
):

    st.json(
        result
    )