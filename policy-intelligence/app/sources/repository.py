from app.sources.models import Source
from app.sources.service import (
    get_enabled_sources,
    get_source,
)


class SourceRepository:

    def get_by_id(
        self,
        source_id: str,
    ) -> Source | None:

        return get_source(
            source_id
        )

    def get_enabled(
        self,
    ) -> list[Source]:

        return get_enabled_sources()

    def exists(
        self,
        source_id: str,
    ) -> bool:

        return (
            self.get_by_id(source_id)
            is not None
        )