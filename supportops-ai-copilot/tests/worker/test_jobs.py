# ============================================================================
# FILE: tests/worker/test_jobs.py
#
# WHAT THIS TESTS: run_ticket_analysis in
# apps/worker/supportops_worker/jobs.py — the function the background worker
# runs when a queued analysis job comes off Redis.
#
# WHY THIS IS THE MOST IMPORTANT TEST FILE IN THE PROJECT: this is the path the
# real UI uses. A user clicks "analyze", the API writes an ai_run row and pushes
# only its ID onto the queue, and then this function does everything else — call
# the model, save the result, record the cost, mark the run finished. If it
# breaks, tickets silently sit at status "queued" forever.
#
#   POST /analyze  ->  ai_run row (status "queued")  ->  Redis  ->  THIS FUNCTION
#
# THE SHAPE OF ALL FOUR TESTS is deliberately identical: set up a ticket and a
# run, call the job once, then inspect the DATABASE rather than the return value
# alone. That matters because the job's real product is persisted state — a
# recommendation row, a cost row, a finished run — not what it hands back.
#
# NOTE THERE IS NO REDIS HERE. The job function takes its session, settings and
# run ID as plain arguments, so it can be called directly. The queue is somebody
# else's problem (see apps/worker/supportops_worker/main.py). That separation is
# what makes this testable at all.
#
# ONE SUCCESS TEST, THREE FAILURE TESTS — a ratio worth noticing. The failure
# paths matter more here, because each one must still leave the run in a clean
# terminal state instead of hanging.
# ============================================================================

from collections.abc import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from supportops_api.settings import Settings
from supportops_db.base import Base
from supportops_db.models import Tenant
from supportops_db.repositories.ai_runs import create_ai_run
from supportops_db.repositories.cost_events import list_cost_events_for_ai_run
from supportops_db.repositories.recommendations import list_ticket_recommendations
from supportops_db.repositories.tickets import create_ticket
from supportops_model_gateway.errors import ModelProviderResponseError
from supportops_worker import jobs


# A FIXTURE is pytest's word for reusable setup. Any test that takes an argument
# called `session` gets this function's result handed to it automatically —
# pytest matches by NAME, which is why there is no visible wiring anywhere.
#
# WHY SQLITE IN MEMORY rather than the real Postgres: "sqlite://" with no path
# means the database exists only in RAM. It is created from nothing, used, and
# vanishes. Tests therefore need no running database, cost nothing, and cannot
# leak state into each other — every test gets a spotless schema.
#
# The two connect arguments are the awkward part, and both exist for the same
# reason: SQLite's in-memory database normally lives inside ONE connection, so a
# second connection would see an entirely empty database.
#   - StaticPool  : reuse a single connection for everything, so the data stays.
#   - check_same_thread=False : SQLite otherwise refuses to be touched from a
#     thread other than the one that opened it; harmless here, since the tests
#     are single-threaded anyway.
@pytest.fixture
def session() -> Generator[Session, None, None]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    # Builds every table straight from the model definitions in
    # packages/db/supportops_db/models.py. Note this SKIPS Alembic entirely — the
    # migrations are not replayed here. Fast, but it means these tests would not
    # notice a migration that had drifted out of step with the models. That gap is
    # covered separately by tests/db/test_migration_files.py.
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    with session_factory() as db_session:
        # Every table is scoped by tenant_id, and a ticket cannot reference a
        # tenant that does not exist (a "foreign key" — a column whose value must
        # match a real row in another table). So the tenant has to be created
        # first, or every insert below would be rejected.
        db_session.add(Tenant(id="tenant_a", name="Tenant A", slug="tenant-a"))
        db_session.commit()

        # `yield` rather than `return` is what makes this a fixture with CLEANUP.
        # Execution pauses here, the test body runs with this session, and then
        # control comes back to finish the `with` block — closing the session and
        # discarding the in-memory database. Same idea as the yield-dependencies
        # in apps/api/supportops_api/dependencies.py.
        yield db_session


