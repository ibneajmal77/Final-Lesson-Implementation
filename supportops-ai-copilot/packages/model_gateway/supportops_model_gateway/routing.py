# ============================================================================
# FILE: packages/model_gateway/supportops_model_gateway/routing.py
#
# THINK OF THIS FILE AS: the switchboard. One small function that turns the
# setting `model_provider` into an actual object capable of talking to an AI.
#
# WHY IT MATTERS MORE THAN ITS SIZE SUGGESTS:
#   This is the ONE place in the entire codebase that knows which AI providers
#   exist. Routes and worker code call build_ticket_analysis_provider() and get
#   back something honouring the contract in providers/base.py — they never
#   mention a provider by name.
#
#   The consequence: switching the whole system from a fake AI to a real paid one
#   is a single environment variable, with no code change anywhere. And adding a
#   third provider means writing one new file and adding one `if` below.
#
# A pattern with a name — a "factory function": something whose job is to decide
# which concrete class to build, so callers can depend on the contract instead.
#
# WHO CALLS IT:
#   routes/tickets.py    - the synchronous AI endpoint
#   apps/worker/jobs.py  - the queued analysis job
#   packages/evals/      - the evaluation harness
# ============================================================================

from supportops_model_gateway.errors import UnsupportedModelProviderError
from supportops_model_gateway.providers.base import TicketAnalysisProvider
from supportops_model_gateway.providers.hosted import (
    # The DEFAULT_* values are imported to use as this function's own defaults,
    # so the fallback values are defined once, next to the code that uses them,
    # rather than being repeated here and drifting apart later.
    DEFAULT_MAX_OUTPUT_TOKENS,
    DEFAULT_OPENAI_BASE_URL,
    DEFAULT_OPENAI_MODEL,
    DEFAULT_TIMEOUT_SECONDS,
    HOSTED_PROVIDER_ALIAS,
    OPENAI_PROVIDER_NAME,
    HostedTicketAnalysisProvider,
)
from supportops_model_gateway.providers.mock import MOCK_PROVIDER_NAME, MockTicketAnalysisProvider


# Builds the right provider for the requested name.
#
# The return type is the PROTOCOL (TicketAnalysisProvider), not a concrete class.
# That is the whole point: the caller is told "you will get something that can
# analyse a ticket", and deliberately not told what it actually is.
def build_ticket_analysis_provider(
    provider_name: str,
    *,                        # everything after this must be named. With two strings,
                              # a float and an int, positional order would be easy to
                              # get wrong — and passing the API key into the wrong
                              # parameter is a mistake worth designing out
    api_key: str = "",
    model_name: str = DEFAULT_OPENAI_MODEL,
    base_url: str = DEFAULT_OPENAI_BASE_URL,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    max_output_tokens: int = DEFAULT_MAX_OUTPUT_TOKENS,
) -> TicketAnalysisProvider:
    # Tidy the name so " Mock " and "MOCK" both work. Small courtesy that
    # prevents a whole category of baffling deployment failures, where a stray
    # space in an environment variable makes a valid setting look unrecognised.
    normalized = provider_name.strip().lower()

    # THE FAKE. Returns canned answers without touching the network.
    #
    # Note it takes NO arguments — no key, no model, no timeout, because it needs
    # none of them. Any configuration passed in is simply ignored, which is
    # exactly right: the mock must work when nothing at all is configured. That
    # is what lets the entire test suite run with no API key.
    if normalized == MOCK_PROVIDER_NAME:
        return MockTicketAnalysisProvider()

    # THE REAL ONE. Two accepted names — "openai" and a friendlier alias,
    # "hosted" — pointing at the same implementation. The alias exists so that
    # configuration and documentation can talk about a "hosted provider" in
    # general terms without naming a specific vendor everywhere.
    if normalized in {OPENAI_PROVIDER_NAME, HOSTED_PROVIDER_ALIAS}:
        return HostedTicketAnalysisProvider(
            api_key=api_key,
            model_name=model_name,
            base_url=base_url,
            timeout_seconds=timeout_seconds,
            max_output_tokens=max_output_tokens,
        )

    # An unrecognised name. Failing loudly here is the right behaviour: quietly
    # falling back to the mock would be far worse, because the system would
    # appear to work while producing meaningless canned answers, and nobody would
    # notice until a customer received one.
    #
    # Note the original name is echoed back, not the tidied one — so the message
    # shows exactly what was configured, which is what the person fixing it needs.
    raise UnsupportedModelProviderError(f"unsupported model provider: {provider_name}")
