"""Tests for gateway execution, retry/fallback policy, redaction, and cost rows."""

from decimal import Decimal

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from packages.db.models.model_gateway import AIRun, CostRecord, ModelRoute
from packages.model_gateway.client import ModelGateway
from packages.model_gateway.errors import BudgetExceededError
from packages.model_gateway.types import ChatMessage, ModelRequest


def test_chat_request_persists_ai_run_and_cost_records(db_session: Session, tenant) -> None:
    request = ModelRequest(
        tenant_id=tenant.id,
        use_case="chat",
        messages=(ChatMessage(role="user", content="hello user@example.com"),),
    )

    response = ModelGateway(db_session).chat(request)

    ai_run = db_session.get(AIRun, response.ai_run_id)
    cost_records = db_session.scalars(
        select(CostRecord).where(CostRecord.ai_run_id == response.ai_run_id)
    ).all()
    assert ai_run is not None
    assert ai_run.status == "succeeded"
    assert ai_run.provider_name == "mock_public"
    assert ai_run.input_tokens is not None
    assert ai_run.estimated_cost_usd is not None
    assert ai_run.input_preview == "hello [redacted-email]"
    assert cost_records
    assert response.observability_attributes["gen_ai.request.model"] == response.model_name


def test_embedding_request_returns_vectors_in_input_order(db_session: Session, tenant) -> None:
    request = ModelRequest(
        tenant_id=tenant.id,
        use_case="embedding",
        inputs=("alpha", "beta"),
    )

    response = ModelGateway(db_session).embed(request)

    assert len(response.embeddings) == 2
    assert response.embeddings[0] != response.embeddings[1]
    assert all(len(vector) == 8 for vector in response.embeddings)


def test_timeout_retries_inside_one_ai_run(db_session: Session, tenant) -> None:
    route = db_session.scalars(
        select(ModelRoute).where(ModelRoute.route_key == "chat_primary")
    ).one()
    original_config = dict(route.route_config_json)
    route.route_config_json = {"mock_scenario": "timeout_once", "max_retries": 1}
    db_session.commit()
    try:
        response = ModelGateway(db_session).chat(
            ModelRequest(
                tenant_id=tenant.id,
                use_case="chat",
                messages=(ChatMessage(role="user", content="retry please"),),
            )
        )
    finally:
        route.route_config_json = original_config
        db_session.commit()

    ai_run = db_session.get(AIRun, response.ai_run_id)
    assert ai_run is not None
    assert ai_run.status == "succeeded"
    assert ai_run.response_json is not None
    attempts = ai_run.response_json["attempts"]
    assert len(attempts) == 2


def test_unavailable_primary_falls_back_after_policy_revalidation(
    db_session: Session,
    tenant,
) -> None:
    route = db_session.scalars(
        select(ModelRoute).where(ModelRoute.route_key == "chat_primary")
    ).one()
    original_config = dict(route.route_config_json)
    route.route_config_json = {"mock_scenario": "unavailable"}
    db_session.commit()
    try:
        response = ModelGateway(db_session).chat(
            ModelRequest(
                tenant_id=tenant.id,
                use_case="chat",
                messages=(ChatMessage(role="user", content="fallback please"),),
            )
        )
    finally:
        route.route_config_json = original_config
        db_session.commit()

    assert response.route_key == "chat_private"
    assert response.provider_name == "mock_private"


def test_budget_block_creates_blocked_ai_run(db_session: Session, tenant) -> None:
    request = ModelRequest(
        tenant_id=tenant.id,
        use_case="chat",
        messages=(ChatMessage(role="user", content="too expensive"),),
        max_cost_usd=Decimal("0.000001"),
    )

    with pytest.raises(BudgetExceededError) as exc_info:
        ModelGateway(db_session).chat(request)

    ai_run_id = exc_info.value.details["ai_run_id"] if exc_info.value.details else None
    assert ai_run_id is not None
    ai_run = db_session.get(AIRun, ai_run_id)
    assert ai_run is not None
    assert ai_run.status == "blocked"
    assert ai_run.error_code == "ai.budget_exceeded"


def test_restricted_request_redacts_stored_content(db_session: Session, tenant) -> None:
    request = ModelRequest(
        tenant_id=tenant.id,
        use_case="chat",
        messages=(ChatMessage(role="user", content="secret password=abc123"),),
        restricted_data=True,
    )

    response = ModelGateway(db_session).chat(request)

    ai_run = db_session.get(AIRun, response.ai_run_id)
    assert ai_run is not None
    assert ai_run.input_preview == "[restricted]"
    assert ai_run.request_json == {
        "redacted": True,
        "use_case": "chat",
        "message_count": 1,
        "input_count": 0,
    }
