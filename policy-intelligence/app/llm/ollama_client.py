from typing import Any

import ollama
import structlog

from app.cache.manager import llm_cache
from app.core.config import get_settings
from app.core.metrics import metrics


logger = structlog.get_logger()


class OllamaClient:

    def __init__(self):
        self.settings = get_settings()

        self.client = ollama.Client(
            host=self.settings.ollama_host
        )

    def list_models(self) -> list[str]:
        response = self.client.list()

        models = getattr(
            response,
            "models",
            [],
        )

        result = []

        for model in models:
            name = (
                getattr(model, "model", None)
                or getattr(model, "name", None)
            )

            if name:
                result.append(name)

        return sorted(result)

    def chat(
        self,
        prompt: str,
        *,
        model: str | None = None,
        temperature: float = 0.2,
        system: str | None = None,
        use_cache: bool = True,
    ) -> dict[str, Any]:

        model = (
            model
            or self.settings.ollama_model_fast
        )

        cache_key = llm_cache.make_key(
            model,
            prompt,
            system,
            temperature,
        )

        if (
            self.settings.llm_cache_enabled
            and use_cache
        ):
            cached = llm_cache.get(
                cache_key
            )

            if cached is not None:
                metrics.increment(
                    "llm_cache_hits"
                )

                return cached

        metrics.increment(
            "llm_cache_misses"
        )

        messages = []

        if system:
            messages.append(
                {
                    "role": "system",
                    "content": system,
                }
            )

        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        response = self.client.chat(
            model=model,
            messages=messages,
            options={
                "temperature": temperature
            },
        )

        result = {
            "model": model,
            "content": response["message"][
                "content"
            ],
            "done": response.get(
                "done",
                True,
            ),
        }

        if (
            self.settings.llm_cache_enabled
            and use_cache
        ):
            llm_cache.set(
                cache_key,
                result,
            )

        return result


ollama_client = OllamaClient()