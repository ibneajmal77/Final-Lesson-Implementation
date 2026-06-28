# tests/test_schemas.py
from __future__ import annotations

import pytest
from pydantic import ValidationError

from model_lab.schemas import ExperimentCase, ExperimentResult, GenerationSettings, ModelSpec


def test_case_accepts_valid_data() -> None:
    case = ExperimentCase(
        case_id="missing_evidence",
        system="You help support agents.",
        user="No policy evidence is available.",
        expected_behavior=["asks for evidence"],
    )
    assert case.risk == "medium"


def test_case_rejects_empty_user() -> None:
    with pytest.raises(ValidationError):
        ExperimentCase(case_id="bad", system="x", user="", expected_behavior=["x"])


def test_settings_reject_invalid_top_p() -> None:
    with pytest.raises(ValidationError):
        GenerationSettings(top_p=1.5)


def test_model_spec_records_family_and_tuning() -> None:
    spec = ModelSpec(
        model_id="example/instruct-model",
        runner="fake",
        family="dense_decoder",
        instruction_tuned=True,
        open_weight=True,
    )
    assert spec.instruction_tuned is True


def test_experiment_result_accepts_hosted_provider_metadata() -> None:
    result = ExperimentResult(
        case_id="missing_evidence",
        runner="hosted_recorded",
        model_id="provider-model-name",
        provider={
            "serving_region": "recorded-region-or-unknown",
            "regional_availability_checked": True,
            "provider_data_policy_reviewed": True,
        },
        settings={"temperature": 0.2},
        input_tokens=0,
        output_tokens=0,
        latency_ms=0.0,
        output_text="Synthetic-data output.",
        flags=["manual_record"],
    )
    assert result.provider is not None
    assert result.provider["regional_availability_checked"] is True