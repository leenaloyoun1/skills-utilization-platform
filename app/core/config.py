"""Central application configuration."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Skills Utilization Platform"
    app_env: str = "development"
    debug: bool = True

    database_url: str

    embedding_model: str = (
        "sentence-transformers/all-MiniLM-L6-v2"
    )
    default_top_n: int = 3

    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()