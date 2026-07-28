# ============================================================================
# FILE: packages/db/supportops_db/repositories/ai_runs.py
#
# THINK OF THIS FILE AS: the job-sheet drawer for queued AI work — creating job
# sheets, reading them, and moving them through their states.
#
# Unlike the other repositories, this one is mostly about CHANGING rows rather
# than creating them. That is because a job sheet has a lifetime: it is created
# empty, then updated as the work progresses.
#
# THE STATE MACHINE THIS FILE IMPLEMENTS:
#
#            create_ai_run
#                 |
#              [queued]  <- written by the API, waiting in Redis
#                 |          mark_ai_run_running
#              [running] <- the worker has picked it up
#                 |
#         +-------+--------+-------------+
#         |                |             |
#    [succeeded]      [abstained]     [failed]
#     got an answer   AI declined     something broke
#                     to answer
#
#   Every arrow is one of the mark_* functions below, and each is called from
#   apps/worker/supportops_worker/jobs.py at the matching point.
#
# WHY "abstained" IS SEPARATE FROM "failed":
#   An AI saying "this ticket is too ambiguous, I won't guess" is behaving WELL.
#   Counting that as a failure would push the system toward models that always
#   guess, which is the opposite of what you want in something drafting replies
#   to customers. So it gets its own honest label — and it is not counted as a
#   success either, since no usable answer was produced.
# ============================================================================

from sqlalchemy import select
from sqlalchemy.orm import Session

from supportops_db.base import utc_now
from supportops_db.models import AIRun

# The status values written as named constants rather than loose strings.
#
# The reason is simple: a typo in a constant name ("AI_RUN_STATUS_SUCEEDED")
# fails loudly and immediately, while a typo in a bare string ("suceeded") is
# stored happily and only surfaces weeks later as a report where the numbers
# quietly do not add up.
AI_RUN_STATUS_QUEUED = "queued"
AI_RUN_STATUS_RUNNING = "running"
AI_RUN_STATUS_SUCCEEDED = "succeeded"
AI_RUN_STATUS_FAILED = "failed"
AI_RUN_STATUS_ABSTAINED = "abstained"


# Creates a job sheet, in the "queued" state.
#
# Called by routes/tickets.py BEFORE the job is pushed onto Redis, and that
# order is deliberate. Written first, a job that never reaches the queue still
# leaves a visible record stuck in "queued" that someone can find and retry.
# Queued first, a crash before writing would leave the worker holding an ID for
# a row that does not exist.
#
# `model_name` and `prompt_version` are optional because they are not always
# known yet — the worker chooses the prompt template when it actually runs, and
# fills the value in later.
def create_ai_run(
    session: Session,
    *,
    tenant_id: str,
    ticket_id: str,
    run_type: str,               # "ticket_analysis" today; room for other AI jobs later
    model_provider: str,
    model_name: str | None,
    prompt_version: str | None,
    input_hash: str,             # fingerprint of the ticket text, so identical inputs are
                                 # recognisable without storing the text twice
) -> AIRun:
    run = AIRun(
        tenant_id=tenant_id,
        ticket_id=ticket_id,
        run_type=run_type,
        status=AI_RUN_STATUS_QUEUED,     # always starts here
        model_provider=model_provider,
        model_name=model_name,
        prompt_version=prompt_version,
        input_hash=input_hash,
    )
    session.add(run)
    session.flush()
    return run


# Fetches a job sheet by ID alone, with NO tenant filter.
#
# THE ONE DELIBERATE EXCEPTION to the tenant-filtering rule that every other
# lookup in this project follows. It exists for the worker: when a job arrives
# off the queue, all the worker has is an ID. It has no user, no company, and no
# way to know which tenant to filter by — the row itself is what tells it.
#
# That is safe here because the worker is trusted internal code, not something
# reachable from outside. But it is exactly why the function below exists.
def get_ai_run_by_id(session: Session, *, ai_run_id: str) -> AIRun | None:
    return session.scalar(select(AIRun).where(AIRun.id == ai_run_id))


# The same lookup, WITH the tenant filter — the version anything user-facing
# must use.
#
# Having both, under clearly different names, is better than one function with
# an optional tenant argument. An optional filter is easy to forget; two named
# functions make the unfiltered one an obvious, deliberate choice that stands
# out in review.
def get_ai_run_for_tenant(session: Session, *, tenant_id: str, ai_run_id: str) -> AIRun | None:
    return session.scalar(
        select(AIRun).where(
            AIRun.tenant_id == tenant_id,
            AIRun.id == ai_run_id,
        )
    )


