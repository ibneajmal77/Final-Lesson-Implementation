from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from supportops_api.dependencies import get_db_session
from supportops_api.main import create_app
from supportops_db.base import Base
from supportops_db.models import Tenant


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    with session_factory() as session:
        session.add_all(
            [
                Tenant(id="tenant_a", name="Tenant A", slug="tenant-a"),
                Tenant(id="tenant_b", name="Tenant B", slug="tenant-b"),
            ]
        )
        session.commit()

    def override_get_db_session() -> Generator[Session, None, None]:
        session = session_factory()
        try:
            yield session
        finally:
            session.close()

    app = create_app()
    app.dependency_overrides[get_db_session] = override_get_db_session

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def tenant_headers(tenant_id: str = "tenant_a") -> dict[str, str]:
    return {
        "X-Tenant-Id": tenant_id,
        "X-User-Id": "user_agent",
        "X-Role": "agent",
    }


def ticket_payload(external_id: str = "ticket-001") -> dict[str, object]:
    return {
        "external_id": external_id,
        "channel": "email",
        "subject": "Charged twice",
        "body": "I was charged twice for order ORD-123.",
        "customer_id": "customer-123",
        "metadata": {"source": "test"},
    }


def create_ticket_and_ai_analysis(
    client: TestClient,
    tenant_id: str = "tenant_a",
) -> tuple[str, str]:
    created = client.post(
        "/tickets",
        headers=tenant_headers(tenant_id),
        json=ticket_payload(f"{tenant_id}-ticket"),
    )
    ticket_id = created.json()["id"]
    analysis = client.post(
        f"/tickets/{ticket_id}/ai-analysis",
        headers=tenant_headers(tenant_id),
    )
    return ticket_id, analysis.json()["id"]


def create_recommendation_review(
    client: TestClient,
    *,
    ticket_id: str,
    recommendation_id: str,
    decision: str,
    tenant_id: str = "tenant_a",
) -> dict[str, object]:
    payload: dict[str, object] = {"decision": decision}
    if decision == "edited":
        payload["edited_reply"] = "I reviewed this billing issue and will verify the charge."

    response = client.post(
        f"/tickets/{ticket_id}/recommendations/{recommendation_id}/reviews",
        headers=tenant_headers(tenant_id),
        json=payload,
    )
    return response.json()


def test_create_ticket_requires_identity_headers(client: TestClient) -> None:
    response = client.post("/tickets", json=ticket_payload())

    assert response.status_code == 401


def test_create_ticket(client: TestClient) -> None:
    response = client.post("/tickets", headers=tenant_headers(), json=ticket_payload())

    assert response.status_code == 201
    body = response.json()
    assert body["tenant_id"] == "tenant_a"
    assert body["external_id"] == "ticket-001"
    assert body["status"] == "open"
    assert body["priority"] == "normal"
    assert body["metadata"] == {"source": "test"}


def test_create_ticket_is_idempotent_by_tenant_and_external_id(client: TestClient) -> None:
    first = client.post("/tickets", headers=tenant_headers(), json=ticket_payload())
    second = client.post("/tickets", headers=tenant_headers(), json=ticket_payload())

    assert first.status_code == 201
    assert second.status_code == 200
    assert second.json()["id"] == first.json()["id"]


def test_list_tickets_only_returns_current_tenant(client: TestClient) -> None:
    client.post("/tickets", headers=tenant_headers("tenant_a"), json=ticket_payload("a-001"))
    client.post("/tickets", headers=tenant_headers("tenant_b"), json=ticket_payload("b-001"))

    response = client.get("/tickets", headers=tenant_headers("tenant_a"))

    assert response.status_code == 200
    tickets = response.json()
    assert len(tickets) == 1
    assert tickets[0]["external_id"] == "a-001"
    assert tickets[0]["tenant_id"] == "tenant_a"


def test_get_ticket_cannot_cross_tenant_boundary(client: TestClient) -> None:
    created = client.post("/tickets", headers=tenant_headers("tenant_a"), json=ticket_payload())
    ticket_id = created.json()["id"]

    response = client.get(f"/tickets/{ticket_id}", headers=tenant_headers("tenant_b"))

    assert response.status_code == 404


