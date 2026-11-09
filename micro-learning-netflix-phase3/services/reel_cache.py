# services/reel_cache.py

import json
from pathlib import Path

REEL_DIR = Path(
    "generated/reels"
)

def load_reel(chunk_no):

    path = REEL_DIR / (
        f"reel_{chunk_no}.json"
    )

    if path.exists():

        with open(path) as f:
            return json.load(f)

    return None


def save_reel(
    chunk_no,
    data
):

    path = REEL_DIR / (
        f"reel_{chunk_no}.json"
    )

    with open(path, "w") as f:

        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )