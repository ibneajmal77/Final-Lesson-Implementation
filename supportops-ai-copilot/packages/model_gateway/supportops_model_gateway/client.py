# ============================================================================
# FILE: packages/model_gateway/supportops_model_gateway/client.py
#
# THINK OF THIS FILE AS: a convenience wrapper — "build the right provider and
# hold on to it", in one object.
#
# WORTH KNOWING BEFORE YOU SPEND TIME HERE: nothing in the running application
# actually uses this class. routes/tickets.py and apps/worker/jobs.py both call
# build_ticket_analysis_provider() from routing.py directly.
#
# WHY IT EXISTS ANYWAY:
#   It offers a slightly friendlier shape for anyone who wants to make several
#   analysis calls in a row: construct one client, then call analyze_ticket()
#   repeatedly, without re-selecting the provider each time. That suits scripts
#   and experiments better than the factory function does.
#
#   The application code does not need that, because it configures a provider
#   per request anyway — settings can change between requests, and the pilot
#   kill switch is meant to take effect immediately.
#
# A pattern worth recognising in general: a thin "facade" over a factory. Useful
# when it earns its place; dead weight when it does not. This one currently sits
# in the second category, which is worth knowing before you assume changing it
# would affect the running system.
# ============================================================================

from supportops_model_gateway.providers.base import TicketAnalysisInput, TicketAnalysisResult
from supportops_model_gateway.providers.hosted import (
    # Imported purely to reuse as this constructor's defaults, so the fallback
    # values are defined once and cannot drift.
    DEFAULT_MAX_OUTPUT_TOKENS,
    DEFAULT_OPENAI_BASE_URL,
    DEFAULT_OPENAI_MODEL,
    DEFAULT_TIMEOUT_SECONDS,
)
from supportops_model_gateway.routing import build_ticket_analysis_provider


class ModelGatewayClient:
    # Chooses the provider ONCE, at construction, and remembers it.
    #
    # That is the only real difference from calling routing.py yourself: the
    # selection happens up front instead of on every call. It also means a
    # configuration error — a bad provider name, a missing API key — surfaces
    # immediately when the client is created, rather than on first use.
    def __init__(
        self,
        provider_name: str,
        *,                        # everything after must be named, so the API key cannot
                                  # accidentally be passed into the model_name slot
        api_key: str = "",
        model_name: str = DEFAULT_OPENAI_MODEL,
        base_url: str = DEFAULT_OPENAI_BASE_URL,
        timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
        max_output_tokens: int = DEFAULT_MAX_OUTPUT_TOKENS,
    ) -> None:
        # The single underscore prefix is a convention meaning "internal — do not
        # use this from outside the class".
        self._provider = build_ticket_analysis_provider(
            provider_name,
            api_key=api_key,
            model_name=model_name,
            base_url=base_url,
            timeout_seconds=timeout_seconds,
            max_output_tokens=max_output_tokens,
        )

    # Passes the call straight through to whichever provider was chosen.
    #
    # A "delegating" method: it adds no behaviour of its own. Its value is that
    # this class ends up satisfying the same TicketAnalysisProvider contract as
    # the providers themselves, so it can be used anywhere one is expected.
    def analyze_ticket(self, ticket: TicketAnalysisInput) -> TicketAnalysisResult:
        return self._provider.analyze_ticket(ticket)
