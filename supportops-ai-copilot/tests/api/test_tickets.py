# ============================================================================
# FILE: tests/api/test_tickets.py
#
# WHAT THIS TESTS: the public support-ticket workflow exposed by the FastAPI
# routes in apps/api/supportops_api/routes/{tickets,approvals,metrics}.py.
#
# THINK OF THIS FILE AS: a rehearsal room for the API. It sends realistic HTTP
# requests through the assembled app, but swaps expensive shared infrastructure
# for small in-process stand-ins so every rehearsal starts clean and runs offline.
#
# THE BEHAVIOUR COVERED HERE:
#   identity headers and tenant boundaries
#     -> ticket creation, duplicate protection, listing, and lookup
#       -> free baseline analysis and synchronous mock-AI analysis
#         -> queued-analysis job creation and Redis hand-off
#           -> approve, edit, reject, and list human reviews
#             -> review, pilot, cost, and live Prometheus metrics
#               -> request IDs added by the middleware in main.py
#
# HOW ONE TEST REQUEST TRAVELS:
#   TestClient sends an in-process HTTP request
#     -> main.py runs the real middleware and router selection
#       -> dependencies.py reads the identity headers
#         -> the fixture below supplies a temporary SQLAlchemy session
#           -> the real repository functions query an in-memory SQLite database
#
# IMPORTANT TEST BOUNDARIES:
#   - PostgreSQL is replaced by SQLite. These tests check route/repository
#     behaviour, not PostgreSQL-specific SQL; tests/db/ covers schema details.
#   - Redis is replaced by FakeAnalysisQueue. Queued jobs are recorded but never
#     executed here; tests/worker/test_jobs.py covers the worker.
#   - AI calls use providers/mock.py, whose fixed output is free and repeatable.
#   These boundaries make failures precise, but a passing file is not proof that
#   a deployed PostgreSQL, Redis, and hosted model can communicate end to end.
#
# WHO USES IT / WHAT LIVES HERE: pytest discovers every `test_` function;
# helper functions build repeatable requests; the `client` fixture assembles and
# tears down a fresh application database for each test.
# ============================================================================
# `Generator` describes a fixture that yields a value, then resumes for cleanup.
from collections.abc import Generator

# pytest discovers tests, supplies fixtures by argument name, and reports assertions.
import pytest

# TestClient calls the real FastAPI app without opening a network port.
from fastapi.testclient import TestClient

# SQLAlchemy builds the temporary database connection used by the repositories.
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# StaticPool keeps one in-memory SQLite connection alive across TestClient's threads.
from sqlalchemy.pool import StaticPool

# These production dependencies are replaced inside the fixture below.
from supportops_api.dependencies import get_ai_analysis_queue, get_db_session

# create_app wires in the real middleware and every real route.
from supportops_api.main import create_app

# Settings is used to test the AI rollout switches; get_settings is the hook replaced.
from supportops_api.settings import Settings, get_settings

# Base knows every SQLAlchemy table, while Tenant supplies the two test companies.
from supportops_db.base import Base
from supportops_db.models import Tenant

# Prometheus counters live for the whole Python process, so each test must reset them.
from supportops_observability.metrics import reset_metrics


# A "fake" or "test double" has the same small interface as a real dependency
# but controlled behaviour. This replaces AnalysisQueue in
# apps/worker/supportops_worker/queues.py, so no Redis server is needed.
class FakeAnalysisQueue:
    # Python calls __init__ when the fixture constructs a new fake queue.
    def __init__(self) -> None:
        # Keep the exact run IDs handed off by routes/tickets.py. Tests inspect
        # this list to prove rejected requests never reached the queue.
        self.enqueued_run_ids: list[str] = []

    # Match the production queue method name and argument exactly.
    def enqueue_ai_analysis(self, ai_run_id: str) -> dict[str, str]:
        # Recording the call is enough for route tests; executing it belongs to
        # tests/worker/test_jobs.py.
        self.enqueued_run_ids.append(ai_run_id)
        # The real RQ library returns a job object. A dictionary is sufficient
        # because routes/tickets.py deliberately accepts either shape when it
        # extracts the job ID for logging.
        return {"id": f"job-{ai_run_id}", "queue_name": "ai_analysis"}


