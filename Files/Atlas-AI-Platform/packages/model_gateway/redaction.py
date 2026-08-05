"""Redaction, request hashing, and preview helpers.

The gateway persists enough metadata for audit and debugging, but these helpers
prevent obvious secrets, emails, and restricted-data payloads from being stored
in full.
"""

from __future__ import annotations

import hashlib
import json
import re
from typing import Any

from packages.model_gateway.types import ChatMessage, ModelRequest

_EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
_SECRET_RE = re.compile(r"(?i)\b(api[_-]?key|password|token|secret)\s*[:=]\s*\S+")


def redact_text(value: str) -> str:
    without_secrets = _SECRET_RE.sub(r"\1=[redacted]", value)
    return _EMAIL_RE.sub("[redacted-email]", without_secrets)


def preview_text(value: str, *, restricted: bool, max_length: int = 500) -> str:
    if restricted:
        return "[restricted]"
    redacted = redact_text(value).strip()
    if len(redacted) <= max_length:
        return redacted
    return redacted[: max_length - 3] + "..."


def request_hash(request: ModelRequest) -> str:
    """Hash stable request fields for deduplication/audit without storing raw text."""
    payload = {
        "tenant_id": str(request.tenant_id),
        "use_case": request.use_case,
        "messages": [{"role": msg.role, "content": msg.content} for msg in request.messages],
        "inputs": list(request.inputs),
        "restricted_data": request.restricted_data,
        "prompt_version_id": str(request.prompt_version_id) if request.prompt_version_id else None,
        "prompt_template_id": (
            str(request.prompt_template_id) if request.prompt_template_id else None
        ),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def request_preview(request: ModelRequest) -> str | None:
    """Return a redacted short text preview for the AI run ledger."""
    text = "\n".join(msg.content for msg in request.messages) or "\n".join(request.inputs)
    if not text:
        return None
    return preview_text(text, restricted=request.restricted_data)


def response_preview(content: str | None, *, restricted: bool) -> str | None:
    if content is None:
        return None
    return preview_text(content, restricted=restricted)


def redacted_request_json(request: ModelRequest) -> dict[str, Any]:
    if request.restricted_data:
        # Restricted requests store counts and routing metadata only.
        return {
            "redacted": True,
            "use_case": request.use_case,
            "message_count": len(request.messages),
            "input_count": len(request.inputs),
        }
    return {
        "use_case": request.use_case,
        "messages": [_message_to_json(message) for message in request.messages],
        "inputs": [redact_text(value) for value in request.inputs],
        "restricted_data": request.restricted_data,
        "prompt_version_id": str(request.prompt_version_id) if request.prompt_version_id else None,
        "prompt_name": request.prompt_name,
        "prompt_version_number": request.prompt_version_number,
    }


def _message_to_json(message: ChatMessage) -> dict[str, str]:
    return {"role": message.role, "content": redact_text(message.content)}


def redacted_response_json(
    *,
    content: str | None,
    embeddings_count: int,
    restricted: bool,
    metadata: dict[str, Any],
) -> dict[str, Any]:
    if restricted:
        # Preserve operational metadata, but do not persist model output text.
        return {"redacted": True, "embeddings_count": embeddings_count, **metadata}
    return {"content": redact_text(content or ""), "embeddings_count": embeddings_count, **metadata}