def test_create_baseline_analysis_for_ticket(client: TestClient) -> None:
    created = client.post("/tickets", headers=tenant_headers(), json=ticket_payload())
    ticket_id = created.json()["id"]

    response = client.post(f"/tickets/{ticket_id}/baseline-analysis", headers=tenant_headers())

    assert response.status_code == 201
    body = response.json()
    assert body["tenant_id"] == "tenant_a"
    assert body["ticket_id"] == ticket_id
    assert body["source"] == "baseline_v1"
    assert body["category"] == "billing"
    assert body["priority"] == "high"
    assert body["requires_escalation"] is False
    assert body["extracted_fields"]["order_ids"] == ["ORD-123"]
    assert body["reasons"]


def test_list_ticket_recommendations_for_ticket(client: TestClient) -> None:
    created = client.post("/tickets", headers=tenant_headers(), json=ticket_payload())
    ticket_id = created.json()["id"]
    analysis = client.post(f"/tickets/{ticket_id}/baseline-analysis", headers=tenant_headers())

    response = client.get(f"/tickets/{ticket_id}/recommendations", headers=tenant_headers())

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["id"] == analysis.json()["id"]
    assert body[0]["ticket_id"] == ticket_id


def test_create_ai_analysis_for_ticket(client: TestClient) -> None:
    created = client.post("/tickets", headers=tenant_headers(), json=ticket_payload())
    ticket_id = created.json()["id"]

    response = client.post(f"/tickets/{ticket_id}/ai-analysis", headers=tenant_headers())

    assert response.status_code == 201
    body = response.json()
    assert body["tenant_id"] == "tenant_a"
    assert body["ticket_id"] == ticket_id
    assert body["source"] == "mock_llm_v1"
    assert body["model_name"] == "mock-ticket-analyzer"
    assert body["prompt_version"] == "supportops_ticket_analysis_v1"
    assert body["category"] == "billing"
    assert body["priority"] == "high"
    assert body["summary"]
    assert "billing" in body["suggested_reply"].lower()
    assert body["extracted_fields"]["order_ids"] == ["ORD-123"]