# A pytest "fixture" is reusable setup supplied to any test that asks for a
# parameter with the same name. The decorator registers this function as `client`.
@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    # The metric objects in packages/observability/metrics.py are process-wide,
    # unlike the database below. Resetting them prevents an earlier test's calls
    # from changing a later test's Prometheus assertions.
    reset_metrics()
    # `sqlite://` creates a database in memory: fast, private to this fixture,
    # and discarded automatically. TestClient handles requests on another
    # thread, so check_same_thread=False permits both threads to use it.
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        # An in-memory database normally belongs to one connection. StaticPool
        # always returns the same connection, so setup and route requests see
        # the same tables and rows rather than separate empty databases.
        poolclass=StaticPool,
    )
    # Build tables from packages/db/supportops_db/models.py. This bypasses the
    # Alembic migration files, so migration/model drift is tested separately in
    # tests/db/test_migration_files.py rather than caught here.
    Base.metadata.create_all(engine)
    # A session is SQLAlchemy's unit of conversation with the database.
    # Disabling automatic flush/commit makes the real route code's explicit
    # session.commit() calls decide when writes become permanent.
    session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    # Seed two companies so every access-control test can ask whether tenant A
    # can see tenant B's data. The `with` block closes this setup session even if
    # seeding fails.
    with session_factory() as session:
        session.add_all(
            [
                Tenant(id="tenant_a", name="Tenant A", slug="tenant-a"),
                Tenant(id="tenant_b", name="Tenant B", slug="tenant-b"),
            ]
        )
        session.commit()

    # FastAPI expects a fresh database session per request. `yield` hands it to
    # the route; `finally` closes it after the response, including error paths.
    def override_get_db_session() -> Generator[Session, None, None]:
        session = session_factory()
        try:
            yield session
        finally:
            session.close()

    # Assemble the same application main.py exposes to Uvicorn.
    app = create_app()
    fake_queue = FakeAnalysisQueue()
    # `app.state` is FastAPI's bag for application-wide objects. Production code
    # does not read this attribute; tests use it to inspect the fake afterwards.
    app.state.fake_analysis_queue = fake_queue
    # `dependency_overrides` is FastAPI's built-in form of monkeypatching.
    # "Monkeypatch" means temporarily replacing a real collaborator during a
    # test: Postgres sessions become SQLite sessions and Redis becomes our fake.
    app.dependency_overrides[get_db_session] = override_get_db_session
    app.dependency_overrides[get_ai_analysis_queue] = lambda: fake_queue
    # Entering TestClient starts the app; yielding lets one test make requests;
    # leaving the block performs client shutdown before fixture cleanup resumes.
    with TestClient(app) as test_client:
        yield test_client

    # Never leak replacements into later requests. Each test gets a new app
    # anyway, but explicit cleanup keeps the fixture safe if its scope changes.
    app.dependency_overrides.clear()


# Build the three headers get_current_actor reads in dependencies.py. The
# default keeps most tests short; passing tenant_b exercises isolation.
#
# Honest boundary: these headers are trusted identity claims, not a real login.
# No User rows are seeded above because the current dependency never looks them
# up. tests/api/test_security.py documents that gateway-trust design explicitly.
def tenant_headers(tenant_id: str = "tenant_a") -> dict[str, str]:
    return {
        # The repository layer receives this tenant ID on every query.
        "X-Tenant-Id": tenant_id,
        # approvals.py records this value as the reviewer for its audit trail.
        "X-User-Id": "user_agent",
        # An agent may create tickets, request analysis, and review drafts.
        "X-Role": "agent",
    }


# One valid request body for schemas/tickets.py. Its defaults are deliberately
# meaningful: billing keywords and ORD-123 drive the baseline classifier down
# a predictable path, while callers can vary only the external ID when needed.
def ticket_payload(external_id: str = "ticket-001") -> dict[str, object]:
    return {
        # The customer's help-desk ID. routes/tickets.py uses it to recognise a retry.
        "external_id": external_id,
        "channel": "email",
        "subject": "Charged twice",
        "body": "I was charged twice for order ORD-123.",
        "customer_id": "customer-123",
        # A nested free-form field also proves JSON metadata survives the database round trip.
        "metadata": {"source": "test"},
    }


