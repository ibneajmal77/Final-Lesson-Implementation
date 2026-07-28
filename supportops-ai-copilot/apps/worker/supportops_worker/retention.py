# ============================================================================
# FILE: apps/worker/supportops_worker/retention.py
#
# THINK OF THIS FILE AS: the shredder — the part that deletes old data once we
# are no longer entitled to keep it.
#
# WHY A PROGRAM EXISTS PURELY TO DELETE THINGS:
#   Privacy law (GDPR and similar) says you may keep personal data only as long
#   as you have a reason to. Support tickets are full of personal data: names,
#   email addresses, order numbers, sometimes payment details. "We kept it
#   because storage is cheap" is not a lawful reason.
#
#   So most tables in this project carry a `retention_expires_at` column — a
#   date after which that row must go. This file finds the rows past their date.
#
# IMPORTANT: AS WRITTEN, THIS DELETES NOTHING.
#   Read run_retention_deletion_job below carefully. It COUNTS expired rows and
#   logs the number, and when asked to delete for real it logs
#   "retention_deletion_not_implemented" instead. The counting half is finished;
#   the deleting half is not.
#
#   That is a defensible order to build it in — you want to watch the counts for
#   a while and be sure they look right before letting anything delete production
#   data — but it does mean the compliance promise is not yet kept. Anyone
#   relying on this needs to know that. See docs/stage-14-security-implementation.md.
#
# HOW IT IS MEANT TO BE RUN:
#   Periodically, on a schedule (nightly). Notice it takes no queue job and no
#   HTTP request — it is a standalone routine, intended for the "maintenance"
#   queue defined in queues.py or for an external scheduler.
#
# WHERE THE EXPIRY DATES COME FROM:
#   Set when rows are created, e.g. `retention_expires_at` on a policy in
#   routes/policies.py. The columns were added by migration 0007.
# ============================================================================

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from supportops_api.settings import get_settings
from supportops_db.models import (
    AIRun,
    CostEvent,
    RecommendationReview,
    TenantPolicy,
    Ticket,
    TicketRecommendation,
)
from supportops_db.session import create_db_engine, create_session_factory
from supportops_observability.logging import get_logger

logger = get_logger(__name__)


# How many expired rows were found, per table.
#
# Counted per table rather than as one lump because the tables mean different
# things. "12 expired tickets" and "12 expired cost records" call for entirely
# different reactions — cost records hold no personal data, while tickets are
# the most sensitive rows in the system.
@dataclass(frozen=True)
class RetentionCandidateCounts:
    tickets: int
    ai_runs: int
    ticket_recommendations: int
    recommendation_reviews: int
    cost_events: int
    support_policies: int

    # A "property" is a method you read like a plain value: `counts.total`, with
    # no brackets. Computed on demand rather than stored, so it can never fall
    # out of step with the six numbers above.
    @property
    def total(self) -> int:
        return (
            self.tickets
            + self.ai_runs
            + self.ticket_recommendations
            + self.recommendation_reviews
            + self.cost_events
            + self.support_policies
        )


# Counts what is currently past its expiry date, in every table.
#
# Read-only — no deletion here at all, which is what makes it safe to call any
# time, including from tests and from a monitoring check.
def collect_retention_candidates(
    session: Session,
    *,
    now: datetime | None = None,      # normally left out; see below
) -> RetentionCandidateCounts:
    # The optional `now` exists for testing. Being able to pass in a pretend
    # "today" lets a test create a row expiring next week and then ask "what
    # would be expired a fortnight from now?" without waiting or fiddling with
    # the system clock. In real use it is omitted and the real time is used.
    #
    # datetime.now(UTC) rather than plain datetime.now(): always in UTC, never
    # the server's local timezone. Time comparisons against database timestamps
    # must all be in the same timezone, or rows near the boundary get deleted
    # hours early or late — and around a daylight-saving change, both.
    cutoff = now or datetime.now(UTC)
    return RetentionCandidateCounts(
        tickets=_count_expired(session, Ticket, cutoff=cutoff),
        ai_runs=_count_expired(session, AIRun, cutoff=cutoff),
        ticket_recommendations=_count_expired(session, TicketRecommendation, cutoff=cutoff),
        recommendation_reviews=_count_expired(session, RecommendationReview, cutoff=cutoff),
        cost_events=_count_expired(session, CostEvent, cutoff=cutoff),
        support_policies=_count_expired(session, TenantPolicy, cutoff=cutoff),
    )


# The scheduled routine.
#
# NOTE THE DEFAULT: `dry_run=True`. A "dry run" means "tell me what you WOULD do,
# but don't do it". Defaulting to the harmless behaviour is the right instinct
# for anything destructive — deleting production data should require someone to
# have deliberately typed dry_run=False, never be what happens when an argument
# is forgotten.
def run_retention_deletion_job(*, dry_run: bool = True) -> RetentionCandidateCounts:
    # Builds its own database connection, like the seed script and the worker
    # job: this runs standalone, with no FastAPI request to supply one.
    settings = get_settings()
    engine = create_db_engine(settings.database_url)
    session_factory = create_session_factory(engine)

    with session_factory() as session:
        counts = collect_retention_candidates(session)

    # Logged on EVERY run, dry or not. That log line is what makes the figure
    # trackable over time — a slowly climbing count of expired-but-still-present
    # rows is exactly the signal that the unimplemented half below matters.
    logger.info(
        "retention_candidates_collected",
        extra={"job_id": "retention_deletion", "candidate_count": counts.total},
    )

    # THE UNFINISHED PART. Asked to delete for real, it logs a warning saying it
    # cannot, and deletes nothing.
    #
    # Recording it as a WARNING rather than staying silent is the right call: a
    # silent no-op would let everyone believe deletion was happening. This way,
    # anyone who runs it in earnest gets told plainly that it did not work, and
    # the warning shows up in monitoring.
    if not dry_run:
        logger.warning(
            "retention_deletion_not_implemented",
            extra={"job_id": "retention_deletion", "candidate_count": counts.total},
        )
    return counts


# Counts expired rows in ONE table.
#
# `model: Any` is what lets a single function serve all six tables. The type is
# left loose because these are SQLAlchemy model classes, which are awkward to
# describe precisely enough for a type checker while keeping this readable.
def _count_expired(session: Session, model: Any, *, cutoff: datetime) -> int:
    # Reads as: "count the rows in this table where retention_expires_at is set
    # AND has already passed".
    #
    # The `is_not(None)` half is essential. A row with no expiry date is meant to
    # be kept indefinitely, and dropping that condition would compare NULL
    # against the cutoff — which in SQL is neither true nor false, so those rows
    # would silently be excluded here, but the same mistake in a DELETE could
    # behave very differently. Being explicit removes the doubt entirely.
    #
    # Note it counts in the DATABASE (`func.count()`) rather than fetching the
    # rows and counting them in Python. Only a single number crosses the network,
    # which matters when the answer could be millions.
    count = session.scalar(
        select(func.count()).select_from(model).where(
            model.retention_expires_at.is_not(None),
            model.retention_expires_at <= cutoff,      # multiple conditions are ANDed together
        )
    )
    # `count or 0` guards the case where the query returns None instead of a
    # number — so the caller always gets a real integer and never has to
    # None-check the arithmetic in `total`.
    return int(count or 0)
