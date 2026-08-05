"""Unit tests for environment-backed settings.

The `monkeypatch` fixture is pytest's temporary environment/config mutation
helper; changes are automatically undone after each test.
"""

import pytest
from pydantic import ValidationError

from packages.core.config import Settings

ATLAS_ENV_KEYS = [
    "ATLAS_ENV",
    "ATLAS_APP_NAME",
    "ATLAS_API_HOST",
    "ATLAS_API_PORT",
    "ATLAS_API_PREFIX",
    "ATLAS_DATABASE_URL",
    "ATLAS_REDIS_URL",
    "ATLAS_LOG_LEVEL",
    "ATLAS_MODEL_GATEWAY_ENABLE_MANAGED_PROVIDER",
    "ATLAS_OPENAI_COMPATIBLE_API_KEY",
]


def test_settings_defaults_are_local_safe(monkeypatch) -> None:
    for key in ATLAS_ENV_KEYS:
        monkeypatch.delenv(key, raising=False)

    settings = Settings(_env_file=None)

    assert settings.env == "local"
    assert settings.app_name == "Atlas AI Platform"
    assert settings.api_prefix == "/api/v1"
    assert "postgresql+psycopg" in settings.database_url
    assert settings.model_gateway_enable_managed_provider is False
    assert settings.openai_compatible_api_key is None


def test_api_prefix_is_normalized() -> None:
    settings = Settings(_env_file=None, api_prefix="api/custom/")

    assert settings.api_prefix == "/api/custom"


def test_api_prefix_cannot_be_empty() -> None:
    with pytest.raises(ValidationError):
        Settings(_env_file=None, api_prefix="   ")
