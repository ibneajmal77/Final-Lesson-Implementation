import json
import time
from typing import Any

import httpx
from pydantic import ValidationError

from supportops_model_gateway.errors import (
    ModelProviderConfigurationError,
    ModelProviderRequestError,
    ModelProviderResponseError,
)
from supportops_model_gateway.providers.base import TicketAnalysisInput, TicketAnalysisResult
from supportops_prompts.registry import get_prompt, render_prompt
from supportops_prompts.schemas import FullTicketAnalysis

OPENAI_PROVIDER_NAME = "openai"
HOSTED_PROVIDER_ALIAS = "hosted"
OPENAI_SOURCE = "openai_responses_v1"
DEFAULT_OPENAI_MODEL = "gpt-5.6"
DEFAULT_OPENAI_BASE_URL = "https://api.openai.com/v1"
DEFAULT_TIMEOUT_SECONDS = 30.0
DEFAULT_MAX_OUTPUT_TOKENS = 1200
FULL_ANALYSIS_PROMPT_NAME = "full_ticket_analysis"
FULL_ANALYSIS_SCHEMA_NAME = "supportops_full_ticket_analysis"


class HostedTicketAnalysisProvider:
    def __init__(
        self,
        *,
        api_key: str,
        model_name: str = DEFAULT_OPENAI_MODEL,
        base_url: str = DEFAULT_OPENAI_BASE_URL,
        timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
        max_output_tokens: int = DEFAULT_MAX_OUTPUT_TOKENS,
        http_client: httpx.Client | None = None,
    ) -> None:
        if not api_key.strip():
            raise ModelProviderConfigurationError(
                "MODEL_API_KEY is required when MODEL_PROVIDER=openai"
            )
        if not model_name.strip():
            raise ModelProviderConfigurationError("MODEL_NAME is required")
        if timeout_seconds <= 0:
            raise ModelProviderConfigurationError("MODEL_TIMEOUT_SECONDS must be greater than 0")
        if max_output_tokens <= 0:
            raise ModelProviderConfigurationError("MODEL_MAX_OUTPUT_TOKENS must be greater than 0")

        self._api_key = api_key
        self._model_name = model_name
        self._base_url = base_url.rstrip("/")
        self._timeout_seconds = timeout_seconds
        self._max_output_tokens = max_output_tokens
        self._http_client = http_client or httpx.Client()

    def analyze_ticket(self, ticket: TicketAnalysisInput) -> TicketAnalysisResult:
        prompt_spec = get_prompt(FULL_ANALYSIS_PROMPT_NAME)
        prompt = render_prompt(
            FULL_ANALYSIS_PROMPT_NAME,
            {
                "ticket_subject": ticket.subject,
                "ticket_body": ticket.body,
                "customer_id": ticket.customer_id or "unknown",
                "policy_context": ticket.policy_context or "No policy context provided.",
            },
        )
        request_payload = self._build_request_payload(
            prompt=prompt,
            prompt_id=prompt_spec.prompt_id,
        )

        started = time.perf_counter()
        response_payload = self._post_response(request_payload)
        latency_ms = int((time.perf_counter() - started) * 1000)

        output_text = _extract_output_text(response_payload)
        analysis = _parse_analysis(output_text)
        usage = _extract_usage(response_payload)
        raw_response_id = _string_or_none(response_payload.get("id"))

        return _analysis_to_result(
            analysis=analysis,
            ticket=ticket,
            model_name=_string_or_none(response_payload.get("model")) or self._model_name,
            prompt_version=prompt_spec.prompt_id,
            input_tokens=usage["input_tokens"],
            output_tokens=usage["output_tokens"],
            latency_ms=latency_ms,
            raw_response_id=raw_response_id,
        )

    def _build_request_payload(self, *, prompt: str, prompt_id: str) -> dict[str, Any]:
        return {
            "model": self._model_name,
            "input": prompt,
            "max_output_tokens": self._max_output_tokens,
            "store": False,
            "metadata": {
                "prompt_id": prompt_id,
                "schema_name": FULL_ANALYSIS_SCHEMA_NAME,
            },
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": FULL_ANALYSIS_SCHEMA_NAME,
                    "strict": True,
                    "schema": FullTicketAnalysis.model_json_schema(),
                }
            },
        }

    def _post_response(self, payload: dict[str, Any]) -> dict[str, Any]:
        try:
            response = self._http_client.post(
                f"{self._base_url}/responses",
                headers={
                    "Authorization": f"Bearer {self._api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=self._timeout_seconds,
            )
            response.raise_for_status()
        except httpx.TimeoutException as exc:
            raise ModelProviderRequestError("hosted model request timed out") from exc
        except httpx.HTTPStatusError as exc:
            detail = exc.response.text[:500]
            raise ModelProviderRequestError(
                f"hosted model request failed with HTTP {exc.response.status_code}: {detail}"
            ) from exc
        except httpx.HTTPError as exc:
            raise ModelProviderRequestError("hosted model request failed") from exc

        try:
            parsed = response.json()
        except json.JSONDecodeError as exc:
            raise ModelProviderResponseError("hosted model returned non-JSON response") from exc
        if not isinstance(parsed, dict):
            raise ModelProviderResponseError("hosted model response must be a JSON object")
        return parsed


def _extract_output_text(payload: dict[str, Any]) -> str:
    error = payload.get("error")
    if error:
        raise ModelProviderResponseError(f"hosted model returned error: {error}")

    status = payload.get("status")
    if status not in (None, "completed"):
        raise ModelProviderResponseError(f"hosted model response status was {status!r}")

    output_text = payload.get("output_text")
    if isinstance(output_text, str) and output_text.strip():
        return output_text

    texts: list[str] = []
    output = payload.get("output")
    if not isinstance(output, list):
        raise ModelProviderResponseError("hosted model response missing output items")

    for item in output:
        if not isinstance(item, dict):
            continue
        content = item.get("content")
        if not isinstance(content, list):
            continue
        for part in content:
            if not isinstance(part, dict):
                continue
            refusal = part.get("refusal")
            if part.get("type") == "refusal" or isinstance(refusal, str):
                raise ModelProviderResponseError("hosted model refused the request")
            if part.get("type") == "output_text" and isinstance(part.get("text"), str):
                texts.append(part["text"])

    text = "".join(texts).strip()
    if not text:
        raise ModelProviderResponseError("hosted model response did not include output text")
    return text


def _parse_analysis(output_text: str) -> FullTicketAnalysis:
    try:
        return FullTicketAnalysis.model_validate_json(output_text)
    except ValidationError as exc:
        raise ModelProviderResponseError("hosted model returned invalid ticket analysis") from exc


def _extract_usage(payload: dict[str, Any]) -> dict[str, int]:
    usage = payload.get("usage")
    if not isinstance(usage, dict):
        return {"input_tokens": 0, "output_tokens": 0}
    return {
        "input_tokens": _int_or_zero(usage.get("input_tokens")),
        "output_tokens": _int_or_zero(usage.get("output_tokens")),
    }


def _analysis_to_result(
    *,
    analysis: FullTicketAnalysis,
    ticket: TicketAnalysisInput,
    model_name: str,
    prompt_version: str,
    input_tokens: int,
    output_tokens: int,
    latency_ms: int,
    raw_response_id: str | None,
) -> TicketAnalysisResult:
    extracted_fields = analysis.extracted_fields.model_dump(mode="json")
    extracted_fields.update(
        {
            "customer_id": ticket.customer_id,
            "provider": OPENAI_PROVIDER_NAME,
            "evidence_ids": analysis.evidence_ids,
            "risk_flags": list(analysis.risk_flags),
            "abstain": analysis.abstain,
            "raw_response_id": raw_response_id,
            "model_usage": {
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
            },
        }
    )

    suggested_reply = ""
    if analysis.draft_response is not None:
        suggested_reply = analysis.draft_response.response_text

    return TicketAnalysisResult(
        source=OPENAI_SOURCE,
        model_name=model_name,
        prompt_version=prompt_version,
        category=analysis.category,
        priority=analysis.priority,
        requires_escalation=analysis.requires_escalation,
        confidence=analysis.category_confidence,
        summary=_summary_for_analysis(analysis),
        suggested_reply=suggested_reply,
        extracted_fields=extracted_fields,
        reasons=_reasons_for_analysis(analysis),
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        latency_ms=latency_ms,
        raw_response_id=raw_response_id,
    )


def _summary_for_analysis(analysis: FullTicketAnalysis) -> str:
    if analysis.abstain:
        return "Model abstained because the ticket needs more information."
    return (
        f"Customer ticket classified as {analysis.category} with "
        f"{analysis.priority} priority."
    )


def _reasons_for_analysis(analysis: FullTicketAnalysis) -> list[str]:
    reasons = [
        "Hosted OpenAI model returned a structured full-ticket analysis.",
        f"Category confidence: {analysis.category_confidence:.2f}.",
    ]
    risk_flags = [flag for flag in analysis.risk_flags if flag != "none"]
    if risk_flags:
        reasons.append(f"Risk flags: {', '.join(risk_flags)}.")
    if analysis.missing_information:
        reasons.append(f"Missing information: {', '.join(analysis.missing_information)}.")
    if analysis.abstain:
        reasons.append("Model abstained from a complete recommendation.")
    return reasons


def _int_or_zero(value: object) -> int:
    return value if isinstance(value, int) else 0


def _string_or_none(value: object) -> str | None:
    return value if isinstance(value, str) and value else None