# Create a ticket and immediately run the SYNCHRONOUS mock-AI endpoint. The
# returned pair is the database ID of the ticket and its recommendation, which
# review and metrics tests need to build their nested URLs.
def create_ticket_and_ai_analysis(
    client: TestClient,
    tenant_id: str = "tenant_a",
) -> tuple[str, str]:
    created = client.post(
        "/tickets",
        headers=tenant_headers(tenant_id),
        # The ID is fixed per tenant. Repeated calls in one test therefore reuse
        # one ticket through the route's duplicate protection, but each AI call
        # still creates a new recommendation. The review-metrics test relies on
        # counting drafts, not distinct tickets.
        json=ticket_payload(f"{tenant_id}-ticket"),
    )
    ticket_id = created.json()["id"]
    analysis = client.post(
        f"/tickets/{ticket_id}/ai-analysis",
        headers=tenant_headers(tenant_id),
    )
    # This helper does not assert either HTTP status before indexing the JSON.
    # A route failure still fails the test, but usually as a less-informative
    # missing-key error; focused endpoint tests below make the statuses explicit.
    return ticket_id, analysis.json()["id"]


# Record one human verdict through routes/approvals.py and return its JSON form.
def create_recommendation_review(
    client: TestClient,
    # The bare `*` makes every following argument keyword-only. It prevents two
    # similar string IDs from being silently passed in the wrong order.
    *,
    ticket_id: str,
    recommendation_id: str,
    decision: str,
    tenant_id: str = "tenant_a",
) -> dict[str, object]:
    payload: dict[str, object] = {"decision": decision}
    # An "edited" verdict is invalid without changed text. Supply a stable edit
    # so callers testing metric counts do not need to repeat irrelevant wording.
    if decision == "edited":
        payload["edited_reply"] = "I reviewed this billing issue and will verify the charge."

    response = client.post(
        f"/tickets/{ticket_id}/recommendations/{recommendation_id}/reviews",
        headers=tenant_headers(tenant_id),
        json=payload,
    )
    # As above, this convenience helper leaves status assertions to the tests
    # concerned with approval behaviour.
    return response.json()


# The front-door failure: a write with no identity headers must stop in
# dependencies.get_current_actor before routes/tickets.py reaches the database.
def test_create_ticket_requires_identity_headers(client: TestClient) -> None:
    response = client.post("/tickets", json=ticket_payload())

    # 401 means "the server cannot identify the caller." A 403 would mean the
    # caller was known but lacked permission, which is a different problem.
    assert response.status_code == 401


# The ordinary ticket-creation path, from HTTP validation through the tickets
# repository and back out through the TicketRead response schema.
def test_create_ticket(client: TestClient) -> None:
    response = client.post("/tickets", headers=tenant_headers(), json=ticket_payload())

    # 201 Created promises that this request made a new database row.
    assert response.status_code == 201
    body = response.json()
    # tenant_id comes from the trusted Actor headers, never from the JSON body.
    assert body["tenant_id"] == "tenant_a"
    assert body["external_id"] == "ticket-001"
    # `open` and `normal` are database-model defaults in supportops_db/models.py.
    assert body["status"] == "open"
    assert body["priority"] == "normal"
    # Confirms the route's metadata_json column-to-API metadata conversion.
    assert body["metadata"] == {"source": "test"}


# "Idempotent" means retrying the same operation has the same final effect as
# doing it once. Ticket importers retry after network failures, so the pair
# (tenant_id, external_id) must identify the already-created ticket.
def test_create_ticket_is_idempotent_by_tenant_and_external_id(client: TestClient) -> None:
    first = client.post("/tickets", headers=tenant_headers(), json=ticket_payload())
    second = client.post("/tickets", headers=tenant_headers(), json=ticket_payload())

    # The first call creates; the retry honestly reports 200 OK because nothing
    # new was created. Returning the same ID proves the route found the old row.
    assert first.status_code == 201
    assert second.status_code == 200
    assert second.json()["id"] == first.json()["id"]


# The central multi-tenant read test. "Tenant" means one customer company in a
# shared system; every repository query must filter by its tenant_id.
def test_list_tickets_only_returns_current_tenant(client: TestClient) -> None:
    # Put one distinguishable row on each side of the boundary.
    client.post("/tickets", headers=tenant_headers("tenant_a"), json=ticket_payload("a-001"))
    client.post("/tickets", headers=tenant_headers("tenant_b"), json=ticket_payload("b-001"))

    response = client.get("/tickets", headers=tenant_headers("tenant_a"))

    assert response.status_code == 200
    tickets = response.json()
    # Exactly one is stronger than merely finding A: it proves B did not leak in.
    assert len(tickets) == 1
    assert tickets[0]["external_id"] == "a-001"
    assert tickets[0]["tenant_id"] == "tenant_a"


