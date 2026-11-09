import json
import hashlib
from pathlib import Path


def get_cache_key(text, model):

    return hashlib.md5(
        f"{text}_{model}".encode()
    ).hexdigest()


def load_cache(cache_dir, key):

    path = Path(cache_dir) / f"{key}.json"

    if path.exists():

        return json.loads(path.read_text())

    return None


def save_cache(cache_dir, key, data):

    path = Path(cache_dir)

    path.mkdir(parents=True, exist_ok=True)

    with open(path / f"{key}.json", "w") as f:

        json.dump(data, f, indent=2)