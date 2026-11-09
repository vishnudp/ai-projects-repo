import json
from typing import Optional

from sqlalchemy import text

from app.db.database import get_engine
from app.db.models.source import Source


class SourceRepository:

    def create(self, source: Source) -> Source:
        engine = get_engine()

        with engine.begin() as connection:
           connection.execute(
            text(
                """
                INSERT INTO sources (
                    source_id,
                    name,
                    organization,
                    source_type,
                    url,
                    country_scope,
                    sector_scope,
                    collection_methods,
                    reliability,
                    enabled,
                    metadata
                )
                VALUES (
                    :source_id,
                    :name,
                    :organization,
                    :source_type,
                    :url,
                    :country_scope,
                    :sector_scope,
                    :collection_methods,
                    :reliability,
                    :enabled,
                    :metadata
                )
                """
            ),
            {
                "source_id": source.source_id,
                "name": source.name,
                "organization": source.organization,
                "source_type": source.source_type,
                "url": source.url,
                "country_scope": json.dumps(
                    source.country_scope
                ),
                "sector_scope": json.dumps(
                    source.sector_scope
                ),
                "collection_methods": json.dumps(
                    source.collection_methods
                ),
                "reliability": source.reliability,
                "enabled": int(source.enabled),
                "metadata": json.dumps(
                    source.metadata
                ),
            },
        )

        return source

    def get_by_id(
        self,
        source_id: str,
    ) -> Optional[Source]:

        engine = get_engine()

        with engine.connect() as connection:
            row = connection.execute(
                text(
                    """
                    SELECT
                        source_id,
                        name,
                        organization,
                        source_type,
                        url,
                        country_scope,
                        sector_scope,
                        collection_methods,
                        reliability,
                        enabled,
                        metadata
                    FROM sources
                    WHERE source_id = :source_id
                    """
                ),
                {"source_id": source_id},
            ).mappings().first()

        if row is None:
            return None

        return Source(
            source_id=row["source_id"],
            name=row["name"],
            organization=row["organization"],
            source_type=row["source_type"],
            url=row["url"],
            country_scope=json.loads(
                row["country_scope"] or "[]"
            ),
            sector_scope=json.loads(
                row["sector_scope"] or "[]"
            ),
            collection_methods=json.loads(
                row["collection_methods"] or "[]"
            ),
            reliability=row["reliability"],
            enabled=bool(row["enabled"]),
            metadata=json.loads(
                row["metadata"] or "{}"
            ),
        )

    def count(self) -> int:
        engine = get_engine()

        with engine.connect() as connection:
            return connection.execute(
                text("SELECT COUNT(*) FROM sources")
            ).scalar_one()