# Possessing another company's real ticket ID must not bypass tenant filtering.
def test_get_ticket_cannot_cross_tenant_boundary(client: TestClient) -> None:
    created = client.post("/tickets", headers=tenant_headers("tenant_a"), json=ticket_payload())
    ticket_id = created.json()["id"]

    # Ask for A's known ID while claiming to be tenant B.
    response = client.get(f"/tickets/{ticket_id}", headers=tenant_headers("tenant_b"))

    # Deliberately 404, not 403: "not found" does not reveal that another
    # company's object exists. get_ticket_by_id applies the tenant filter.
    assert response.status_code == 404


# Exercise analysis path 1 in routes/tickets.py: the free, synchronous keyword
# classifier in packages/domain/supportops_domain/services/baseline.py. No model
# gateway, Redis queue, or worker participates.
def test_create_baseline_analysis_for_ticket(client: TestClient) -> None:
    created = client.post("/tickets", headers=tenant_headers(), json=ticket_payload())
    ticket_id = created.json()["id"]

    response = client.post(f"/tickets/{ticket_id}/baseline-analysis", headers=tenant_headers())

    assert response.status_code == 201
    body = response.json()
    # The saved recommendation must remain attached to both the caller's company
    # and the exact ticket that was analysed.
    assert body["tenant_id"] == "tenant_a"
    assert body["ticket_id"] == ticket_id
    # The versioned source label makes old and new rule sets distinguishable.
    assert body["source"] == "baseline_v1"
    # These values follow from "charged twice" plus the concrete ORD-123 order.
    assert body["category"] == "billing"
    assert body["priority"] == "high"
    assert body["requires_escalation"] is False
    # Proves useful structured data survives repository storage and JSON conversion.
    assert body["extracted_fields"]["order_ids"] == ["ORD-123"]
    # Truthiness checks that at least one explanation exists without coupling
    # this route test to the classifier's exact prose.
    assert body["reasons"]


# A recommendation is useful only if it can be read back later for human review.
# This covers list_ticket_recommendations in repositories/recommendations.py.
def test_list_ticket_recommendations_for_ticket(client: TestClient) -> None:
    created = client.post("/tickets", headers=tenant_headers(), json=ticket_payload())
    ticket_id = created.json()["id"]
    analysis = client.post(f"/tickets/{ticket_id}/baseline-analysis", headers=tenant_headers())

    response = client.get(f"/tickets/{ticket_id}/recommendations", headers=tenant_headers())

    assert response.status_code == 200
    body = response.json()
    # Only one analysis was requested, so one result should be stored. Matching
    # IDs proves this is that result rather than an unrelated row.
    assert len(body) == 1
    assert body[0]["id"] == analysis.json()["id"]
    assert body[0]["ticket_id"] == ticket_id


# Exercise analysis path 2: the synchronous AI route. The caller waits while
# routes/tickets.py builds a provider, analyses, saves the recommendation, and
# records a cost event in one request.
def test_create_ai_analysis_for_ticket(client: TestClient) -> None:
    created = client.post("/tickets", headers=tenant_headers(), json=ticket_payload())
    ticket_id = created.json()["id"]

    response = client.post(f"/tickets/{ticket_id}/ai-analysis", headers=tenant_headers())

    assert response.status_code == 201
    body = response.json()
    assert body["tenant_id"] == "tenant_a"
    assert body["ticket_id"] == ticket_id
    # These labels prove routing.py selected providers/mock.py, not the baseline
    # endpoint or a real paid provider.
    assert body["source"] == "mock_llm_v1"
    assert body["model_name"] == "mock-ticket-analyzer"
    assert body["prompt_version"] == "supportops_ticket_analysis_v1"
    # The mock deliberately wraps the baseline classifier, so these values are
    # stable enough for exact assertions while still exercising model plumbing.
    assert body["category"] == "billing"
    assert body["priority"] == "high"
    assert body["summary"]
    assert "billing" in body["suggested_reply"].lower()
    assert body["extracted_fields"]["order_ids"] == ["ORD-123"]
    # Honest limitation: this proves the model-gateway contract and persistence,
    # not the quality or availability of a hosted language model.


