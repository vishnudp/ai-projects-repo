import os
import time
import streamlit as st

from services.extractor import extract_text

from services.chunk_service import (
    create_chunks
)

from services.summary_service import (
    summarize_chunks_parallel
)

from services.document_service import (
    summarize_document
)

from services.repository import (
    save_case,
    load_repository
)

from services.comparison_service import (
    compare_case_studies
)

from services.cache_service import (
    generate_file_hash
)

# ------------------------------------
# PAGE CONFIG
# ------------------------------------

st.set_page_config(
    page_title="AI Case Study Intelligence Engine",
    layout="wide"
)

st.title(
    "AI Case Study Intelligence Engine"
)

st.write(
    """
    Upload one or more case studies and generate:

    - Chunk Summaries
    - Document Summaries
    - Repository Knowledge Base
    - Case Study Comparison
    - Best Practices
    - Success Rate Analysis
    - Cost Reduction Analysis
    """
)

# ------------------------------------
# ENSURE DIRECTORIES EXIST
# ------------------------------------

os.makedirs(
    "uploads",
    exist_ok=True
)

os.makedirs(
    "cache/chunks",
    exist_ok=True
)

os.makedirs(
    "cache/documents",
    exist_ok=True
)

# ------------------------------------
# FILE UPLOAD
# ------------------------------------

uploaded_files = st.file_uploader(
    "Upload Case Studies",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)

processed_cases = []

# ------------------------------------
# PROCESS FILES
# ------------------------------------

if uploaded_files:

    for uploaded_file in uploaded_files:

        st.divider()

        st.subheader(
            f"Processing: {uploaded_file.name}"
        )

        total_start = time.time()

        # ----------------------------
        # SAVE FILE
        # ----------------------------

        file_path = os.path.join(
            "uploads",
            uploaded_file.name
        )

        with open(
            file_path,
            "wb"
        ) as f:

            f.write(
                uploaded_file.getbuffer()
            )

        # ----------------------------
        # EXTRACT TEXT
        # ----------------------------

        with st.spinner(
            "Extracting text..."
        ):

            text = extract_text(
                file_path
            )

        st.success(
            "Text extraction completed"
        )

        st.write(
            f"Characters Extracted: {len(text):,}"
        )

        # --------------------------------
        # POC LIMIT
        # --------------------------------

        text = text[:30000]

        st.info(
            f"Using {len(text):,} characters for analysis"
        )

        # --------------------------------
        # FILE HASH FOR CACHE
        # --------------------------------

        file_hash = generate_file_hash(
            text
        )

        # --------------------------------
        # CHUNKING
        # --------------------------------

        chunks = create_chunks(
            text,
            chunk_size=15000
        )

        st.info(
            f"Total Chunks: {len(chunks)}"
        )

        # --------------------------------
        # CHUNK SUMMARIES
        # --------------------------------

        chunk_start = time.time()

        with st.spinner(
            "Generating chunk summaries..."
        ):

            chunk_summaries = (
                summarize_chunks_parallel(
                    chunks
                )
            )

        chunk_time = round(
            time.time() - chunk_start,
            2
        )

        st.success(
            f"{len(chunk_summaries)} chunk summaries generated"
        )

        st.write(
            f"Chunk Summary Time: {chunk_time} sec"
        )

        # --------------------------------
        # DEBUG VIEW
        # --------------------------------

        with st.expander(
            "View Chunk Summaries"
        ):

            st.json(
                chunk_summaries
            )

        # --------------------------------
        # DOCUMENT SUMMARY
        # --------------------------------

        document_start = time.time()

        with st.spinner(
            "Generating document summary..."
        ):

            document_summary = (
                summarize_document(
                    file_hash,
                    chunk_summaries
                )
            )

        document_time = round(
            time.time() - document_start,
            2
        )

        st.success(
            "Document Summary Generated"
        )

        st.write(
            f"Document Summary Time: {document_time} sec"
        )

        # --------------------------------
        # DISPLAY SUMMARY
        # --------------------------------

        st.subheader(
            "Document Summary"
        )

        st.json(
            document_summary
        )

        processed_cases.append(
            document_summary
        )

        # --------------------------------
        # SAVE TO REPOSITORY
        # --------------------------------

        try:

            save_case(
                document_summary
            )

            st.success(
                "Saved to repository"
            )

        except Exception as e:

            st.error(
                f"Repository Save Error: {e}"
            )

        total_time = round(
            time.time() - total_start,
            2
        )

        st.info(
            f"Total Processing Time: {total_time} sec"
        )

# ------------------------------------
# CASE STUDY COMPARISON
# ------------------------------------

if len(processed_cases) >= 2:

    st.divider()

    st.header(
        "Case Study Comparison"
    )

    with st.spinner(
        "Comparing case studies..."
    ):

        comparison = compare_case_studies(
            processed_cases
        )

    st.json(
        comparison
    )

# ------------------------------------
# REPOSITORY VIEW
# ------------------------------------

st.divider()

st.subheader(
    "Repository"
)

if st.button(
    "Load Repository"
):

    try:

        cases = load_repository()

        st.success(
            f"Loaded {len(cases)} case studies"
        )

        st.json(
            cases
        )

    except Exception as e:

        st.error(
            str(e)
        )

