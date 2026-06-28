# model_lab/schemas.py
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

RiskLevel = Literal["low", "medium", "high"]
RunnerKind = Literal["baseline", "fake", "transformers"]
ModelFamily = Literal[
    "encoder",
    "decoder",
    "encoder_decoder",
    "dense_decoder",
    "mixture_of_experts",
    "reasoning",
    "multimodal",
]


class ExperimentCase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case_id: str = Field(min_length=1)
    system: str = Field(min_length=1)
    user: str = Field(min_length=1)
    expected_behavior: list[str] = Field(min_length=1)
    risk: RiskLevel = "medium"
    max_input_tokens: int = Field(default=1_000, ge=1, le=128_000)

    @field_validator("case_id")
    @classmethod
    def case_id_is_slug(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned.replace("_", "").replace("-", "").isalnum():
            raise ValueError("case_id must be a simple slug")
        return cleaned


class GenerationSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    max_new_tokens: int = Field(default=120, ge=1, le=4_000)
    do_sample: bool = False
    temperature: float = Field(default=1.0, gt=0, le=5.0)
    top_p: float = Field(default=1.0, gt=0, le=1.0)
    top_k: int = Field(default=50, ge=1)
    stop_sequences: list[str] = Field(default_factory=list)
    repetition_penalty: float | None = Field(default=None, gt=0)
    seed: int | None = None


class ModelSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    model_id: str = Field(min_length=1)
    revision: str | None = None
    runner: RunnerKind = "baseline"
    family: ModelFamily | None = None
    open_weight: bool = False
    hosted: bool = False
    instruction_tuned: bool = False
    multimodal: bool = False
    notes: str = ""


class TokenReport(BaseModel):
    tokenizer: str
    text_chars: int = Field(ge=0)
    token_count: int = Field(ge=0)
    tokens: list[str]
    token_ids: list[int] = Field(default_factory=list)
    special_tokens: list[str] = Field(default_factory=list)


class ExperimentResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case_id: str
    runner: str
    model_id: str
    model_revision: str | None = None
    provider: dict[str, Any] | None = None
    settings: dict[str, Any]
    input_tokens: int = Field(ge=0)
    output_tokens: int = Field(ge=0)
    latency_ms: float = Field(ge=0)
    output_text: str
    flags: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class CaseScore(BaseModel):
    case_id: str
    score: int = Field(ge=0, le=4)
    unsupported_claim: bool
    instruction_violation: bool
    missing_evidence_handled: bool
    notes: list[str] = Field(default_factory=list)