# The master feature switch is the emergency brake for AI-specific incidents.
# Ticket creation still works, but synchronous model work must stop with a
# temporary-service response before a provider is built.
def test_ai_analysis_can_be_disabled(client: TestClient) -> None:
    created = client.post("/tickets", headers=tenant_headers(), json=ticket_payload())
    ticket_id = created.json()["id"]
    # This FastAPI dependency override is a targeted monkeypatch: for this app,
    # calls asking for get_settings receive a Settings object with AI turned off.
    client.app.dependency_overrides[get_settings] = lambda: Settings(ai_analysis_enabled=False)

    # `finally` always removes the override, even if the request raises. Without
    # it, later operations could inherit a setting they never asked for.
    try:
        response = client.post(f"/tickets/{ticket_id}/ai-analysis", headers=tenant_headers())
    finally:
        # pop(..., None) removes the entry and stays harmless if it is already gone.
        client.app.dependency_overrides.pop(get_settings, None)

    # 503 says the feature is temporarily unavailable for everyone, matching
    # _require_ai_analysis_enabled in routes/tickets.py.
    assert response.status_code == 503
    assert response.json()["detail"] == "ai analysis is disabled"


# The same emergency brake must protect path 3, the queued analysis endpoint.
def test_async_ai_analysis_enqueue_can_be_disabled(client: TestClient) -> None:
    created = client.post("/tickets", headers=tenant_headers(), json=ticket_payload())
    ticket_id = created.json()["id"]
    client.app.dependency_overrides[get_settings] = lambda: Settings(ai_analysis_enabled=False)

    try:
        response = client.post(f"/tickets/{ticket_id}/analyze", headers=tenant_headers())
    finally:
        client.app.dependency_overrides.pop(get_settings, None)

    assert response.status_code == 503
    assert response.json()["detail"] == "ai analysis is disabled"
    # More important than the error text: no run ID reached Redis's stand-in.
    # This locks in the order "check the switch, THEN create/queue work."
    assert client.app.state.fake_analysis_queue.enqueued_run_ids == []


# An "allowlist" is an explicit list of who may use a feature. Once this setting
# names tenant B, tenant A must be refused even though the master switch is on.
def test_ai_analysis_requires_enabled_tenant_when_tenant_allowlist_is_set(
    client: TestClient,
) -> None:
    created = client.post("/tickets", headers=tenant_headers(), json=ticket_payload())
    ticket_id = created.json()["id"]
    client.app.dependency_overrides[get_settings] = lambda: Settings(
        ai_analysis_enabled_tenants="tenant_b"
    )

    try:
        response = client.post(f"/tickets/{ticket_id}/ai-analysis", headers=tenant_headers())
    finally:
        client.app.dependency_overrides.pop(get_settings, None)

    # 403 means the service works, but this known caller is outside the pilot.
    # Retrying will not help until configuration changes.
    assert response.status_code == 403
    assert response.json()["detail"] == "ai analysis is not enabled for this tenant or category"


# Pilot access is narrowed by ticket category as well as tenant. This ticket is
# classified as account_access by services/baseline.py, while only billing is enabled.
def test_async_ai_analysis_requires_enabled_category(client: TestClient) -> None:
    created = client.post(
        "/tickets",
        headers=tenant_headers(),
        # Written out rather than using ticket_payload because its words must
        # drive a different baseline category.
        json={
            "external_id": "account-access-001",
            "channel": "email",
            "subject": "Password reset",
            "body": "I cannot access my account and need a password reset.",
            "customer_id": "customer-123",
            "metadata": {"source": "test"},
        },
    )
    ticket_id = created.json()["id"]
    client.app.dependency_overrides[get_settings] = lambda: Settings(
        ai_analysis_enabled_categories="billing"
    )

    try:
        response = client.post(f"/tickets/{ticket_id}/analyze", headers=tenant_headers())
    finally:
        client.app.dependency_overrides.pop(get_settings, None)

    assert response.status_code == 403
    assert response.json()["detail"] == "ai analysis is not enabled for this tenant or category"
    # Again verify refusal happened before any queue side effect.
    assert client.app.state.fake_analysis_queue.enqueued_run_ids == []

