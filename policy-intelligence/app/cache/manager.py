import hashlib
import json
from pathlib import Path
from typing import Any

from app.core.config import BASE_DIR


class FileCache:
    """
    Local file-based cache.

    Used for the MVP.
    Can later be replaced by Redis without
    changing the business/service layer.
    """

    def __init__(self, namespace: str):
        self.root = (
            BASE_DIR
            / "data"
            / "cache"
            / namespace
        )

        self.root.mkdir(
            parents=True,
            exist_ok=True,
        )

    @staticmethod
    def make_key(*parts: Any) -> str:
        payload = json.dumps(
            parts,
            sort_keys=True,
            default=str,
        )

        return hashlib.sha256(
            payload.encode("utf-8")
        ).hexdigest()

    def get(self, key: str) -> Any | None:
        path = self.root / f"{key}.json"

        if not path.exists():
            return None

        try:
            return json.loads(
                path.read_text(
                    encoding="utf-8"
                )
            )
        except (
            OSError,
            json.JSONDecodeError,
        ):
            return None

    def set(
        self,
        key: str,
        value: Any,
    ) -> None:
        path = self.root / f"{key}.json"
        temp_path = path.with_suffix(".tmp")

        temp_path.write_text(
            json.dumps(
                value,
                ensure_ascii=False,
                default=str,
            ),
            encoding="utf-8",
        )

        temp_path.replace(path)

    def delete(self, key: str) -> None:
        path = self.root / f"{key}.json"

        if path.exists():
            path.unlink()

    def clear(self) -> None:
        for path in self.root.glob("*.json"):
            path.unlink()


# ============================================================
# Cache namespaces
# ============================================================

llm_cache = FileCache("llm")

embedding_cache = FileCache("embeddings")

retrieval_cache = FileCache("retrieval")