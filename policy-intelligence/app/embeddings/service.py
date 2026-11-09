import hashlib
from functools import lru_cache

from sentence_transformers import SentenceTransformer

from app.cache.manager import embedding_cache
from app.core.config import get_settings
from app.core.metrics import metrics


@lru_cache
def get_embedding_model() -> SentenceTransformer:
    settings = get_settings()

    return SentenceTransformer(
        settings.embedding_model
    )


class EmbeddingService:

    def __init__(self):
        self.settings = get_settings()

    @staticmethod
    def content_hash(text: str) -> str:
        return hashlib.sha256(
            text.encode("utf-8")
        ).hexdigest()

    def embed(
        self,
        text: str,
    ) -> list[float]:

        content_hash = self.content_hash(
            text
        )

        cache_key = embedding_cache.make_key(
            self.settings.embedding_model,
            content_hash,
        )

        # -----------------------------------------
        # Cache lookup
        # -----------------------------------------

        if self.settings.embedding_cache_enabled:

            cached = embedding_cache.get(
                cache_key
            )

            if cached is not None:

                metrics.increment(
                    "embedding_cache_hits"
                )

                return cached

        metrics.increment(
            "embedding_cache_misses"
        )

        # -----------------------------------------
        # Generate embedding
        # -----------------------------------------

        model = get_embedding_model()

        vector = model.encode(
            text,
            normalize_embeddings=True,
        ).tolist()

        # -----------------------------------------
        # Cache result
        # -----------------------------------------

        if self.settings.embedding_cache_enabled:

            embedding_cache.set(
                cache_key,
                vector
            )

        return vector

    def embed_many(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        if not texts:
            return []

        return [
            self.embed(text)
            for text in texts
        ]


embedding_service = EmbeddingService()