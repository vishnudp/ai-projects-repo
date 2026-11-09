import json

from services.local_llm import generate

from services.cache_service import (
    load_document_cache,
    save_document_cache
)

from utils.json_utils import (
    extract_json
)


def summarize_document(
    document_key,
    chunk_summaries
):

    # -------------------------
    # CACHE CHECK
    # -------------------------

    cached = load_document_cache(
        document_key
    )

    if cached:

        print(
            "DOCUMENT CACHE HIT"
        )

        return cached

    # -------------------------
    # BUILD PROMPT
    # -------------------------

    prompt = open(
        "prompts/document_summary_prompt.txt",
        encoding="utf-8"
    ).read()

    prompt = prompt.replace(
        "{summaries}",
        json.dumps(
            chunk_summaries,
            ensure_ascii=False
        )
    )

    # -------------------------
    # LLM CALL
    # -------------------------

    result = generate(
        prompt
    )

    print(
        "DOCUMENT SUMMARY GENERATED"
    )

    # -------------------------
    # PARSE JSON
    # -------------------------

    try:

        data = extract_json(
            result
        )

        save_document_cache(
            document_key,
            data
        )

        return data

    except Exception as e:

        print(
            "JSON PARSE ERROR"
        )

        print(e)

        print(
            "RAW RESPONSE"
        )

        print(result)

        return {
            "error": str(e),
            "raw_response": result
        }