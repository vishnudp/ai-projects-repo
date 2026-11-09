from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_env: str = "development"
    app_name: str = "policy-intelligence"
    log_level: str = "INFO"

    ollama_host: str = "http://localhost:11434"

    ollama_model_fast: str = "qwen3:4b"
    ollama_model_reasoning: str = "qwen3:8b"
    ollama_embedding_model: str = "nomic-embed-text:latest"

    embedding_model: str = "all-MiniLM-L6-v2" 

    database_url: str = "sqlite:///./data/policy_intelligence.db"

    llm_cache_enabled: bool = True
    embedding_cache_enabled: bool = True
    retrieval_cache_enabled: bool = True

    max_llm_workers: int = Field(default=2, ge=1)
    max_ingestion_workers: int = Field(default=5, ge=1)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()