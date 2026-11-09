from typing import Optional

from sqlalchemy import text

from app.db.database import get_engine
from app.db.models.document import Document


class DocumentRepository:

    def create(self, document: Document) -> Document:

        engine = get_engine()

        with engine.begin() as connection:

            # ---------------------------------------------
            # Document
            # ---------------------------------------------

            connection.execute(
                text(
                    """
                    INSERT INTO documents (
                        document_id,
                        external_id,
                        source_id,
                        title,
                        source_url,
                        source_name,
                        content,
                        published_at,
                        retrieved_at,
                        content_hash
                    )
                    VALUES (
                        :document_id,
                        :external_id,
                        :source_id,
                        :title,
                        :source_url,
                        :source_name,
                        :content,
                        :published_at,
                        :retrieved_at,
                        :content_hash
                    )
                    """
                ),
                {
                    "document_id": document.document_id,
                    "external_id": document.external_id,
                    "source_id": document.source_id,
                    "title": document.title,
                    "source_url": document.source_url,
                    "source_name": document.source_name,
                    "content": document.content,
                    "published_at": (
                        document.published_at.isoformat()
                        if document.published_at
                        else None
                    ),
                    "retrieved_at": (
                        document.retrieved_at.isoformat()
                        if document.retrieved_at
                        else None
                    ),
                    "content_hash": document.content_hash,
                },
            )

            # ---------------------------------------------
            # Countries
            # ---------------------------------------------

            for country in document.countries:
                connection.execute(
                    text(
                        """
                        INSERT INTO document_countries (
                            document_id,
                            country_code
                        )
                        VALUES (
                            :document_id,
                            :country_code
                        )
                        """
                    ),
                    {
                        "document_id": document.document_id,
                        "country_code": country,
                    },
                )

            # ---------------------------------------------
            # Sectors
            # ---------------------------------------------

            for sector in document.sectors:
                connection.execute(
                    text(
                        """
                        INSERT INTO document_sectors (
                            document_id,
                            sector_code
                        )
                        VALUES (
                            :document_id,
                            :sector_code
                        )
                        """
                    ),
                    {
                        "document_id": document.document_id,
                        "sector_code": sector,
                    },
                )

            # ---------------------------------------------
            # Policy domains
            # ---------------------------------------------

            for policy_domain in document.policy_domains:
                connection.execute(
                    text(
                        """
                        INSERT INTO document_policy_domains (
                            document_id,
                            policy_domain_code
                        )
                        VALUES (
                            :document_id,
                            :policy_domain_code
                        )
                        """
                    ),
                    {
                        "document_id": document.document_id,
                        "policy_domain_code": policy_domain,
                    },
                )

            # ---------------------------------------------
            # Topics
            # ---------------------------------------------

            for topic in document.topics:
                connection.execute(
                    text(
                        """
                        INSERT INTO document_topics (
                            document_id,
                            topic_code
                        )
                        VALUES (
                            :document_id,
                            :topic_code
                        )
                        """
                    ),
                    {
                        "document_id": document.document_id,
                        "topic_code": topic,
                    },
                )

        return document

    def get_by_id(
        self,
        document_id: str,
    ) -> Optional[Document]:

        engine = get_engine()

        with engine.connect() as connection:

            document = connection.execute(
                text(
                    """
                    SELECT
                        document_id,
                        external_id,
                        source_id,
                        title,
                        source_url,
                        source_name,
                        content,
                        published_at,
                        retrieved_at,
                        content_hash
                    FROM documents
                    WHERE document_id = :document_id
                    """
                ),
                {"document_id": document_id},
            ).mappings().first()

            if document is None:
                return None

            countries = connection.execute(
                text(
                    """
                    SELECT country_code
                    FROM document_countries
                    WHERE document_id = :document_id
                    ORDER BY country_code
                    """
                ),
                {"document_id": document_id},
            ).scalars().all()

            sectors = connection.execute(
                text(
                    """
                    SELECT sector_code
                    FROM document_sectors
                    WHERE document_id = :document_id
                    ORDER BY sector_code
                    """
                ),
                {"document_id": document_id},
            ).scalars().all()

            policy_domains = connection.execute(
                text(
                    """
                    SELECT policy_domain_code
                    FROM document_policy_domains
                    WHERE document_id = :document_id
                    ORDER BY policy_domain_code
                    """
                ),
                {"document_id": document_id},
            ).scalars().all()

            topics = connection.execute(
                text(
                    """
                    SELECT topic_code
                    FROM document_topics
                    WHERE document_id = :document_id
                    ORDER BY topic_code
                    """
                ),
                {"document_id": document_id},
            ).scalars().all()

        return Document(
            document_id=document["document_id"],
            external_id=document["external_id"],
            source_id=document["source_id"],
            title=document["title"],
            source_url=document["source_url"],
            source_name=document["source_name"],
            content=document["content"],
            published_at=document["published_at"],
            retrieved_at=document["retrieved_at"],
            content_hash=document["content_hash"],
            countries=list(countries),
            sectors=list(sectors),
            policy_domains=list(policy_domains),
            topics=list(topics),
        )

    def exists_by_external_id(
        self,
        external_id: str,
    ) -> bool:

        if not external_id:
            return False

        engine = get_engine()

        with engine.connect() as connection:
            result = connection.execute(
                text(
                    """
                    SELECT 1
                    FROM documents
                    WHERE external_id = :external_id
                    LIMIT 1
                    """
                ),
                {
                    "external_id": external_id,
                },
            ).first()

        return result is not None

    def exists_by_content_hash(
        self,
        content_hash: str,
    ) -> bool:

        if not content_hash:
            return False

        engine = get_engine()

        with engine.connect() as connection:
            result = connection.execute(
                text(
                    """
                    SELECT 1
                    FROM documents
                    WHERE content_hash = :content_hash
                    LIMIT 1
                    """
                ),
                {
                    "content_hash": content_hash,
                },
            ).first()

        return result is not None

    def count(self) -> int:
        engine = get_engine()

        with engine.connect() as connection:
            return connection.execute(
                text("SELECT COUNT(*) FROM documents")
            ).scalar_one()
