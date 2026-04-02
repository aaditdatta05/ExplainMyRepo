from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="EXPLAIN_MY_REPO_",
        extra="ignore",
    )

    env: str = Field(default="development")
    log_level: str = Field(default="INFO")
    openai_api_key: str = Field(default="")
    llm_timeout_seconds: float = Field(default=20.0)
    llm_max_retries: int = Field(default=2)
    llm_base_backoff_seconds: float = Field(default=0.5)
    cache_ttl_seconds: int = Field(default=300)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