# Tenant isolation is checked before synchronous model work. An attacker with a
# valid ticket ID from tenant A must not use tenant B headers to analyse it.
def test_ai_analysis_cannot_cross_tenant_boundary(client: TestClient) -> None:
    created = client.post("/tickets", headers=tenant_headers("tenant_a"), json=ticket_payload())
    ticket_id = created.json()["id"]

    response = client.post(
        f"/tickets/{ticket_id}/ai-analysis",
        headers=tenant_headers("tenant_b"),
    )

    # The generic 404 conceals whether that cross-tenant ID exists at all.
    assert response.status_code == 404
    assert response.json()["detail"] == "ticket not found"




# Exercise analysis path 3 up to the process boundary: routes/tickets.py writes
# an AIRun through repositories/ai_runs.py and hands its ID to the queue. The
# fake deliberately does not run apps/worker/supportops_worker/jobs.py.
def test_enqueue_ticket_analysis_for_ticket(client: TestClient) -> None:
    created = client.post("/tickets", headers=tenant_headers(), json=ticket_payload())
    ticket_id = created.json()["id"]

    response = client.post(f"/tickets/{ticket_id}/analyze", headers=tenant_headers())

    # 202 Accepted means "valid and recorded, but not finished yet."
    assert response.status_code == 202
    body = response.json()
    assert body["tenant_id"] == "tenant_a"
    assert body["ticket_id"] == ticket_id
    assert body["run_type"] == "ticket_analysis"
    # `queued` is the first state in ai_runs.py's durable state machine.
    assert body["status"] == "queued"
    # The run records intended configuration before the worker starts.
    assert body["model_provider"] == "mock"
    # input_hash is a one-way fingerprint of ticket text. It supports comparing
    # runs without copying private customer words into logs or queue messages.
    assert body["input_hash"]
    # No worker ran, so no recommendation can be attached yet.
    assert body["output_recommendation"] is None
    # The key hand-off contract: only the durable run ID reaches the queue.
    assert client.app.state.fake_analysis_queue.enqueued_run_ids == [body["id"]]


# Clients poll this endpoint after receiving 202. It reads the durable job-sheet
# history, allowing another process to report progress without holding one HTTP
# request open for the model's entire runtime.
def test_list_ticket_analysis_runs(client: TestClient) -> None:
    created = client.post("/tickets", headers=tenant_headers(), json=ticket_payload())
    ticket_id = created.json()["id"]
    analysis = client.post(f"/tickets/{ticket_id}/analyze", headers=tenant_headers())

    response = client.get(f"/tickets/{ticket_id}/analysis", headers=tenant_headers())

    assert response.status_code == 200
    body = response.json()
    # One enqueue created one visible run, and its ID matches the POST response.
    assert len(body) == 1
    assert body[0]["id"] == analysis.json()["id"]
    # It remains queued because FakeAnalysisQueue never invokes the worker.
    assert body[0]["status"] == "queued"