def test_ai_analysis_cannot_cross_tenant_boundary(client: TestClient) -> None:
    created = client.post("/tickets", headers=tenant_headers("tenant_a"), json=ticket_payload())
    ticket_id = created.json()["id"]

    response = client.post(
        f"/tickets/{ticket_id}/ai-analysis",
        headers=tenant_headers("tenant_b"),
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "ticket not found"


def test_approve_recommendation_review(client: TestClient) -> None:
    ticket_id, recommendation_id = create_ticket_and_ai_analysis(client)

    response = client.post(
        f"/tickets/{ticket_id}/recommendations/{recommendation_id}/reviews",
        headers=tenant_headers(),
        json={"decision": "approved", "notes": "Looks good."},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["tenant_id"] == "tenant_a"
    assert body["ticket_id"] == ticket_id
    assert body["recommendation_id"] == recommendation_id
    assert body["reviewer_user_id"] == "user_agent"
    assert body["decision"] == "approved"
    assert body["final_summary"]
    assert body["final_reply"]
    assert body["notes"] == "Looks good."


def test_edit_recommendation_review(client: TestClient) -> None:
    ticket_id, recommendation_id = create_ticket_and_ai_analysis(client)

    response = client.post(
        f"/tickets/{ticket_id}/recommendations/{recommendation_id}/reviews",
        headers=tenant_headers(),
        json={
            "decision": "edited",
            "edited_reply": "I reviewed this billing issue and will verify the duplicate charge.",
            "notes": "Made tone more direct.",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["decision"] == "edited"
    assert body["final_summary"]
    assert (
        body["final_reply"]
        == "I reviewed this billing issue and will verify the duplicate charge."
    )
    assert body["notes"] == "Made tone more direct."


def test_edit_recommendation_review_requires_edited_content(client: TestClient) -> None:
    ticket_id, recommendation_id = create_ticket_and_ai_analysis(client)

    response = client.post(
        f"/tickets/{ticket_id}/recommendations/{recommendation_id}/reviews",
        headers=tenant_headers(),
        json={"decision": "edited"},
    )

    assert response.status_code == 422
    assert response.json()["detail"] == "edited decision requires edited_summary or edited_reply"


def test_reject_recommendation_review(client: TestClient) -> None:
    ticket_id, recommendation_id = create_ticket_and_ai_analysis(client)

    response = client.post(
        f"/tickets/{ticket_id}/recommendations/{recommendation_id}/reviews",
        headers=tenant_headers(),
        json={"decision": "rejected", "notes": "Wrong customer tone."},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["decision"] == "rejected"
    assert body["final_summary"] is None
    assert body["final_reply"] is None
    assert body["notes"] == "Wrong customer tone."


def test_list_recommendation_reviews(client: TestClient) -> None:
    ticket_id, recommendation_id = create_ticket_and_ai_analysis(client)
    created = client.post(
        f"/tickets/{ticket_id}/recommendations/{recommendation_id}/reviews",
        headers=tenant_headers(),
        json={"decision": "approved"},
    )

    response = client.get(
        f"/tickets/{ticket_id}/recommendations/{recommendation_id}/reviews",
        headers=tenant_headers(),
    )

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["id"] == created.json()["id"]
    assert body[0]["decision"] == "approved"


def test_review_recommendation_cannot_cross_tenant_boundary(client: TestClient) -> None:
    ticket_id, recommendation_id = create_ticket_and_ai_analysis(client, tenant_id="tenant_a")

    response = client.post(
        f"/tickets/{ticket_id}/recommendations/{recommendation_id}/reviews",
        headers=tenant_headers("tenant_b"),
        json={"decision": "approved"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "ticket not found"


def test_review_metrics_for_current_tenant(client: TestClient) -> None:
    first_ticket_id, first_recommendation_id = create_ticket_and_ai_analysis(client)
    second_ticket_id, second_recommendation_id = create_ticket_and_ai_analysis(client)
    third_ticket_id, third_recommendation_id = create_ticket_and_ai_analysis(client)
    other_ticket_id, other_recommendation_id = create_ticket_and_ai_analysis(
        client,
        tenant_id="tenant_b",
    )

    create_recommendation_review(
        client,
        ticket_id=first_ticket_id,
        recommendation_id=first_recommendation_id,
        decision="approved",
    )
    create_recommendation_review(
        client,
        ticket_id=second_ticket_id,
        recommendation_id=second_recommendation_id,
        decision="rejected",
    )
    create_recommendation_review(
        client,
        ticket_id=third_ticket_id,
        recommendation_id=third_recommendation_id,
        decision="edited",
    )
    create_recommendation_review(
        client,
        ticket_id=other_ticket_id,
        recommendation_id=other_recommendation_id,
        decision="approved",
        tenant_id="tenant_b",
    )

    response = client.get("/metrics/reviews", headers=tenant_headers())

    assert response.status_code == 200
    body = response.json()
    assert body["tenant_id"] == "tenant_a"
    assert body["total_recommendations"] == 3
    assert body["reviewed_recommendations"] == 3
    assert body["review_coverage_rate"] == 1.0
    assert body["total_reviews"] == 3
    assert body["approved"] == 1
    assert body["rejected"] == 1
    assert body["edited"] == 1
    assert body["approval_rate"] == 0.3333
    assert body["rejection_rate"] == 0.3333
    assert body["edit_rate"] == 0.3333
    assert body["by_source"][0]["key"] == "mock_llm_v1"
    assert body["by_source"][0]["total_reviews"] == 3
    assert body["by_category"][0]["key"] == "billing"
    assert body["by_category"][0]["total_reviews"] == 3


def test_review_metrics_include_unreviewed_recommendations_in_coverage(
    client: TestClient,
) -> None:
    create_ticket_and_ai_analysis(client)

    response = client.get("/metrics/reviews", headers=tenant_headers())

    assert response.status_code == 200
    body = response.json()
    assert body["total_recommendations"] == 1
    assert body["reviewed_recommendations"] == 0
    assert body["review_coverage_rate"] == 0.0
    assert body["total_reviews"] == 0
    assert body["approval_rate"] == 0.0
    assert body["by_source"] == []
    assert body["by_category"] == []


def test_review_metrics_require_known_tenant(client: TestClient) -> None:
    response = client.get("/metrics/reviews", headers=tenant_headers("missing_tenant"))

    assert response.status_code == 404
    assert response.json()["detail"] == "tenant not found"


def test_baseline_analysis_cannot_cross_tenant_boundary(client: TestClient) -> None:
    created = client.post("/tickets", headers=tenant_headers("tenant_a"), json=ticket_payload())
    ticket_id = created.json()["id"]

    response = client.post(
        f"/tickets/{ticket_id}/baseline-analysis",
        headers=tenant_headers("tenant_b"),
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "ticket not found"


def test_unknown_tenant_cannot_create_ticket(client: TestClient) -> None:
    response = client.post(
        "/tickets",
        headers=tenant_headers("missing_tenant"),
        json=ticket_payload(),
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "tenant not found"
