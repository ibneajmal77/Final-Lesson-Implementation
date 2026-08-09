"""Seed prompt loader tests.

Phase 02's rule is that no prompt text lives in a Python module. These tests
prove the shipped seeds parse, and that a malformed seed fails loudly at load
time with the filename in the message rather than surfacing later as a KeyError
inside a render call.

No database is required — the loader is file I/O and validation only.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from packages.prompts.errors import PromptValidationError
from packages.prompts.seeds_loader import (
    SEEDS_DIRECTORY,
    load_all_seed_prompts,
    load_seed_prompt,
)


def test_shipped_seeds_directory_exists_and_is_not_empty() -> None:
    """Phase 03 adds a file to this directory, so it has to be real."""
    assert SEEDS_DIRECTORY.is_dir()
    assert list(SEEDS_DIRECTORY.glob("*.yaml"))


def test_every_shipped_seed_parses() -> None:
    seeds = load_all_seed_prompts()

    assert {seed.name for seed in seeds} == {"rag_answer_support", "classification_ticket"}
    for seed in seeds:
        assert seed.system_prompt.strip()
        assert seed.user_template.strip()


def test_seed_variables_default_to_untrusted() -> None:
    """A seed that forgets the flag must get the fenced treatment, not the raw one."""
    seeds = {seed.name: seed for seed in load_all_seed_prompts()}

    ticket = seeds["classification_ticket"]
    assert [variable.name for variable in ticket.input_variables] == ["ticket_text"]
    assert ticket.input_variables[0].trusted is False
    assert ticket.input_variables[0].required is True


def test_prompt_bodies_keep_their_exact_whitespace() -> None:
    """Stripping a body would change the rendered text and its render hash."""
    seeds = {seed.name: seed for seed in load_all_seed_prompts()}

    rag = seeds["rag_answer_support"]
    assert rag.user_template.startswith("Context:\n")
    assert rag.user_template.endswith("\n")


def test_missing_required_field_is_rejected_with_the_filename(tmp_path: Path) -> None:
    path = tmp_path / "broken.yaml"
    path.write_text("name: broken\nuse_case: chat\n", encoding="utf-8")

    with pytest.raises(PromptValidationError) as exc_info:
        load_seed_prompt(path)

    assert exc_info.value.code == "prompts.seed_missing_field"
    assert exc_info.value.details["file"] == "broken.yaml"
    assert exc_info.value.details["field"] == "system_prompt"


def test_invalid_yaml_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "invalid.yaml"
    path.write_text("name: [unclosed\n", encoding="utf-8")

    with pytest.raises(PromptValidationError) as exc_info:
        load_seed_prompt(path)

    assert exc_info.value.code == "prompts.seed_invalid_yaml"


def test_non_mapping_document_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "list.yaml"
    path.write_text("- one\n- two\n", encoding="utf-8")

    with pytest.raises(PromptValidationError) as exc_info:
        load_seed_prompt(path)

    assert exc_info.value.code == "prompts.seed_invalid_shape"


def test_non_list_input_variables_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "bad_vars.yaml"
    path.write_text(
        "name: x\nuse_case: chat\nsystem_prompt: s\nuser_template: u\ninput_variables: nope\n",
        encoding="utf-8",
    )

    with pytest.raises(PromptValidationError) as exc_info:
        load_seed_prompt(path)

    assert exc_info.value.code == "prompts.seed_invalid_shape"


def test_seed_without_variables_loads_as_an_empty_tuple(tmp_path: Path) -> None:
    path = tmp_path / "novars.yaml"
    path.write_text(
        "name: x\nuse_case: chat\nsystem_prompt: s\nuser_template: u\n",
        encoding="utf-8",
    )

    seed = load_seed_prompt(path)

    assert seed.input_variables == ()
    assert seed.description is None
