"""Runtime configuration loaded from environment variables and `.env`.

This is closest to strongly typed `IOptions<T>` in ASP.NET Core. Pydantic reads
`ATLAS_*` variables, applies defaults for local development, and validates the
few settings that need normalization.

Python notes for .NET reviewers:
- Class attributes with type hints, such as `api_port: int`, declare model
  fields for Pydantic.
- `str | None` is a nullable string.
- Decorators like `@field_validator` attach framework behavior to a method.
"""

from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed application settings with local-safe defaults."""

    # `model_config` is Pydantic configuration, similar to options binding rules.
    model_config = SettingsConfigDict(env_prefix="ATLAS_", env_file=".env", extra="ignore")

    # `Field(default=...)` supplies a default and can also carry validation
    # metadata. Environment variables override these defaults at runtime.
    env: str = Field(default="local")
    app_name: str = Field(default="Atlas AI Platform")
    api_host: str = Field(default="0.0.0.0")
    api_port: int = Field(default=8000)
    api_prefix: str = Field(default="/api/v1")
    database_url: str = Field(
        default="postgresql+psycopg://atlas:atlas@localhost:55432/atlas?connect_timeout=3"
    )
    redis_url: str = Field(default="redis://localhost:6379/0")
    log_level: str = Field(default="INFO")
    model_gateway_enable_managed_provider: bool = Field(default=False)
    openai_compatible_api_key: str | None = Field(default=None)

    @field_validator("api_prefix")
    @classmethod
    def normalize_api_prefix(cls, value: str) -> str:
        """Normalize `/api/v1`-style prefixes as settings are loaded."""
        if not value.strip():
            raise ValueError("api_prefix must not be empty")
        normalized = value.strip()
        if not normalized.startswith("/"):
            normalized = f"/{normalized}"
        return normalized.rstrip("/") or "/"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return one cached settings object per process.

    `@lru_cache` memoizes the function result. That gives callers a cheap
    singleton-like settings instance without a global mutable object.
    """
    return Settings()
