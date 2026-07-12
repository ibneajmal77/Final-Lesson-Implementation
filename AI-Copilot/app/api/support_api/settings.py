from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "supportops-ai-copilot"
    app_env: str = "local"
    log_level: str = "INFO"
    database_url: str = "postgresql://supportops:supportops@localhost:5432/supportops"
    redis_url: str = "redis://localhost:6379/0"
    model_provider: str = "mock"
    model_api_key: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def getting_settings() -> Settings:
    return Settings()