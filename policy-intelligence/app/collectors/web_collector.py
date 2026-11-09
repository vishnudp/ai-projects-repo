from datetime import datetime, timezone

import requests
from requests import Response
from requests.exceptions import RequestException

from app.collectors.base import BaseCollector
from app.ingestion.base import RawDocument

from app.collectors.errors import (
    CollectorHTTPError,
    CollectorNetworkError,
    CollectorValidationError,
)

class WebCollector(BaseCollector):
    """
    Collector for web-based sources.

    Responsibility:
        Fetch web content and convert it into RawDocument.

    Not responsible for:
        - policy classification
        - sector classification
        - country classification
        - topic extraction
        - relevance scoring
        - LLM processing
        - persistence
    """

    DEFAULT_TIMEOUT = 15
    DEFAULT_MAX_CONTENT_SIZE = 5 * 1024 * 1024
    DEFAULT_RETRIES = 3

    def collect(self) -> list[RawDocument]:

        collection_config = self.config.get(
            "collection",
            {},
        )

        url = collection_config.get("base_url")

        if not url:
            raise ValueError(
                f"No base_url configured for source "
                f"{self.source_id}"
            )

        timeout = collection_config.get(
            "timeout",
            self.DEFAULT_TIMEOUT,
        )

        max_content_size = collection_config.get(
            "max_content_size",
            self.DEFAULT_MAX_CONTENT_SIZE,
        )

        retries = collection_config.get(
            "retries",
            self.DEFAULT_RETRIES,
        )

        response = self._fetch(
            url=url,
            timeout=timeout,
            retries=retries,
        )

        self._validate_response(
            response=response,
            max_content_size=max_content_size,
        )

        content = response.text

        source_name = self.config.get(
            "name"
        )

        document = RawDocument(
            external_id=url,

            title=(
                source_name
                or self.source_id
            ),

            source_url=url,

            source_id=self.source_id,

            source_name=source_name,

            content=content,

            retrieved_at=datetime.now(
                timezone.utc
            ),

            metadata={
                "collector": "web",
                "http_status": response.status_code,
                "content_type": response.headers.get(
                    "Content-Type"
                ),
                "content_length": len(
                    response.content
                ),
            },
        )

        return self._validate_documents(
            [document]
        )

    def _fetch(
        self,
        url: str,
        timeout: int,
        retries: int,
    ) -> Response:

        last_error = None

        for attempt in range(1, retries + 1):

            try:

                response = requests.get(
                    url,
                    timeout=timeout,
                    headers={
                        "User-Agent": (
                            "GlobalPolicyIntelligence/0.1"
                        )
                    },
                )

                return response

            except RequestException as exc:

                last_error = exc

                if attempt == retries:
                    raise CollectorNetworkError(
                        message=(
                            f"Failed to fetch URL: {url}"
                        ),
                        source_id=self.source_id,
                    ) from exc

        raise RuntimeError(
            f"Failed to fetch URL after "
            f"{retries} attempts: {url}"
        ) from last_error

    def _validate_response(
        self,
        response: Response,
        max_content_size: int,
    ) -> None:

        try:
            response.raise_for_status()

        except RequestException as exc:

            retryable = response.status_code >= 500

            raise CollectorHTTPError(
                message=(
                    f"HTTP request failed: "
                    f"{response.status_code}"
                ),
                source_id=self.source_id,
                retryable=retryable,
            ) from exc

        content_type = (
            response.headers
            .get("Content-Type", "")
            .lower()
        )

        allowed_content_types = (
            "text/html",
            "text/plain",
            "application/xhtml+xml",
        )

        if not any(
            content_type.startswith(
                allowed
            )
            for allowed in allowed_content_types
        ):

            raise CollectorValidationError(
                message=(
                    f"Unsupported content type: "
                    f"{content_type}"
                ),
                source_id=self.source_id,
            )

        content_length = response.headers.get(
            "Content-Length"
        )

        if content_length:

            try:
                size = int(content_length)

                if size > max_content_size:
                    raise CollectorValidationError(
                        message=(
                            "Response exceeds maximum "
                            "allowed size"
                        ),
                        source_id=self.source_id,
                    )

            except ValueError as exc:

                if "exceeds maximum" in str(exc):
                    raise

        if len(response.content) > max_content_size:

            raise ValueError(
                "Response exceeds maximum "
                "allowed size"
            )