# Tenant filtering must happen before even creating the async job sheet.
def test_enqueue_ticket_analysis_cannot_cross_tenant_boundary(client: TestClient) -> None:
    created = client.post("/tickets", headers=tenant_headers("tenant_a"), json=ticket_payload())
    ticket_id = created.json()["id"]

    response = client.post(
        f"/tickets/{ticket_id}/analyze",
        headers=tenant_headers("tenant_b"),
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "ticket not found"

# This preceding async boundary test does not also inspect fake_analysis_queue
# as the feature-flag tests do. Its 404 checks confidentiality; a queue-side-
# effect assertion would make the no-work guarantee stronger.
#
# Approval is the explicit human-in-the-loop safety step in routes/approvals.py.
# The AI draft is never treated as final merely because analysis succeeded.
def test_approve_recommendation_review(client: TestClient) -> None:
    ticket_id, recommendation_id = create_ticket_and_ai_analysis(client)

    # In production an agent reads the draft before sending this decision. The
    # test automates the verdict only to verify persistence and response shape.
    response = client.post(
        f"/tickets/{ticket_id}/recommendations/{recommendation_id}/reviews",
        headers=tenant_headers(),
        json={"decision": "approved", "notes": "Looks good."},
    )

    assert response.status_code == 201
    body = response.json()
    # These links form the audit trail: company, ticket, exact draft, and person.
    assert body["tenant_id"] == "tenant_a"
    assert body["ticket_id"] == ticket_id
    assert body["recommendation_id"] == recommendation_id
    assert body["reviewer_user_id"] == "user_agent"
    assert body["decision"] == "approved"
    # For approval, _review_final_content copies the AI text unchanged into the
    # final fields. Truthiness is enough here; the edit test checks exact text.
    assert body["final_summary"]
    assert body["final_reply"]
    assert body["notes"] == "Looks good."


# An "edited" decision preserves the human's corrected version rather than
# quietly treating every accepted draft as unchanged AI output.
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
    # No edited_summary was supplied, so approvals.py correctly falls back to
    # the original summary while replacing only the reply.
    assert body["final_summary"]
    assert (
        body["final_reply"]
        == "I reviewed this billing issue and will verify the duplicate charge."
    )
    assert body["notes"] == "Made tone more direct."


# A verdict claiming "edited" without changed content is contradictory and
# would corrupt edit-rate metrics, so the route must reject it.
def test_edit_recommendation_review_requires_edited_content(client: TestClient) -> None:
    ticket_id, recommendation_id = create_ticket_and_ai_analysis(client)

    response = client.post(
        f"/tickets/{ticket_id}/recommendations/{recommendation_id}/reviews",
        headers=tenant_headers(),
        json={"decision": "edited"},
    )

    # 422 means the JSON shape was understood, but its combination of values is
    # not meaningful. This check lives in approvals._review_final_content.
    assert response.status_code == 422
    assert response.json()["detail"] == "edited decision requires edited_summary or edited_reply"


# Rejection still creates an audit record, but no reply is accepted as final.
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
    # Explicit None values distinguish "nothing approved" from empty wording.
    assert body["final_summary"] is None
    assert body["final_reply"] is None
    # Free-text notes later feed feedback clustering in repositories/pilot.py.
    assert body["notes"] == "Wrong customer tone."


# Reviews are append-only audit events. This proves a saved decision can be
# listed beneath the exact ticket and recommendation URL.
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
    # Matching the generated ID proves the GET returned the POSTed audit row.
    assert body[0]["id"] == created.json()["id"]
    assert body[0]["decision"] == "approved"


# Knowing both inner IDs must never let tenant B reach tenant A's draft.
# approvals.py validates each parent link in the deeply nested URL.
def test_review_recommendation_cannot_cross_tenant_boundary(client: TestClient) -> None:
    ticket_id, recommendation_id = create_ticket_and_ai_analysis(client, tenant_id="tenant_a")

    response = client.post(
        f"/tickets/{ticket_id}/recommendations/{recommendation_id}/reviews",
        headers=tenant_headers("tenant_b"),
        json={"decision": "approved"},
    )

    # It fails at the tenant-scoped ticket lookup, concealing existence.
    assert response.status_code == 404
    assert response.json()["detail"] == "ticket not found"


# The quality scoreboard in routes/metrics.py must count review decisions for
# the current company only, then provide both totals and useful slices.
def test_review_metrics_for_current_tenant(client: TestClient) -> None:
    # The helper reuses one ticket ID per tenant but makes a fresh recommendation
    # on each AI call. These are three drafts for A and one control draft for B.
    first_ticket_id, first_recommendation_id = create_ticket_and_ai_analysis(client)
    second_ticket_id, second_recommendation_id = create_ticket_and_ai_analysis(client)
    third_ticket_id, third_recommendation_id = create_ticket_and_ai_analysis(client)
    other_ticket_id, other_recommendation_id = create_ticket_and_ai_analysis(
        client,
        tenant_id="tenant_b",
    )

    # Give tenant A one of each verdict, creating an intentionally even dataset.
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
        # This tempting fourth approval must be excluded from A's report.
        tenant_id="tenant_b",
    )

    response = client.get("/metrics/reviews", headers=tenant_headers())

    assert response.status_code == 200
    body = response.json()
    assert body["tenant_id"] == "tenant_a"
    # "Recommendations" are produced drafts; "reviewed" means at least one
    # human verdict exists. Here all three A drafts were reviewed.
    assert body["total_recommendations"] == 3
    assert body["reviewed_recommendations"] == 3
    assert body["review_coverage_rate"] == 1.0
    # The B approval must not turn these totals into four or approved into two.
    assert body["total_reviews"] == 3
    assert body["approved"] == 1
    assert body["rejected"] == 1
    assert body["edited"] == 1
    # metrics.py rounds ratios to four decimal places: one divided by three.
    assert body["approval_rate"] == 0.3333
    assert body["rejection_rate"] == 0.3333
    assert body["edit_rate"] == 0.3333
    # Breakdowns expose hidden differences by model source and ticket category.
    # There is one key in each list because all A drafts used the same mock
    # provider and billing input.
    assert body["by_source"][0]["key"] == "mock_llm_v1"
    assert body["by_source"][0]["total_reviews"] == 3
    assert body["by_category"][0]["key"] == "billing"
    assert body["by_category"][0]["total_reviews"] == 3



