from supportops_model_gateway.errors import UnsupportedModelProviderError
from supportops_model_gateway.providers.base import TicketAnalysisProvider
from supportops_model_gateway.providers.mock import MOCK_PROVIDER_NAME, MockTicketAnalysisProvider


def build_ticket_analysis_provider(provider_name: str) -> TicketAnalysisProvider:
    normalized = provider_name.strip().lower()
    if normalized == MOCK_PROVIDER_NAME:
        return MockTicketAnalysisProvider()
    raise UnsupportedModelProviderError(f"unsupported model provider: {provider_name}")

