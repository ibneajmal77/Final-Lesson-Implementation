from supportops_model_gateway.providers.base import TicketAnalysisInput, TicketAnalysisResult
from supportops_model_gateway.providers.hosted import (
    DEFAULT_MAX_OUTPUT_TOKENS,
    DEFAULT_OPENAI_BASE_URL,
    DEFAULT_OPENAI_MODEL,
    DEFAULT_TIMEOUT_SECONDS,
)
from supportops_model_gateway.routing import build_ticket_analysis_provider


class ModelGatewayClient:
    def __init__(
        self,
        provider_name: str,
        *,
        api_key: str = "",
        model_name: str = DEFAULT_OPENAI_MODEL,
        base_url: str = DEFAULT_OPENAI_BASE_URL,
        timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
        max_output_tokens: int = DEFAULT_MAX_OUTPUT_TOKENS,
    ) -> None:
        self._provider = build_ticket_analysis_provider(
            provider_name,
            api_key=api_key,
            model_name=model_name,
            base_url=base_url,
            timeout_seconds=timeout_seconds,
            max_output_tokens=max_output_tokens,
        )

    def analyze_ticket(self, ticket: TicketAnalysisInput) -> TicketAnalysisResult:
        return self._provider.analyze_ticket(ticket)
