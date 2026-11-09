import httpx
import streamlit as st


API_URL = "http://localhost:8000"


# =========================================================
# API
# =========================================================

def collect_sources(
    source_ids: list[str],
) -> dict:

    payload = {
        "source_ids": source_ids,
    }

    response = httpx.post(
        f"{API_URL}/collection",
        json=payload,
        timeout=300,
    )

    # Show actual FastAPI error instead of only
    # HTTPStatusError
    if response.status_code >= 400:

        try:
            detail = response.json()
        except Exception:
            detail = response.text

        raise RuntimeError(
            f"Collection API failed "
            f"({response.status_code}): "
            f"{detail}"
        )

    return response.json()


# =========================================================
# Page
# =========================================================

st.set_page_config(
    page_title="Sources & Collection",
    page_icon="🌍",
    layout="wide",
)


st.title(
    "🌍 Sources & Collection"
)

st.caption(
    "Wave 2 — Source Registry & Collection"
)


# =========================================================
# Source Selection
# =========================================================

st.subheader(
    "Collection Sources"
)

available_sources = [
    "oecd",
    "who",
    "world_bank",
]


selected_sources = st.multiselect(
    "Select sources",
    options=available_sources,
    default=["oecd"],
)


# =========================================================
# Collection Configuration
# =========================================================

st.subheader(
    "Collection Configuration"
)

col1, col2, col3 = st.columns(3)


with col1:

    primary_country = st.selectbox(
        "Primary Country",
        [
            "India",
            "Australia",
            "Singapore",
            "United States",
            "United Kingdom",
            "Canada",
            "Germany",
            "France",
            "Japan",
            "China",
        ],
        index=0,
    )


with col2:

    comparison_countries = st.multiselect(
        "Comparison Countries",
        [
            "Australia",
            "Singapore",
            "United States",
            "United Kingdom",
            "Canada",
            "Germany",
            "France",
            "Japan",
            "China",
            "India",
        ],
    )


with col3:

    sector = st.text_input(
        "Sector",
        placeholder=(
            "e.g. Artificial Intelligence"
        ),
    )


st.divider()


# =========================================================
# Execute Collection
# =========================================================

if st.button(
    "🚀 Start Collection",
    type="primary",
    disabled=not selected_sources,
):

    st.session_state[
        "collection_result"
    ] = None

    st.session_state[
        "collection_error"
    ] = None

    with st.spinner(
        "Collecting from selected sources..."
    ):

        try:

            result = collect_sources(
                selected_sources
            )

            st.session_state[
                "collection_result"
            ] = result

        except Exception as exc:

            st.session_state[
                "collection_error"
            ] = str(exc)


# =========================================================
# Error
# =========================================================

if st.session_state.get(
    "collection_error"
):

    st.error(
        st.session_state[
            "collection_error"
        ]
    )


# =========================================================
# Result
# =========================================================

result = st.session_state.get(
    "collection_result"
)