def test_pilot_metrics_for_current_tenant(client: TestClient) -> None:
    client.app.dependency_overrides[get_settings] = lambda: Settings(
        ai_analysis_enabled_categories="billing"
    )
    try:
        ticket_id, recommendation_id = create_ticket_and_ai_analysis(client)
        create_recommendation_review(
            client,
            ticket_id=ticket_id,
            recommendation_id=recommendation_id,
            decision="approved",
        )
        response = client.get("/metrics/pilot", headers=tenant_headers())
    finally:
        client.app.dependency_overrides.pop(get_settings, None)

    assert response.status_code == 200
    body = response.json()
    assert body["tenant_id"] == "tenant_a"
    assert body["pilot_categories"] == ["billing"]
    assert body["reviewed_drafts"] == 1
    assert body["accepted_drafts"] == 1
    assert body["rejected_drafts"] == 0
    assert body["draft_acceptance_rate"] == 1.0
    assert body["cost_per_accepted_draft"] == 0.0
    assert body["safety_failures"] == 0
    assert body["exit_decision"] == "iterate"


def test_pilot_feedback_returns_rejected_drafts(client: TestClient) -> None:
    client.app.dependency_overrides[get_settings] = lambda: Settings(
        ai_analysis_enabled_categories="billing"
    )
    try:
        ticket_id, recommendation_id = create_ticket_and_ai_analysis(client)
        review_response = client.post(
            f"/tickets/{ticket_id}/recommendations/{recommendation_id}/reviews",
            headers=tenant_headers(),
            json={"decision": "rejected", "notes": "Wrong tone for this customer."},
        )
        response = client.get("/metrics/pilot/feedback", headers=tenant_headers())
    finally:
        client.app.dependency_overrides.pop(get_settings, None)

    assert review_response.status_code == 201
    assert response.status_code == 200
    body = response.json()
    assert body["tenant_id"] == "tenant_a"
    assert body["pilot_categories"] == ["billing"]
    assert len(body["candidates"]) == 1
    assert body["candidates"][0]["decision"] == "rejected"
    assert body["candidates"][0]["review_id"] == review_response.json()["id"]
    assert body["reason_clusters"] == [{"reason": "tone", "count": 1}]
    assert "difficult eval dataset" in body["recommended_next_step"]

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


def test_cost_metrics_for_current_tenant(client: TestClient) -> None:
    create_ticket_and_ai_analysis(client, tenant_id="tenant_a")
    create_ticket_and_ai_analysis(client, tenant_id="tenant_b")

    response = client.get("/metrics/costs", headers=tenant_headers("tenant_a"))

    assert response.status_code == 200
    body = response.json()
    assert body["tenant_id"] == "tenant_a"
    assert body["total_events"] == 1
    assert body["input_tokens"] == 0
    assert body["output_tokens"] == 0
    assert body["estimated_cost_usd"] == 0.0
    assert body["cost_per_accepted_draft"] == 0.0
    assert body["by_provider"][0]["key"] == "mock_llm_v1"
    assert body["by_model"][0]["key"] == "mock-ticket-analyzer"


def test_cost_metrics_require_known_tenant(client: TestClient) -> None:
    response = client.get("/metrics/costs", headers=tenant_headers("missing_tenant"))

    assert response.status_code == 404
    assert response.json()["detail"] == "tenant not found"


def test_runtime_metrics_endpoint_exposes_prometheus_text(client: TestClient) -> None:
    response = client.get("/metrics/runtime")

    assert response.status_code == 200
    assert "tickets_created_total" in response.text
    assert "ai_analysis_started_total" in response.text
    assert "model_cost_usd_total" in response.text


def test_request_id_is_returned_in_response_header(client: TestClient) -> None:
    response = client.get("/health", headers={"X-Request-Id": "req-test-123"})

    assert response.status_code == 200
    assert response.headers["X-Request-Id"] == "req-test-123"
