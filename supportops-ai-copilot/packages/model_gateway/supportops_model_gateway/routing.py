from supportops_model_gateway.errors import UnsupportedModelProviderError
from supportops_model_gateway.providers.base import TicketAnalysisProvider
from supportops_model_gateway.providers.hosted import (
    DEFAULT_MAX_OUTPUT_TOKENS,
    DEFAULT_OPENAI_BASE_URL,
    DEFAULT_OPENAI_MODEL,
    DEFAULT_TIMEOUT_SECONDS,
    HOSTED_PROVIDER_ALIAS,
    OPENAI_PROVIDER_NAME,
    HostedTicketAnalysisProvider,
)
from supportops_model_gateway.providers.mock import MOCK_PROVIDER_NAME, MockTicketAnalysisProvider


def build_ticket_analysis_provider(
    provider_name: str,
    *,
    api_key: str = "",
    model_name: str = DEFAULT_OPENAI_MODEL,
    base_url: str = DEFAULT_OPENAI_BASE_URL,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    max_output_tokens: int = DEFAULT_MAX_OUTPUT_TOKENS,
) -> TicketAnalysisProvider:
    normalized = provider_name.strip().lower()
    if normalized == MOCK_PROVIDER_NAME:
        return MockTicketAnalysisProvider()
    if normalized in {OPENAI_PROVIDER_NAME, HOSTED_PROVIDER_ALIAS}:
        return HostedTicketAnalysisProvider(
            api_key=api_key,
            model_name=model_name,
            base_url=base_url,
            timeout_seconds=timeout_seconds,
            max_output_tokens=max_output_tokens,
        )
    raise UnsupportedModelProviderError(f"unsupported model provider: {provider_name}")