# A PLAIN HELPER, not a fixture — it is called explicitly by each test.
#
# It recreates the state the API leaves behind just before queueing: a ticket to
# analyse, plus an ai_run row already marked as pending work. The worker never
# creates these itself; it only ever picks up a run that already exists.
#
# WHY IT RETURNS BOTH IDs: the tests need the run ID to invoke the job, and the
# ticket ID to look up what the job wrote afterwards.
def create_ticket_and_run(session: Session) -> tuple[str, str]:
    ticket = create_ticket(
        session,
        tenant_id="tenant_a",
        external_id="ticket-worker-001",
        channel="email",
        subject="Charged twice",
        body="I was charged twice for order ORD-123.",
        customer_id="customer-123",
        metadata={"source": "worker-test"},
    )
    run = create_ai_run(
        session,
        tenant_id="tenant_a",
        ticket_id=ticket.id,
        run_type="ticket_analysis",
        model_provider="mock",
        model_name="mock-ticket-analyzer",
        prompt_version=None,
        # A real run stores a fingerprint of the input here, so identical tickets
        # can be recognised. The tests never read it, so a fixed dummy is fine.
        input_hash="abc123",
    )
    session.commit()
    return ticket.id, run.id


# THE HAPPY PATH — one call, then four separate things are checked, because a
# single analysis is supposed to leave four distinct traces behind.
def test_worker_creates_ai_output_and_marks_run_succeeded(session: Session) -> None:
    ticket_id, run_id = create_ticket_and_run(session)

    # model_provider="mock" is what keeps the whole suite free and offline. It
    # selects the fake provider in packages/model_gateway/, which returns a
    # canned, correctly-shaped answer instead of calling a real AI service. No
    # network, no API key, no per-run cost, and identical output every time —
    # which is the only reason the exact assertions below are possible.
    run = jobs.run_ticket_analysis(
        session=session,
        settings=Settings(model_provider="mock"),
        ai_run_id=run_id,
    )

    # Read back through the REPOSITORIES rather than writing a query here. Tests
    # go through the same front door as production code
    # (packages/db/supportops_db/repositories/), so tenant scoping is exercised
    # too rather than quietly bypassed.
    recommendations = list_ticket_recommendations(
        session,
        tenant_id="tenant_a",
        ticket_id=ticket_id,
    )
    cost_events = list_cost_events_for_ai_run(session, ai_run_id=run_id)

    assert run.status == "succeeded"
    # The run must POINT AT its output. Without this link you could see that an
    # analysis succeeded but have no way to find what it produced.
    assert run.output_recommendation_id == recommendations[0].id

    # Both timestamps set means the run reached a proper end. A run with a start
    # and no finish is the signature of a crashed or stuck job.
    assert run.started_at is not None
    assert run.finished_at is not None

    # The source records WHICH engine produced this, so mock, real-AI and
    # keyword-baseline results stay distinguishable forever in the database.
    assert recommendations[0].source == "mock_llm_v1"

    # The link back the other way: from a recommendation to the run that made it.
    assert recommendations[0].extracted_fields_json["ai_run_id"] == run_id

    # Proof the free keyword classifier ran ALONGSIDE the AI and its verdict was
    # stored next to the AI's. That is what later allows the two to be compared —
    # the baseline is the yardstick the AI is measured against, so it has to be
    # captured at the same moment rather than recomputed later.
    assert recommendations[0].extracted_fields_json["baseline_preview"]["category"] == "billing"

    # EXACTLY ONE cost event — not "at least one". This catches double-billing,
    # where a retry or a stray second call would quietly charge twice.
    assert len(cost_events) == 1
    # The remaining assertions all check that the cost is fully ATTRIBUTABLE —
    # traceable to a tenant, a ticket, a recommendation, and a specific model.
    # Spend has to be answerable at that granularity: "which customer, and for
    # what work". A cost total with no such trail cannot be billed or explained.
    assert cost_events[0].tenant_id == "tenant_a"
    assert cost_events[0].ticket_id == ticket_id
    assert cost_events[0].recommendation_id == recommendations[0].id
    assert cost_events[0].provider == "mock_llm_v1"
    assert cost_events[0].model == "mock-ticket-analyzer"


# FAILURE 1 OF 3 — the master switch is off.
#
# This is a POLICY refusal, not a breakdown: someone deliberately disabled AI
# analysis. The point of the test is that a policy refusal still ends the run
# properly instead of leaving it pending forever.
def test_worker_marks_run_failed_when_ai_analysis_is_disabled(session: Session) -> None:
    ticket_id, run_id = create_ticket_and_run(session)

    run = jobs.run_ticket_analysis(
        session=session,
        settings=Settings(model_provider="mock", ai_analysis_enabled=False),
        ai_run_id=run_id,
    )

    recommendations = list_ticket_recommendations(
        session,
        tenant_id="tenant_a",
        ticket_id=ticket_id,
    )
    assert run.status == "failed"

    # A STABLE, MACHINE-READABLE code — not a sentence. Dashboards and alerts
    # group on this, so it must not change when the wording of a message does.
    assert run.error_code == "ai_analysis_disabled"

    # The three assertions that really matter on every failure path:
    #   - no output was linked,
    #   - the run still reached a terminal state (both timestamps set),
    #   - and NOTHING was written to the database.
    # A half-finished analysis would be worse than none, because a reviewer might
    # act on it. Refusing cleanly is the correct behaviour.
    assert run.output_recommendation_id is None
    assert run.started_at is not None
    assert run.finished_at is not None
    assert recommendations == []


