"""Tests for model route selection, rejection reasons, and tenant route gates."""

from decimal import Decimal

from sqlalchemy.orm import Session

from packages.model_gateway.router import ModelRouter
from packages.model_gateway.types import ChatMessage, ModelRequest


def test_router_selects_private_route_for_restricted_data(
    db_session: Session,
    tenant,
) -> None:
    request = ModelRequest(
        tenant_id=tenant.id,
        use_case="rag_answer",
        messages=(ChatMessage(role="user", content="private question"),),
        restricted_data=True,
    )

    decision = ModelRouter(db_session).select_route(request)

    assert decision.selected is not None
    assert decision.selected.route_key == "rag_answer_private"
    assert any(rejected["reason"] == "data_policy" for rejected in decision.rejected_routes)


def test_router_rejects_routes_over_request_budget(db_session: Session, tenant) -> None:
    request = ModelRequest(
        tenant_id=tenant.id,
        use_case="chat",
        messages=(ChatMessage(role="user", content="hello"),),
        max_cost_usd=Decimal("0.000001"),
    )

    decision = ModelRouter(db_session).select_route(request)

    assert decision.selected is None
    assert decision.error_code == "ai.budget_exceeded"
