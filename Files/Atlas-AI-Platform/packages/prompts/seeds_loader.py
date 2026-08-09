"""Load seed prompts from YAML into typed contracts.

Phase 02 declared the rule that no prompt text lives in a Python module, then
shipped no `seeds/` directory at all, so the rule had nothing to demonstrate it.
This loader plus `seeds/*.yaml` closes that, and it is the loader Phase 03 needs
before it can add `structured_output_repair.yaml`.

The parse is deliberately strict. A malformed seed is a startup-time failure
with a filename in the message, not a `KeyError` surfacing later inside a render
call where the cause is much harder to see.

Python notes for .NET reviewers:
- `Path(__file__).parent` resolves paths relative to this source file, so the
  loader works regardless of the process working directory.
- `yaml.safe_load` refuses to construct arbitrary Python objects, which is the
  only variant safe to point at a file you did not write.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from packages.prompts.contracts import VariableDeclaration
from packages.prompts.errors import PromptValidationError

SEEDS_DIRECTORY = Path(__file__).parent / "seeds"


@dataclass(frozen=True, slots=True)
class SeedPrompt:
    """One seed prompt, parsed and validated but not yet written to the database."""

    name: str
    use_case: str
    description: str | None
    system_prompt: str
    user_template: str
    input_variables: tuple[VariableDeclaration, ...]


def load_seed_prompt(path: Path) -> SeedPrompt:
    """Parse and validate a single seed YAML file."""
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise PromptValidationError(
            code="prompts.seed_invalid_yaml",
            message=f"Seed prompt {path.name} is not valid YAML.",
            details={"file": path.name, "reason": str(exc)},
        ) from exc

    if not isinstance(raw, dict):
        raise PromptValidationError(
            code="prompts.seed_invalid_shape",
            message=f"Seed prompt {path.name} must be a YAML mapping.",
            details={"file": path.name},
        )

    return SeedPrompt(
        name=_required_str(raw, "name", path),
        use_case=_required_str(raw, "use_case", path),
        description=_optional_str(raw, "description"),
        # Prompt bodies keep their exact whitespace. Stripping them would change
        # the rendered text, and therefore the render hash, for no benefit.
        system_prompt=_required_str(raw, "system_prompt", path, strip=False),
        user_template=_required_str(raw, "user_template", path, strip=False),
        input_variables=_variables(raw.get("input_variables"), path),
    )


def load_all_seed_prompts(directory: Path | None = None) -> tuple[SeedPrompt, ...]:
    """Load every `*.yaml` seed, sorted by filename for deterministic ordering."""
    target = directory or SEEDS_DIRECTORY
    return tuple(load_seed_prompt(path) for path in sorted(target.glob("*.yaml")))


def _variables(value: Any, path: Path) -> tuple[VariableDeclaration, ...]:
    if value is None:
        return ()
    if not isinstance(value, list):
        raise PromptValidationError(
            code="prompts.seed_invalid_shape",
            message=f"Seed prompt {path.name} declares input_variables that are not a list.",
            details={"file": path.name},
        )
    declarations = []
    for entry in value:
        if not isinstance(entry, dict):
            raise PromptValidationError(
                code="prompts.seed_invalid_shape",
                message=f"Seed prompt {path.name} has a non-mapping input variable.",
                details={"file": path.name},
            )
        declarations.append(
            VariableDeclaration(
                name=_required_str(entry, "name", path),
                required=bool(entry.get("required", True)),
                # Defaulting `trusted` to False is the safe direction: a seed
                # that forgets the flag gets the fenced, injection-resistant
                # treatment rather than being interpolated straight in.
                trusted=bool(entry.get("trusted", False)),
                description=_optional_str(entry, "description"),
                max_tokens=int(entry["max_tokens"]) if entry.get("max_tokens") else None,
            )
        )
    return tuple(declarations)


def _required_str(source: dict[str, Any], key: str, path: Path, *, strip: bool = True) -> str:
    value = source.get(key)
    if not isinstance(value, str) or not value.strip():
        raise PromptValidationError(
            code="prompts.seed_missing_field",
            message=f"Seed prompt {path.name} is missing the required field '{key}'.",
            details={"file": path.name, "field": key},
        )
    return value.strip() if strip else value


def _optional_str(source: dict[str, Any], key: str) -> str | None:
    value = source.get(key)
    return value.strip() if isinstance(value, str) and value.strip() else None
