from __future__ import annotations

from model_lab.tokenization import inspect_with_simple_tokenizer, simple_token_count, simple_tokens


def test_simple_tokenizer_splits_words_and_punctuation() -> None:
    assert simple_tokens("Order A-1049 refund?") == ["Order", "A", "-", "1049", "refund", "?"]


def test_token_count_is_not_character_count() -> None:
    text = "Refund for order A-1049?"
    assert simple_token_count(text) == 6
    assert simple_token_count(text) < len(text)


def test_token_report_contains_tokens_ids_and_counts() -> None:
    report = inspect_with_simple_tokenizer("hello world")
    assert report.token_count == 2
    assert report.tokens == ["hello", "world"]
    assert report.token_ids == [0, 1]