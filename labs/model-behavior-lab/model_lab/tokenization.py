# model_lab/tokenization.py
from __future__ import annotations

import re
from typing import Any

from .schemas import TokenReport

TOKEN_PATTERN = re.compile(r"\w+|[^\w\s]", re.UNICODE)


def simple_tokens(text: str) -> list[str]:
    return TOKEN_PATTERN.findall(text)


def simple_token_count(text: str) -> int:
    return len(simple_tokens(text))


def inspect_with_simple_tokenizer(text: str) -> TokenReport:
    tokens = simple_tokens(text)
    return TokenReport(
        tokenizer="simple_regex",
        text_chars=len(text),
        token_count=len(tokens),
        tokens=tokens,
        token_ids=list(range(len(tokens))),
    )


def inspect_with_hf_tokenizer(
    *,
    model_id: str,
    text: str,
    revision: str | None = None,
) -> TokenReport:
    from transformers import AutoTokenizer

    kwargs: dict[str, Any] = {"trust_remote_code": False}
    if revision:
        kwargs["revision"] = revision
    tokenizer = AutoTokenizer.from_pretrained(model_id, **kwargs)
    token_ids = tokenizer(text, add_special_tokens=False)["input_ids"]
    tokens = tokenizer.convert_ids_to_tokens(token_ids)
    special_tokens = list(getattr(tokenizer, "all_special_tokens", []) or [])
    return TokenReport(
        tokenizer=model_id,
        text_chars=len(text),
        token_count=len(token_ids),
        tokens=list(tokens),
        token_ids=list(token_ids),
        special_tokens=special_tokens,
    )