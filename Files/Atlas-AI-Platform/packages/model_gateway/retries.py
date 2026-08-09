"""Retry policy: backoff, jitter, and retry classification.

Phase 01 planned this module and shipped only the loop, inside `client.py`.
That loop retried immediately, which is the failure mode worth naming: when a
provider is rate limiting or briefly overloaded, an instant retry arrives while
the same condition still holds, and N callers retrying in lockstep turn one
spike into a self-inflicted stampede.

The policy here is exponential backoff with **full jitter**: the delay is drawn
uniformly from `[0, exponential_ceiling]` rather than being exactly the ceiling.
Equal-length sleeps would keep concurrent callers synchronized; randomizing the
wait is what actually spreads them out.

Everything except `sleep()` is pure, so the timing rules are unit-testable
without a clock, a provider, or a database.

Python notes for .NET reviewers:
- `@dataclass(frozen=True)` is close to a C# `readonly record struct`.
- `random.Random` is an explicit RNG instance, so tests can seed it and get
  deterministic draws instead of patching the global module.
"""

from __future__ import annotations

import random
import time
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

DEFAULT_BASE_DELAY_SECONDS = 0.25
DEFAULT_MAX_DELAY_SECONDS = 8.0
DEFAULT_MAX_RETRIES = 1


@dataclass(frozen=True, slots=True)
class RetryPolicy:
    """Per-route retry timing rules, resolved from `route_config`."""

    max_retries: int = DEFAULT_MAX_RETRIES
    base_delay_seconds: float = DEFAULT_BASE_DELAY_SECONDS
    max_delay_seconds: float = DEFAULT_MAX_DELAY_SECONDS
    jitter: bool = True

    @property
    def max_attempts(self) -> int:
        """Total provider calls allowed: the first attempt plus the retries."""
        return self.max_retries + 1


def policy_from_route_config(route_config: Mapping[str, Any]) -> RetryPolicy:
    """Read a RetryPolicy out of a route's JSON config, falling back to defaults.

    Routes seeded before this module existed only carry `max_retries`, so every
    other field has to degrade to a default rather than raise.
    """
    return RetryPolicy(
        max_retries=_as_int(route_config.get("max_retries"), DEFAULT_MAX_RETRIES),
        base_delay_seconds=_as_float(
            route_config.get("retry_base_delay_seconds"),
            DEFAULT_BASE_DELAY_SECONDS,
        ),
        max_delay_seconds=_as_float(
            route_config.get("retry_max_delay_seconds"),
            DEFAULT_MAX_DELAY_SECONDS,
        ),
        # Jitter is opt-out rather than opt-in: a route has to ask for
        # deterministic timing explicitly, and only tests should want that.
        jitter=bool(route_config.get("retry_jitter", True)),
    )


def compute_backoff_delay(
    attempt_number: int,
    policy: RetryPolicy,
    *,
    rng: random.Random | None = None,
) -> float:
    """Return how long to wait before the retry that follows `attempt_number`.

    `attempt_number` is 1-based, so the wait after the first failed call uses
    the base delay, the next doubles it, and so on up to `max_delay_seconds`.
    With jitter enabled the result is a uniform draw from `[0, ceiling]`.
    """
    if attempt_number < 1 or policy.base_delay_seconds <= 0:
        return 0.0
    # `2.0 **` rather than `2 **`: an int base with a non-literal int exponent
    # is typed as returning Any, because a negative exponent would produce a
    # float. Using a float base keeps the whole expression statically a float.
    exponential = policy.base_delay_seconds * (2.0 ** (attempt_number - 1))
    ceiling = min(exponential, policy.max_delay_seconds)
    if not policy.jitter:
        return ceiling
    generator = rng or random.Random()
    return generator.uniform(0.0, ceiling)


def sleep(seconds: float) -> None:
    """Block for `seconds`. Isolated so tests can patch exactly one symbol.

    This is the only impure function in the module, and it is only ever called
    from the synchronous gateway. The async gateway awaits `asyncio.sleep`
    instead — blocking here would stall the whole event loop.
    """
    if seconds > 0:
        time.sleep(seconds)


def _as_int(value: object, fallback: int) -> int:
    """Coerce a JSON config value to int, falling back rather than raising.

    `bool` is excluded explicitly because it subclasses `int` in Python, so a
    stray `true` would otherwise silently become `max_retries=1`.
    """
    if isinstance(value, bool):
        return fallback
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            return fallback
    return fallback


def _as_float(value: object, fallback: float) -> float:
    """Coerce a JSON config value to float, falling back rather than raising."""
    if isinstance(value, bool):
        return fallback
    if isinstance(value, int | float):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return fallback
    return fallback
