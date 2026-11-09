from datetime import datetime, timezone

import feedparser
import requests
from requests.exceptions import RequestException

from app.collectors.base import BaseCollector
from app.collectors.errors import (
    CollectorHTTPError,
    CollectorNetworkError,
    CollectorValidationError,
)
from app.ingestion.base import RawDocument


class RSSCollector(BaseCollector):
    """
    Collector for RSS/Atom feeds.

    Collection only.
    No classification or intelligence processing.
    """

    DEFAULT_TIMEOUT = 15
    DEFAULT_RETRIES = 3

    def collect(self) -> list[RawDocument]:

        collection_config = self.config.get(
            "collection",
            {},
        )

        feed_url = collection_config.get(
            "rss_url"
        )

        print(
            "rss feed_url:",
            feed_url,
        )

        if not feed_url:
            raise CollectorValidationError(
                message=(
                    f"No rss_url configured for "
                    f"source {self.source_id}"
                ),
                source_id=self.source_id,
            )

        timeout = collection_config.get(
            "timeout",
            self.DEFAULT_TIMEOUT,
        )

        retries = collection_config.get(
            "retries",
            self.DEFAULT_RETRIES,
        )

        content = self._fetch(
            feed_url,
            timeout,
            retries,
        )

        parsed = feedparser.parse(content)

        if parsed.bozo and not parsed.entries:
            raise CollectorValidationError(
                message=(
                    "RSS/Atom feed could not "
                    "be parsed"
                ),
                source_id=self.source_id,
            )

        documents = []

        source_name = self.config.get(
            "name"
        )

        for entry in parsed.entries:

            title = (
                entry.get("title")
                or ""
            ).strip()

            url = (
                entry.get("link")
                or ""
            ).strip()

            content_text = (
                entry.get("summary")
                or entry.get("description")
                or ""
            )

            if not title and not url:
                continue

            external_id = (
                entry.get("id")
                or entry.get("guid")
                or url
            )

            published_at = (
                self._parse_date(entry)
            )

            document = RawDocument(
                external_id=external_id,

                title=title,

                source_url=url or feed_url,

                source_id=self.source_id,

                source_name=source_name,

                content=content_text,

                published_at=published_at,

                retrieved_at=datetime.now(
                    timezone.utc
                ),

                metadata={
                    "collector": "rss",
                    "feed_url": feed_url,
                },
            )

            documents.append(document)

        return self._validate_documents(
            documents
        )

    def _fetch(
        self,
        url: str,
        timeout: int,
        retries: int,
    ) -> bytes:

        last_error = None

        for attempt in range(
            1,
            retries + 1,
        ):

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

                try:
                    response.raise_for_status()

                except RequestException as exc:

                    raise CollectorHTTPError(
                        message=(
                            f"RSS request failed: "
                            f"{response.status_code}"
                        ),
                        source_id=self.source_id,
                        retryable=(
                            response.status_code >= 500
                        ),
                    ) from exc

                return response.content

            except CollectorHTTPError as exc:

                if not exc.retryable:
                    raise

                last_error = exc

            except RequestException as exc:

                last_error = exc

                if attempt == retries:
                    raise CollectorNetworkError(
                        message=(
                            f"Failed to fetch RSS "
                            f"feed: {url}"
                        ),
                        source_id=self.source_id,
                    ) from exc

        raise CollectorNetworkError(
            message=(
                f"Failed to fetch RSS feed "
                f"after {retries} attempts: {url}"
            ),
            source_id=self.source_id,
        ) from last_error

    @staticmethod
    def _parse_date(
        entry,
    ):
        parsed_time = (
            entry.get(
                "published_parsed"
            )
            or entry.get(
                "updated_parsed"
            )
        )

        if not parsed_time:
            return None

        try:
            return datetime(
                *parsed_time[:6],
                tzinfo=timezone.utc,
            )

        except (TypeError, ValueError):
            return None