# FAILURE 2 OF 3 — AI is on, but not for THIS kind of ticket.
#
# This is the pilot gate. Only the listed categories may be analysed, which is
# how the rollout is kept narrow while trust is being established. Here only
# "security" is permitted, and the ticket is a billing one, so it is refused.
#
# Note what this depends on: the free keyword classifier has to categorise the
# ticket BEFORE the AI is allowed to see it. The gate is decided by
# packages/domain/supportops_domain/services/baseline.py, not by the AI itself —
# otherwise you would have to run the model to find out whether you were allowed
# to run the model.
def test_worker_marks_run_failed_when_category_is_not_enabled(session: Session) -> None:
    ticket_id, run_id = create_ticket_and_run(session)

    run = jobs.run_ticket_analysis(
        session=session,
        settings=Settings(model_provider="mock", ai_analysis_enabled_categories="security"),
        ai_run_id=run_id,
    )

    recommendations = list_ticket_recommendations(
        session,
        tenant_id="tenant_a",
        ticket_id=ticket_id,
    )
    assert run.status == "failed"
    assert run.error_code == "ai_analysis_category_not_enabled"
    assert run.output_recommendation_id is None
    assert run.started_at is not None
    assert run.finished_at is not None
    assert recommendations == []

# FAILURE 3 OF 3 — the model itself misbehaved, and the only test here that is
# not about policy.
#
# The previous two failures were decided before the AI was ever called. This one
# is the genuinely unpredictable case: the provider was called and came back with
# something unusable. In production this covers a malformed reply, an outage, or
# a response that does not fit the expected shape.
def test_worker_marks_run_failed_when_model_call_fails(
    session: Session,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    ticket_id, run_id = create_ticket_and_run(session)

    # A stand-in provider that does nothing but fail. `*args, **kwargs` means
    # "accept any arguments at all" — it never looks at them, so it does not have
    # to match the real function's signature.
    def fail_provider(*args, **kwargs):
        raise ModelProviderResponseError("invalid model output")

    # MONKEYPATCHING means temporarily replacing a name at runtime. Here the
    # job module's `build_ticket_analysis_provider` is swapped for the failing
    # version above, so the code under test unknowingly builds a broken provider.
    #
    # Note it patches `jobs.build_ticket_analysis_provider` — the name as jobs.py
    # sees it — not the original in the model gateway. Patching where a thing is
    # USED rather than where it is DEFINED is the usual stumbling block with this
    # technique; patching the definition would have no effect here, because
    # jobs.py already holds its own reference to the original.
    #
    # pytest undoes the swap automatically when the test ends, so no other test
    # is affected. That automatic restoration is the whole reason for using
    # monkeypatch instead of assigning to the attribute by hand.
    monkeypatch.setattr(jobs, "build_ticket_analysis_provider", fail_provider)

    run = jobs.run_ticket_analysis(
        session=session,
        settings=Settings(model_provider="mock"),
        ai_run_id=run_id,
    )

    recommendations = list_ticket_recommendations(
        session,
        tenant_id="tenant_a",
        ticket_id=ticket_id,
    )
    assert run.status == "failed"

    # THE KEY ASSERTION IN THIS FILE: the exception did not escape. Had it
    # propagated, the worker would have crashed with the run still marked
    # "queued" — and the UI would show a ticket stuck mid-analysis with nothing
    # to explain why. Instead the failure is caught, recorded, and the run closed.
    #
    # For an unexpected failure the error_code falls back to the EXCEPTION CLASS
    # NAME, rather than the hand-written strings used by the two policy refusals
    # above. That way unknown failures are still grouped sensibly without anyone
    # having to enumerate them in advance.
    assert run.error_code == "ModelProviderResponseError"

    # The human-readable detail is kept separately, so an operator can see what
    # actually went wrong without the alerting rules depending on this wording.
    assert run.error_message == "invalid model output"

    # And again: a failed analysis leaves no partial recommendation behind.
    assert recommendations == []
