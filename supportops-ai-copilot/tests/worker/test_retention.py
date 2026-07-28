# ============================================================================
# FILE: tests/worker/test_retention.py
#
# WHAT THIS TESTS: the privacy cleanup counter in
# apps/worker/supportops_worker/retention.py — the code that finds rows past
# their deletion date.
#
# THE TEST IS ONE LONG SETUP AND SIX SHORT ASSERTIONS, which is typical of
# database tests: creating realistic data is most of the work.
#
# THE CLEVEREST PART IS THE `now=` ARGUMENT AT THE BOTTOM.
#   Time-dependent code is normally miserable to test — you would have to wait,
#   or change the system clock. retention.py accepts an optional `now`, so this
#   test can declare a fixed pretend date and place rows on either side of it.
#   Deterministic, instant, and it will still pass in 2030.
#
#   That is a design lesson worth taking from this file: making the clock an
#   argument rather than a hidden call is what turns untestable code into
#   testable code.
#
# THE TEST'S REAL POINT: it creates TWO tickets, one expired and one not, then
# asserts the count is 1. Counting expired rows is easy; counting ONLY the
# expired ones is the part that could go wrong — and a bug there would mean
# deleting data that should have been kept.
# ============================================================================

from collections.abc import Generator
from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from supportops_db.base import Base
from supportops_db.models import Tenant
from supportops_db.repositories.ai_runs import create_ai_run
from supportops_db.repositories.approvals import create_recommendation_review
from supportops_db.repositories.cost_events import create_cost_event
from supportops_db.repositories.policies import create_support_policy
from supportops_db.repositories.recommendations import create_ticket_recommendation
from supportops_db.repositories.tickets import create_ticket
from supportops_worker.retention import collect_retention_candidates


# A "fixture": setup code pytest runs automatically for any test that names it
# as an argument. This one hands over a ready-to-use database session.
#
# THREE THINGS MAKE THIS FAST AND ISOLATED:
#
#   "sqlite://" with no path - an IN-MEMORY database. Nothing touches the disk,
#     and it disappears when the test ends. No Postgres server needed, and no
#     cleanup to forget.
#
#   StaticPool + check_same_thread - together these keep every connection
#     pointing at the SAME in-memory database. Without them, SQLite would give
#     each connection its own empty one, and the test would mysteriously find no
#     tables.
#
#   Base.metadata.create_all(engine) - builds every table directly from
#     models.py, skipping the migrations. Fast, and it means this test checks the
#     code against the models rather than against migration history. (The
#     migrations get their own coverage in the CI `migrations` job.)
#
# The `yield` hands the session to the test and resumes afterwards — the same
# pattern as get_db_session in dependencies.py.
@pytest.fixture
def session() -> Generator[Session, None, None]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    with session_factory() as db_session:
        # A company must exist first: every other table has a foreign key to it,
        # so nothing else could be created without this row.
        db_session.add(Tenant(id="tenant_a", name="Tenant A", slug="tenant-a"))
        db_session.commit()
        yield db_session


def test_collect_retention_candidates_counts_expired_rows(session: Session) -> None:
    # A FIXED date rather than "today". Essential for a repeatable test: with
    # datetime.now() the boundaries would shift on every run, and a test that
    # passes today could fail tomorrow.
    now = datetime(2026, 7, 21, tzinfo=UTC)
    expired_at = now - timedelta(days=1)      # yesterday: should be counted
    future_at = now + timedelta(days=1)       # tomorrow: should NOT be

    # --- Two tickets: one expired, one not. The heart of the test. ---
    expired_ticket = create_ticket(
        session,
        tenant_id="tenant_a",
        external_id="expired-ticket",
        channel="email",
        subject="Charged twice",
        body="I was charged twice for order ORD-123.",
        customer_id="customer-123",
        metadata={"source": "retention-test"},
    )
    # Set afterwards rather than passed in, because create_ticket takes no
    # retention argument — the expiry is normally applied by a separate policy.
    expired_ticket.retention_expires_at = expired_at

    # THE CONTROL CASE. Without this second ticket, a bug that counted EVERY row
    # regardless of date would still make the test pass — and that bug would
    # delete live customer data. Its presence is what gives the assertion of "1"
    # its meaning.
    future_ticket = create_ticket(
        session,
        tenant_id="tenant_a",
        external_id="future-ticket",
        channel="email",
        subject="Delivery question",
        body="Where is order ORD-999?",
        customer_id="customer-999",
        metadata={"source": "retention-test"},
    )
    future_ticket.retention_expires_at = future_at

    # --- One expired row in each of the other five tables ---
    #
    # Created through the real repository functions rather than by building model
    # objects directly, so the test exercises the same code path the application
    # uses.
    run = create_ai_run(
        session,
        tenant_id="tenant_a",
        ticket_id=expired_ticket.id,
        run_type="ticket_analysis",
        model_provider="mock",
        model_name="mock-ticket-analyzer",
        prompt_version=None,
        input_hash="abc123",
    )
    run.retention_expires_at = expired_at

    recommendation = create_ticket_recommendation(
        session,
        tenant_id="tenant_a",
        ticket_id=expired_ticket.id,
        source="mock_llm_v1",
        category="billing",
        priority="high",
        requires_escalation=False,
        confidence=0.9,
        extracted_fields={"order_ids": ["ORD-123"]},
        reasons=["test"],
    )
    recommendation.retention_expires_at = expired_at

    review = create_recommendation_review(
        session,
        tenant_id="tenant_a",
        ticket_id=expired_ticket.id,
        recommendation_id=recommendation.id,
        reviewer_user_id="user_agent",
        decision="approved",
        final_summary="summary",
        final_reply="reply",
        notes=None,
    )
    review.retention_expires_at = expired_at

    cost_event = create_cost_event(
        session,
        tenant_id="tenant_a",
        provider="mock_llm_v1",
        model="mock-ticket-analyzer",
        operation="retention_test",
        input_tokens=1,
        output_tokens=1,
        estimated_cost_usd=0.0,
        latency_ms=1,
        ticket_id=expired_ticket.id,
        ai_run_id=run.id,
        recommendation_id=recommendation.id,
    )
    cost_event.retention_expires_at = expired_at

    # The only one that takes its expiry as a proper argument, because policies
    # genuinely support a user-set expiry date (see routes/policies.py).
    create_support_policy(
        session,
        tenant_id="tenant_a",
        name="Expired policy",
        content="Expired policy content.",
        created_by_user_id="user_lead",
        retention_expires_at=expired_at,
    )
    session.commit()      # nothing above is permanent until this line

    # THE ACTUAL CALL. Passing `now` is what makes the pretend date take effect.
    counts = collect_retention_candidates(session, now=now)

    # One expired row per table. The first assertion is the meaningful one —
    # TWO tickets exist and only ONE is counted, proving the date filter works
    # rather than the query simply counting everything.
    assert counts.tickets == 1
    assert counts.ai_runs == 1
    assert counts.ticket_recommendations == 1
    assert counts.recommendation_reviews == 1
    assert counts.cost_events == 1
    assert counts.support_policies == 1
    # The computed `total` property. Asserted separately because it is its own
    # small piece of logic that could be wrong even when all six counts are right
    # — a missing table in the sum, for instance.
    assert counts.total == 6

    # WORTH KNOWING WHAT THIS TEST DOES NOT COVER: nothing is actually deleted,
    # because retention.py does not yet implement deletion. This tests the
    # counting half only. When deletion is written, it will need its own test —
    # and a considerably more careful one.
