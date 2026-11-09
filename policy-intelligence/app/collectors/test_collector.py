from datetime import datetime, timezone

from app.collectors.base import BaseCollector
from app.ingestion.base import RawDocument


class TestCollector(BaseCollector):
    """
    Deterministic collector used for integration tests.

    This does not access the internet.
    """

    def collect(self) -> list[RawDocument]:

        return [
            RawDocument(
                external_id="collector-test-001",

                title="Global AI Policy Update",

                source_url=(
                    "https://example.org/"
                    "collector-test-001"
                ),

                source_id=self.source_id,

                source_name=self.config.get(
                    "source_name",
                    self.source_id,
                ),

                content=(
                    "Artificial intelligence policy "
                    "is becoming increasingly important "
                    "for national policy planning."
                ),

                published_at=datetime(
                    2026,
                    8,
                    17,
                    tzinfo=timezone.utc,
                ),

                metadata={
                    "collector": "test",
                },
            )
        ]