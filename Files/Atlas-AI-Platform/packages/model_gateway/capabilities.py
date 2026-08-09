"""Provider capability matrix and capability gating.

Phase 01 planned this module and deferred it, which left capability data sitting
unread in `model_providers.capabilities_json`. The gap matters because the
alternative to checking capabilities is discovering them from a provider error:
ask a model that cannot do structured output for structured output and you get a
500 from the provider, an `ai_runs` row marked failed, and a billed call.

Gating turns that into a refusal before the request leaves the process.

Phase 03 is the first real consumer — it must know whether a route supports
native structured output, a JSON mode, or neither, before it picks a strategy.

Python notes for .NET reviewers:
- `frozenset` is an immutable set, usable as a dictionary key or default value.
- `StrEnum` members compare equal to their string value, which keeps the JSON
  round-trip simple.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from packages.model_gateway.errors import CapabilityNotSupportedError
from packages.model_gateway.types import SelectedRoute


class Capability(StrEnum):
    """One provider feature that a route may or may not support.

    The values match the keys already written into `capabilities_json` by
    `bootstrap.py`, so existing seeded rows are readable without a migration.
    """

    CHAT = "supports_chat"
    EMBEDDINGS = "supports_embeddings"
    STRUCTURED_OUTPUT = "supports_structured_output"
    STREAMING = "supports_streaming"
    TOOL_CALLING = "supports_tool_calling"
    PROMPT_CACHING = "supports_prompt_caching"
    BATCH_API = "supports_batch_api"
    REASONING_CONTROLS = "supports_reasoning_controls"


@dataclass(frozen=True, slots=True)
class CapabilityMatrix:
    """The capability set a single route actually offers."""

    supported: frozenset[Capability]

    def supports(self, capability: Capability) -> bool:
        return capability in self.supported

    def missing(self, required: Iterable[Capability]) -> tuple[Capability, ...]:
        """Return the required capabilities this route does not have.

        Returning the full set rather than the first failure means a caller can
        report everything wrong with a route in one message instead of making
        the user fix one capability at a time.
        """
        return tuple(item for item in required if item not in self.supported)


def matrix_from_capabilities(capabilities: Mapping[str, Any]) -> CapabilityMatrix:
    """Build a CapabilityMatrix from a route's `capabilities` JSON.

    Unknown keys are ignored rather than rejected: a provider row written by a
    newer version of the platform must not break an older reader.
    """
    supported = {
        capability
        for capability in Capability
        if bool(capabilities.get(capability.value, False))
    }
    return CapabilityMatrix(supported=frozenset(supported))


def required_capabilities_for_operation(operation: str) -> frozenset[Capability]:
    """Map a gateway operation onto the capabilities it cannot run without."""
    if operation == "embed":
        return frozenset({Capability.EMBEDDINGS})
    if operation == "structured":
        # Structured output still needs a chat-capable model underneath it.
        return frozenset({Capability.CHAT, Capability.STRUCTURED_OUTPUT})
    return frozenset({Capability.CHAT})


def ensure_route_supports(route: SelectedRoute, *, operation: str) -> None:
    """Raise CapabilityNotSupportedError when a route cannot run an operation."""
    matrix = matrix_from_capabilities(route.capabilities)
    missing = matrix.missing(required_capabilities_for_operation(operation))
    if missing:
        raise CapabilityNotSupportedError(
            {
                "route_key": route.route_key,
                "provider_name": route.provider_name,
                "operation": operation,
                "missing_capabilities": [capability.value for capability in missing],
            }
        )
