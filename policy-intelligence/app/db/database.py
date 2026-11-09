from app.core.config import BASE_DIR, get_settings
from sqlalchemy import create_engine, text


def _normalize_database_url(url: str) -> str:
    if url.startswith("sqlite:///./"):
        relative_path = url.removeprefix("sqlite:///./")

        absolute_path = BASE_DIR / relative_path
        absolute_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        return f"sqlite:///{absolute_path}"

    return url


def get_engine():
    settings = get_settings()

    database_url = _normalize_database_url(
        settings.database_url
    )

    connect_args = {}

    if database_url.startswith("sqlite"):
        connect_args = {
            "check_same_thread": False,
        }

    return create_engine(
        database_url,
        connect_args=connect_args,
        future=True,
    )


def initialize_database() -> None:
    engine = get_engine()

    statements = [

        # -------------------------------------------------
        # Sources
        # -------------------------------------------------

        """
       CREATE TABLE IF NOT EXISTS sources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_id TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            organization TEXT,
            source_type TEXT,
            url TEXT,
            country_scope TEXT,
            sector_scope TEXT,
            collection_methods TEXT,
            reliability REAL,
            enabled INTEGER NOT NULL DEFAULT 1,
            metadata TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """,

        # -------------------------------------------------
        # Documents
        # -------------------------------------------------

        """
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id TEXT NOT NULL UNIQUE,
            external_id TEXT UNIQUE,
            source_id TEXT,
            title TEXT NOT NULL,
            source_url TEXT,
            source_name TEXT,
            content TEXT,
            published_at TEXT,
            retrieved_at TEXT,
            content_hash TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (source_id)
                REFERENCES sources(source_id)
        )
        """,

        # -------------------------------------------------
        # Document → Countries
        # -------------------------------------------------

        """
        CREATE TABLE IF NOT EXISTS document_countries (
            document_id TEXT NOT NULL,
            country_code TEXT NOT NULL,

            PRIMARY KEY (
                document_id,
                country_code
            ),

            FOREIGN KEY (document_id)
                REFERENCES documents(document_id)
                ON DELETE CASCADE
        )
        """,

        # -------------------------------------------------
        # Document → Sectors
        # -------------------------------------------------

        """
        CREATE TABLE IF NOT EXISTS document_sectors (
            document_id TEXT NOT NULL,
            sector_code TEXT NOT NULL,

            PRIMARY KEY (
                document_id,
                sector_code
            ),

            FOREIGN KEY (document_id)
                REFERENCES documents(document_id)
                ON DELETE CASCADE
        )
        """,

        # -------------------------------------------------
        # Document → Policy Domains
        # -------------------------------------------------

        """
        CREATE TABLE IF NOT EXISTS document_policy_domains (
            document_id TEXT NOT NULL,
            policy_domain_code TEXT NOT NULL,

            PRIMARY KEY (
                document_id,
                policy_domain_code
            ),

            FOREIGN KEY (document_id)
                REFERENCES documents(document_id)
                ON DELETE CASCADE
        )
        """,

        # -------------------------------------------------
        # Document → Topics
        # -------------------------------------------------

        """
        CREATE TABLE IF NOT EXISTS document_topics (
            document_id TEXT NOT NULL,
            topic_code TEXT NOT NULL,

            PRIMARY KEY (
                document_id,
                topic_code
            ),

            FOREIGN KEY (document_id)
                REFERENCES documents(document_id)
                ON DELETE CASCADE
        )
        """,

        # -------------------------------------------------
        # Jobs
        # -------------------------------------------------

        """
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_type TEXT NOT NULL,
            status TEXT NOT NULL,
            started_at TEXT,
            completed_at TEXT,
            error TEXT
        )
        """,
    ]

    with engine.begin() as connection:
        # SQLite foreign keys are disabled by default.
        if connection.engine.url.get_backend_name() == "sqlite":
            connection.execute(
                text("PRAGMA foreign_keys = ON")
            )

        for statement in statements:
            connection.execute(text(statement))


def database_health() -> dict:
    engine = get_engine()

    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "status": "connected",
        "engine": "sqlite",
    }