# Lists the analysis attempts for one ticket, newest first.
# This is what the web page polls after starting a queued analysis, watching for
# the top entry's status to change.
def list_ai_runs_for_ticket(
    session: Session,
    *,
    tenant_id: str,
    ticket_id: str,
    limit: int = 50,
) -> list[AIRun]:
    return list(
        session.scalars(
            select(AIRun)
            .where(
                AIRun.tenant_id == tenant_id,
                AIRun.ticket_id == ticket_id,
            )
            .order_by(AIRun.created_at.desc())
            .limit(limit)
        )
    )


# --- The four state transitions --------------------------------------------
#
# These all work differently from every other function in this folder. They take
# an AIRun OBJECT that the caller already has, and change its fields directly.
# Because SQLAlchemy tracks objects it loaded, simply assigning to an attribute
# is enough — it works out the UPDATE statement itself. There is no explicit
# "save" call anywhere below.


# queued -> running. Called the moment the worker picks the job up.
def mark_ai_run_running(session: Session, run: AIRun) -> AIRun:
    run.status = AI_RUN_STATUS_RUNNING
    run.started_at = utc_now()      # starts the clock; comparing this with created_at
                                    # tells you how long the job waited in the queue
    # Clearing any previous error is what makes a RETRY behave correctly. If this
    # job sheet had failed before and is being run again, leaving the old error
    # in place would produce a row that says "running" while still displaying a
    # failure message — confusing to anyone reading it.
    run.error_code = None
    run.error_message = None
    session.flush()
    return run


# running -> succeeded. The happy ending.
def mark_ai_run_succeeded(
    session: Session,
    run: AIRun,
    *,
    output_recommendation_id: str,   # links the job sheet to the result it produced.
                                     # This is what lets the polling page show the answer
                                     # in the same reply that says "done"
    model_name: str | None,
    prompt_version: str | None,      # now known, unlike when the sheet was created
) -> AIRun:
    run.status = AI_RUN_STATUS_SUCCEEDED
    run.output_recommendation_id = output_recommendation_id
    run.model_name = model_name
    run.prompt_version = prompt_version
    run.finished_at = utc_now()      # stops the clock
    session.flush()
    return run


# running -> abstained. The AI declined to answer.
#
# Note this is IDENTICAL to mark_ai_run_succeeded apart from the status value —
# it still records a recommendation, because the AI's explanation of WHY it
# abstained is genuinely useful to the human who picks the ticket up.
#
# The near-duplication is a reasonable choice: two clearly named functions read
# better at the call site in jobs.py than one function taking a status argument,
# and it leaves room for the two paths to diverge later.
def mark_ai_run_abstained(
    session: Session,
    run: AIRun,
    *,
    output_recommendation_id: str,
    model_name: str | None,
    prompt_version: str | None,
) -> AIRun:
    run.status = AI_RUN_STATUS_ABSTAINED
    run.output_recommendation_id = output_recommendation_id
    run.model_name = model_name
    run.prompt_version = prompt_version
    run.finished_at = utc_now()
    session.flush()
    return run


# anything -> failed. Something broke.
def mark_ai_run_failed(
    session: Session,
    run: AIRun,
    *,
    error_code: str,        # short and stable, e.g. "queue_unavailable". Safe to group
                            # and count in dashboards
    error_message: str,     # the full human-readable detail
) -> AIRun:
    run.status = AI_RUN_STATUS_FAILED
    run.error_code = error_code

    # `[:2000]` truncates to the first 2,000 characters. Worth understanding why:
    # error messages from libraries can be enormous — a full stack trace, or an
    # entire HTTP response body. Storing those unbounded would bloat the table
    # and, worse, could drag a large chunk of a customer's ticket text into a
    # column that gets read casually while debugging. Truncating keeps the useful
    # opening of the message and discards the rest.
    #
    # Note this slice never fails: a shorter string is simply returned whole.
    run.error_message = error_message[:2000]

    # `finished_at` is set even on failure. Correct — the job IS finished, it just
    # ended badly, and leaving this empty would make failed jobs look permanently
    # stuck to anything scanning for runaway work.
    run.finished_at = utc_now()
    session.flush()
    return run
