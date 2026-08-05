"""Provider adapter implementations.

Provider modules implement the `ProviderAdapter` protocol, similar to multiple
classes implementing a common C# interface for model vendors.
"""

from packages.model_gateway.providers.base import ProviderAdapter
from packages.model_gateway.providers.mock import MockProvider
from packages.model_gateway.providers.openai_compatible import OpenAICompatibleProvider

__all__ = ["MockProvider", "OpenAICompatibleProvider", "ProviderAdapter"]
