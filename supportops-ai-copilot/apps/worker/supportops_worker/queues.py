# ============================================================================
# FILE: apps/worker/supportops_worker/queues.py
#
# THINK OF THIS FILE AS: the "to-do list" mechanism connecting the API to the
# background worker.
#
# THE PROBLEM IT SOLVES:
#   Asking an AI a question takes seconds. If the API did that while someone
#   waited, the web page would freeze, and a burst of tickets would exhaust the
#   server's connections while every one of them sat idle waiting on the AI.
#
#   So the work is handed off. The API writes "job 123 needs doing" onto a
#   shared list and replies immediately; a separate worker program takes jobs
#   off that list and does them. The list lives in Redis, which both programs
#   can reach.
#
#   The pieces are deliberately loosely joined: the API doesn't know how many
#   workers exist, and the workers don't know who created the job. If every
#   worker is down, jobs simply pile up on the list and get processed when one
#   comes back.
#
# THE JOURNEY OF ONE JOB:
#   routes/tickets.py calls enqueue_ai_analysis(run_id)   <- THIS FILE
#     -> the ID is pushed onto the Redis list
#          -> main.py (the worker process) is watching that list and pulls it off
#               -> jobs.py does the actual AI work
#
# NOTE WHAT TRAVELS ON THE QUEUE: only an ID, never the ticket text. The worker
# looks up whatever it needs from the database itself. That keeps the queue
# small and guarantees the worker reads current data rather than a copy that
# may have changed since the job was created.
# ============================================================================

from dataclasses import dataclass
from typing import Protocol

# The names of the separate to-do lists. Keeping different kinds of work apart
# means a flood of one type cannot starve another — a thousand queued evaluation
# runs will not delay a customer's ticket analysis.
AI_ANALYSIS_QUEUE = "ai_analysis"    # the live one: analysing customer tickets
EVALS_QUEUE = "evals"                # scoring runs from packages/evals/
MAINTENANCE_QUEUE = "maintenance"    # housekeeping, e.g. the retention cleanup

# Every queue name in one tuple, so other code can loop over them all without
# repeating the list and eventually forgetting to update one copy.
ALL_QUEUE_NAMES = (AI_ANALYSIS_QUEUE, EVALS_QUEUE, MAINTENANCE_QUEUE)


# Raised when the queue system itself cannot be used at all.
#
# It exists so that "Redis is unreachable" is a distinct, recognisable failure
# rather than a generic crash. routes/tickets.py catches it and turns it into a
# clear 503 response, and marks the job sheet failed rather than leaving it
# stuck at "pending" forever.
class QueueUnavailableError(RuntimeError):
    pass


# The receipt handed back after a job is queued: which job, on which list.
# Mostly useful for logging — it is what lets you match a line in the API's log
# to the corresponding line in the worker's log.
@dataclass(frozen=True)
class EnqueuedJob:
    id: str
    queue_name: str


# A "Protocol" is a contract, not an implementation: it says "anything with a
# method shaped like this counts as an AnalysisQueue", without demanding that it
# inherit from anything.
#
# The point is testability. The tests can pass in a simple fake object that
# records calls in a list, and the code under test cannot tell the difference —
# so the API's queueing logic can be tested with no Redis running at all. That
# is why routes/tickets.py accepts the queue as an injected dependency rather
# than building one itself.
class AnalysisQueue(Protocol):
    def enqueue_ai_analysis(self, ai_run_id: str) -> EnqueuedJob:
        """Enqueue async AI analysis for an existing ai_runs row."""


# The real implementation, built on RQ ("Redis Queue"), a small and widely used
# Python job-queue library.
class RQAnalysisQueue:
    # Notice the constructor does NOT connect to Redis. It only remembers the
    # address. That is deliberate: creating this object can never fail, so a
    # Redis outage cannot prevent the API from starting up — it only affects the
    # individual requests that actually try to queue something.
    def __init__(self, *, redis_url: str, queue_name: str = AI_ANALYSIS_QUEUE) -> None:
        self._redis_url = redis_url
        self._queue_name = queue_name

    def enqueue_ai_analysis(self, ai_run_id: str) -> EnqueuedJob:
        # The imports sit inside the method, not at the top of the file, so that
        # this module can be imported even where RQ isn't installed — which is
        # what makes the fake queue usable in tests without pulling in Redis.
        # A missing library becomes our own clear error rather than a crash at
        # import time.
        try:
            from redis import Redis
            from rq import Queue  # type: ignore[import-not-found]
        except ImportError as exc:
            raise QueueUnavailableError("RQ is not installed") from exc

        connection = Redis.from_url(self._redis_url)
        queue = Queue(self._queue_name, connection=connection)

        # The job is recorded as a TEXT path to a function plus its arguments —
        # not as the function object itself. RQ writes this into Redis, and the
        # worker process later reads the text and imports that function to run
        # it. That indirection is what lets two entirely separate programs agree
        # on what work to do.
        #
        # The consequence worth remembering: if that function is ever renamed or
        # moved, this string must change too, or queued jobs will fail with an
        # import error. It is a link the compiler cannot check for you.
        job = queue.enqueue_call(
            func="supportops_worker.jobs.analyze_ticket_job",
            args=(ai_run_id,),      # a tuple with one item; the trailing comma is what
                                    # makes it a tuple rather than plain brackets
        )
        return EnqueuedJob(id=job.id, queue_name=self._queue_name)


# The one place that decides which queue implementation the app gets.
#
# A "factory function" like this exists so callers depend on the contract rather
# than the concrete class. Swapping RQ for a different queue system later would
# mean changing this one line, and nothing else. Called from get_ai_analysis_queue()
# in apps/api/supportops_api/dependencies.py.
def build_analysis_queue(redis_url: str) -> AnalysisQueue:
    return RQAnalysisQueue(redis_url=redis_url)
