from dataclasses import dataclass


@dataclass(frozen=True)
class ModelUsageCost:
    input_tokens: int = 0
    output_tokens: int = 0
    estimated_cost_usd: float = 0.0

