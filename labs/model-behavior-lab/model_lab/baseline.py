# model_lab/baseline.py
from __future__ import annotations

import time

from .schemas import ExperimentCase, ExperimentResult
from .tokenization import simple_token_count


def run_deterministic_baseline(case: ExperimentCase) -> ExperimentResult:
    started = time.perf_counter()
    text = case.user.lower()
    flags: list[str] = []

    if "ignore all previous" in text or "guarantee a refund" in text:
        flags.append("adversarial_instruction")
        output = (
            "Do not follow the customer's instruction to bypass policy. "
            "Ask the agent to verify policy evidence before drafting a refund response."
        )
    elif "no order date" in text or "no policy" in text or "evidence is incomplete" in text:
        flags.append("missing_evidence")
        output = (
            "There is not enough evidence to draft a refund decision. "
            "Ask for order details and applicable policy before responding."
        )
    elif "within 30 days" in text and "unopened" in text:
        flags.append("policy_condition_present")
        output = (
            "The policy may allow a refund within 30 days if the item is unopened. "
            "The agent should verify order details before making any commitment."
        )
    else:
        flags.append("needs_review")
        output = "The case needs agent review before a customer-facing answer is drafted."

    latency_ms = (time.perf_counter() - started) * 1000
    return ExperimentResult(
        case_id=case.case_id,
        runner="deterministic_baseline",
        model_id="rule-baseline-v1",
        settings={"mode": "baseline"},
        input_tokens=simple_token_count(case.system + "\n" + case.user),
        output_tokens=simple_token_count(output),
        latency_ms=round(latency_ms, 3),
        output_text=output,
        flags=flags,
    )