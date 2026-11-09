import time
from concurrent.futures import ThreadPoolExecutor

from services.local_llm import generate

from services.cache_service import (
    load_chunk_cache,
    save_chunk_cache
)


def summarize_chunk(chunk):

    cached = load_chunk_cache(chunk)

    if cached:

        print("CHUNK CACHE HIT")

        return cached

    prompt = open(
        "prompts/chunk_summary_prompt.txt",
        encoding="utf-8"
    ).read()

    prompt = prompt.replace(
        "{chunk}",
        chunk
    )

    start = time.time()

    result = generate(prompt)

    print(
        f"Chunk processed in "
        f"{round(time.time()-start,2)} sec"
    )

    save_chunk_cache(
        chunk,
        result
    )

    return result


def summarize_chunks_parallel(chunks):

    with ThreadPoolExecutor(
        max_workers=4
    ) as executor:

        results = list(
            executor.map(
                summarize_chunk,
                chunks
            )
        )

    return results