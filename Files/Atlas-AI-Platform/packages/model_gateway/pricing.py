"""Deterministic local cost estimation for gateway usage.

Real provider billing can be reconciled later, but Phase 01 records estimated
line items immediately so tests and reporting can validate cost plumbing.
"""

from decimal import ROUND_HALF_UP, Decimal

from packages.model_gateway.types import CostLine, TokenUsage

PRICING_VERSION = "phase01-2026-07"

UNIT_COSTS_USD: dict[str, Decimal] = {
    "input_token": Decimal("0.000000150"),
    "output_token": Decimal("0.000000600"),
    "reasoning_token": Decimal("0.000001000"),
    "cache_write_token": Decimal("0.000000050"),
    "cache_read_token": Decimal("0.000000010"),
    "request": Decimal("0.000000000"),
}

_MONEY_QUANT = Decimal("0.000001")


def quantize_money(value: Decimal) -> Decimal:
    """Round money consistently to six decimal places."""
    return value.quantize(_MONEY_QUANT, rounding=ROUND_HALF_UP)


def estimate_cost_lines(usage: TokenUsage) -> tuple[CostLine, ...]:
    """Convert token usage into billable line items."""
    quantities = {
        "input_token": usage.input_tokens,
        "output_token": usage.output_tokens,
        "reasoning_token": usage.reasoning_output_tokens,
        "cache_write_token": usage.cache_creation_input_tokens,
        "cache_read_token": usage.cache_read_input_tokens,
    }
    lines: list[CostLine] = []
    for billing_unit, quantity in quantities.items():
        if quantity is None or quantity <= 0:
            continue
        decimal_quantity = Decimal(quantity)
        unit_cost = UNIT_COSTS_USD[billing_unit]
        lines.append(
            CostLine(
                billing_unit=billing_unit,
                quantity=decimal_quantity,
                unit_cost_usd=unit_cost,
                estimated_cost_usd=quantize_money(decimal_quantity * unit_cost),
                pricing_version=PRICING_VERSION,
            )
        )
    return tuple(lines)


def total_estimated_cost(lines: tuple[CostLine, ...]) -> Decimal:
    """Add billable line items and keep the same money precision."""
    return quantize_money(sum((line.estimated_cost_usd for line in lines), Decimal("0")))
