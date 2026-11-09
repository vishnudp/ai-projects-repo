import os
import json
import hashlib

CHUNK_CACHE = "cache/chunks"
DOC_CACHE = "cache/documents"

os.makedirs(CHUNK_CACHE, exist_ok=True)
os.makedirs(DOC_CACHE, exist_ok=True)


def get_hash(text):
    return hashlib.md5(
        text.encode("utf-8")
    ).hexdigest()


def load_chunk_cache(text):

    key = get_hash(text)

    path = f"{CHUNK_CACHE}/{key}.json"

    if os.path.exists(path):

        with open(path) as f:
            return json.load(f)

    return None


def save_chunk_cache(text, data):

    key = get_hash(text)

    path = f"{CHUNK_CACHE}/{key}.json"

    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def load_document_cache(document_key):

    path = (
        f"{DOC_CACHE}/"
        f"{document_key}.json"
    )

    if os.path.exists(path):

        with open(path) as f:
            return json.load(f)

    return None


def save_document_cache(document_key,data):

    path = (
        f"{DOC_CACHE}/"
        f"{document_key}.json"
    )

    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def generate_file_hash(text):

    return hashlib.md5(
        text.encode("utf-8")
    ).hexdigest()