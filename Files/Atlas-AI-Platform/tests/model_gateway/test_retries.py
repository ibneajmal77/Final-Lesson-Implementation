"""Retry timing tests.

The retry loop used to fire again with no delay at all. These tests pin the
behavior that replaced it, and they run without a clock: `compute_backoff_delay`
is pure, so the timing rules are asserted by arithmetic rather than by sleeping.
"""

from __future__ import annotations

import random

import pytest

from packages.model_gateway.retries import (
    DEFAULT_BASE_DELAY_SECONDS,
    RetryPolicy,
    compute_backoff_delay,
    policy_from_route_config,
    sleep,
)


def test_policy_defaults_apply_when_route_config_is_empty() -> None:
    """Routes seeded before this module existed must still get a policy."""
    policy = policy_from_route_config({})

    assert policy.max_retries == 1
    assert policy.max_attempts == 2
    assert policy.base_delay_seconds == DEFAULT_BASE_DELAY_SECONDS
    assert policy.jitter is True


def test_policy_reads_overrides_from_route_config() -> None:
    policy = policy_from_route_config(
        {
            "max_retries": 4,
            "retry_base_delay_seconds": 0.1,
            "retry_max_delay_seconds": 2.0,
            "retry_jitter": False,
        }
    )

    assert policy.max_retries == 4
    assert policy.max_attempts == 5
    assert policy.base_delay_seconds == 0.1
    assert policy.max_delay_seconds == 2.0
    assert policy.jitter is False


def test_unparseable_route_config_values_fall_back_instead_of_raising() -> None:
    """A bad JSON value must not take down a request that could have run."""
    policy = policy_from_route_config(
        {"max_retries": "not-a-number", "retry_base_delay_seconds": None}
    )

    assert policy.max_retries == 1
    assert policy.base_delay_seconds == DEFAULT_BASE_DELAY_SECONDS


def test_delay_doubles_per_attempt_when_jitter_is_disabled() -> None:
    policy = RetryPolicy(base_delay_seconds=0.5, max_delay_seconds=100.0, jitter=False)

    assert compute_backoff_delay(1, policy) == 0.5
    assert compute_backoff_delay(2, policy) == 1.0
    assert compute_backoff_delay(3, policy) == 2.0
    assert compute_backoff_delay(4, policy) == 4.0


def test_delay_is_capped_at_max_delay_seconds() -> None:
    """Unbounded doubling would eventually park a request for minutes."""
    policy = RetryPolicy(base_delay_seconds=1.0, max_delay_seconds=4.0, jitter=False)

    assert compute_backoff_delay(3, policy) == 4.0
    assert compute_backoff_delay(10, policy) == 4.0


def test_jitter_keeps_delays_within_the_ceiling_and_varies_them() -> None:
    """Full jitter is what stops concurrent callers retrying in lockstep."""
    policy = RetryPolicy(base_delay_seconds=1.0, max_delay_seconds=8.0, jitter=True)
    rng = random.Random(1234)

    delays = [compute_backoff_delay(2, policy, rng=rng) for _ in range(50)]

    # Attempt 2 has a ceiling of 1.0 * 2**1 == 2.0.
    assert all(0.0 <= delay <= 2.0 for delay in delays)
    # If every draw were identical the jitter would not be spreading anything.
    assert len(set(delays)) > 1


def test_jitter_draw_is_deterministic_for_a_seeded_generator() -> None:
    policy = RetryPolicy(base_delay_seconds=1.0, jitter=True)

    first = compute_backoff_delay(1, policy, rng=random.Random(7))
    second = compute_backoff_delay(1, policy, rng=random.Random(7))

    assert first == second


@pytest.mark.parametrize("attempt_number", [0, -1])
def test_non_positive_attempt_numbers_produce_no_delay(attempt_number: int) -> None:
    assert compute_backoff_delay(attempt_number, RetryPolicy()) == 0.0


def test_zero_base_delay_disables_backoff_entirely() -> None:
    """Tests and local runs need an escape hatch that costs no wall-clock time."""
    policy = policy_from_route_config({"retry_base_delay_seconds": 0})

    assert compute_backoff_delay(1, policy) == 0.0
    assert compute_backoff_delay(5, policy) == 0.0


def test_sleep_ignores_non_positive_durations() -> None:
    """A zero delay must not become a syscall on the hot path."""
    sleep(0.0)
    sleep(-1.0)
