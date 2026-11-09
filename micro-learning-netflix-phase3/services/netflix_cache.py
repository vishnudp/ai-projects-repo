import json
from pathlib import Path

NETFLIX_CACHE_DIR = Path(
    "cache/netflix"
)

NETFLIX_CACHE_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def load_netflix(chunk_no):

    path = (
        NETFLIX_CACHE_DIR
        /
        f"netflix_{chunk_no}.json"
    )

    if path.exists():

        return json.loads(
            path.read_text()
        )

    return None


def save_netflix(
    chunk_no,
    data
):

    path = (
        NETFLIX_CACHE_DIR
        /
        f"netflix_{chunk_no}.json"
    )

    with open(
        path,
        "w"
    ) as f:

        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )