from supportops_model_gateway.providers.base import TicketAnalysisInput, TicketAnalysisResult
from supportops_model_gateway.routing import build_ticket_analysis_provider


class ModelGatewayClient:
    def __init__(self, provider_name: str) -> None:
        self._provider = build_ticket_analysis_provider(provider_name)

    def analyze_ticket(self, ticket: TicketAnalysisInput) -> TicketAnalysisResult:
        return self._provider.analyze_ticket(ticket)