if result:

    st.success(
        f"Collection {result.get('status', 'completed')}"
    )

    # -----------------------------------------------------
    # Overall Metrics
    # -----------------------------------------------------

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:

        st.metric(
            "Sources",
            result.get(
                "requested_sources",
                0,
            ),
        )

    with col2:

        st.metric(
            "Successful",
            result.get(
                "successful_sources",
                0,
            ),
        )

    with col3:

        st.metric(
            "Discovered",
            result.get(
                "discovered",
                0,
            ),
        )

    with col4:

        st.metric(
            "Candidates",
            result.get(
                "candidates",
                0,
            ),
        )

    with col5:

        st.metric(
            "Duration",
            f"{result.get('duration_ms', 0):.0f} ms",
        )


    st.divider()


    # =====================================================
    # Source Results
    # =====================================================

    st.subheader(
        "Source Results"
    )

    sources = result.get(
        "sources",
        [],
    )

    for source in sources:

        source_id = source.get(
            "source_id",
            "unknown",
        )

        collector = source.get(
            "collector",
            "unknown",
        )

        with st.expander(
            f"{source_id.upper()} — {collector}"
        ):

            col1, col2, col3, col4 = st.columns(4)

            with col1:

                st.metric(
                    "Discovered",
                    source.get(
                        "discovered",
                        0,
                    ),
                )

            with col2:

                st.metric(
                    "Candidates",
                    source.get(
                        "candidates",
                        source.get(
                            "candidate_count",
                            0,
                        ),
                    ),
                )

            with col3:

                st.metric(
                    "Selected",
                    source.get(
                        "selected",
                        0,
                    ),
                )

            with col4:

                st.metric(
                    "Retrieved",
                    source.get(
                        "retrieved",
                        0,
                    ),
                )

            errors = source.get(
                "errors",
                [],
            )

            if errors:

                st.error(
                    "\n".join(errors)
                )


    # =====================================================
    # Candidate Documents
    # =====================================================

    st.divider()

    st.subheader(
        "Candidate Documents"
    )

    all_candidates = []

    for source in sources:

        candidates = source.get(
            "candidate_documents",
            [],
        )

        if isinstance(
            candidates,
            list,
        ):

            for candidate in candidates:

                candidate["_source_id"] = (
                    source.get(
                        "source_id"
                    )
                )

                all_candidates.append(
                    candidate
                )


    if all_candidates:

        st.write(
            f"Showing "
            f"{len(all_candidates)} "
            f"candidate documents"
        )

        # -------------------------------------------------
        # Candidate filters
        # -------------------------------------------------

        candidate_col1, candidate_col2 = (
            st.columns(2)
        )

        with candidate_col1:

            country_filter = st.text_input(
                "Filter by country",
                key="candidate_country",
            )

        with candidate_col2:

            sector_filter = st.text_input(
                "Filter by sector",
                key="candidate_sector",
            )


        filtered_candidates = []

        for candidate in all_candidates:

            countries = (
                candidate.get(
                    "countries",
                    [],
                )
                or candidate.get(
                    "matched_countries",
                    [],
                )
            )

            sectors = candidate.get(
                "matched_sectors",
                [],
            )

            if isinstance(
                countries,
                str,
            ):
                countries = [
                    countries
                ]

            if isinstance(
                sectors,
                str,
            ):
                sectors = [
                    sectors
                ]

            country_text = " ".join(
                str(x)
                for x in countries
            ).lower()

            sector_text = " ".join(
                str(x)
                for x in sectors
            ).lower()

            if (
                country_filter
                and country_filter.lower()
                not in country_text
            ):
                continue

            if (
                sector_filter
                and sector_filter.lower()
                not in sector_text
            ):
                continue

            filtered_candidates.append(
                candidate
            )


        # -------------------------------------------------
        # Candidate table
        # -------------------------------------------------

        table_rows = []

        for candidate in filtered_candidates:

            table_rows.append(
                {
                    "Source": candidate.get(
                        "_source_id",
                        "",
                    ),

                    "Title": candidate.get(
                        "title",
                        "",
                    ),

                    "Score": candidate.get(
                        "relevance_score",
                        0,
                    ),

                    "Countries": ", ".join(
                        candidate.get(
                            "matched_countries",
                            [],
                        )
                    ),

                    "Sectors": ", ".join(
                        candidate.get(
                            "matched_sectors",
                            [],
                        )
                    ),

                    "Dataflow": candidate.get(
                        "dataflow_id",
                        "",
                    ),
                }
            )


        if table_rows:

            st.dataframe(
                table_rows,
                use_container_width=True,
                hide_index=True,
            )

        else:

            st.info(
                "No candidates match "
                "the selected filters."
            )


        # -------------------------------------------------
        # Candidate details
        # -------------------------------------------------

        st.subheader(
            "Candidate Details"
        )

        # =========================================================
        # Candidate Documents
        # =========================================================

        candidate_documents = source.get(
            "candidate_documents",
            [],
        )

        if not candidate_documents:

            st.info(
                "No candidate documents returned "
                "for this source."
            )

        else:

            st.markdown(
                f"### Candidates "
                f"({len(candidate_documents)})"
            )

            for index, candidate in enumerate(
                candidate_documents,
                start=1,
            ):

                title = (
                    candidate.get(
                        "title"
                    )
                    or "Untitled Dataflow"
                )

                st.markdown(
                    f"#### {index}. {title}"
                )

                # -------------------------------------------------
                # Basic metadata
                # -------------------------------------------------

                col1, col2, col3 = st.columns(
                    3
                )

                with col1:

                    st.write(
                        "**Source**"
                    )

                    st.write(
                        candidate.get(
                            "source_id"
                        )
                        or source.get(
                            "source_id"
                        )
                        or "N/A"
                    )

                with col2:

                    st.write(
                        "**Dataflow**"
                    )

                    st.code(
                        candidate.get(
                            "dataflow_id"
                        )
                        or "N/A"
                    )

                with col3:

                    st.write(
                        "**Agency**"
                    )

                    st.code(
                        candidate.get(
                            "agency_id"
                        )
                        or "N/A"
                    )

                # -------------------------------------------------
                # Relevance
                # -------------------------------------------------

                score = float(
                    candidate.get(
                        "relevance_score",
                        0,
                    )
                    or 0
                )

                st.progress(
                    min(
                        max(
                            score,
                            0.0,
                        ),
                        1.0,
                    ),
                    text=(
                        f"Relevance Score: "
                        f"{score:.2f}"
                    ),
                )

                # -------------------------------------------------
                # Countries
                # -------------------------------------------------

                countries = (
                    candidate.get(
                        "countries",
                        []
                    )
                    or []
                )

                matched_countries = (
                    candidate.get(
                        "matched_countries",
                        []
                    )
                    or []
                )

                matched_sectors = (
                    candidate.get(
                        "matched_sectors",
                        []
                    )
                    or []
                )

                matched_terms = (
                    candidate.get(
                        "matched_terms",
                        []
                    )
                    or []
                )

                col1, col2 = st.columns(
                    2
                )

                with col1:

                    st.write(
                        "**Countries**"
                    )

                    if countries:

                        st.write(
                            ", ".join(
                                str(country)
                                for country
                                in countries
                            )
                        )

                    else:

                        st.caption(
                            "Country dimension not "
                            "available yet."
                        )

                with col2:

                    st.write(
                        "**Matched Countries**"
                    )

                    if matched_countries:

                        st.write(
                            ", ".join(
                                str(country)
                                for country
                                in matched_countries
                            )
                        )

                    else:

                        st.caption(
                            "No country match."
                        )

                # -------------------------------------------------
                # Sectors / Terms
                # -------------------------------------------------

                col1, col2 = st.columns(
                    2
                )

                with col1:

                    st.write(
                        "**Matched Sectors**"
                    )

                    if matched_sectors:

                        for sector in (
                            matched_sectors
                        ):

                            st.success(
                                sector
                            )

                    else:

                        st.caption(
                            "No sector match."
                        )

                with col2:

                    st.write(
                        "**Matched Terms**"
                    )

                    if matched_terms:

                        st.write(
                            ", ".join(
                                str(term)
                                for term
                                in matched_terms
                            )
                        )

                    else:

                        st.caption(
                            "No keyword match."
                        )

                # -------------------------------------------------
                # Reasons
                # -------------------------------------------------

                reasons = (
                    candidate.get(
                        "reasons",
                        []
                    )
                    or []
                )

                if reasons:

                    with st.expander(
                        "Why was this candidate selected?"
                    ):

                        for reason in reasons:

                            st.write(
                                f"• {reason}"
                            )

                # -------------------------------------------------
                # Source URL
                # -------------------------------------------------

                source_url = (
                    candidate.get(
                        "source_url"
                    )
                    or source.get(
                        "source_url"
                    )
                )

                if source_url:

                    st.link_button(
                        "Open Source",
                        source_url,
                    )

                st.divider()