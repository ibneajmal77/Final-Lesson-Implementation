# ============================================================================
# FILE: apps/worker/supportops_worker/main.py
#
# THINK OF THIS FILE AS: the "on" switch for the background worker.
#
# This is a whole separate program from the API. It has no web server, no
# endpoints, and nobody ever sends it a request. It does exactly one thing,
# forever: watch the Redis to-do list, and whenever a job appears, run it.
#
# The two programs are started separately — see docker-compose.yml, where "api"
# and "worker" are two different services running from the same code.
#
# HOW TO RUN IT:
#   python -m supportops_worker.main
#   (docker-compose.yml runs exactly this as the worker container's command)
#
# WHY IT IS SO SHORT:
#   Almost all the real behaviour comes from RQ, the job-queue library. This
#   file only assembles the pieces — connection, queue list, logging — and then
#   hands control over. The actual work lives in jobs.py.
#
# THE OTHER HALF OF THE PICTURE:
#   apps/worker/supportops_worker/queues.py - how jobs get ONTO the list
#   apps/worker/supportops_worker/jobs.py   - what happens when one is picked up
# ============================================================================

from redis import Redis

# Note it reuses the API's settings module. Both programs read the same
# environment variables, so they are guaranteed to agree about which database
# and which Redis they are talking to. Two separate settings files would be an
# invitation for them to drift apart and quietly stop cooperating.
from supportops_api.settings import get_settings
from supportops_observability.logging import configure_json_logging, get_logger
from supportops_worker.queues import AI_ANALYSIS_QUEUE

logger = get_logger(__name__)


def main() -> None:
    # RQ is imported here rather than at the top of the file so that a missing
    # dependency produces a plain, actionable sentence instead of a wall of
    # import traceback. SystemExit stops the program cleanly with that message
    # on screen — the person seeing it needs to install requirements, not debug.
    try:
        from rq import Queue, Worker  # type: ignore[import-not-found]
    except ImportError as exc:
        message = "RQ is not installed. Install requirements.txt before starting worker."
        raise SystemExit(message) from exc

    settings = get_settings()

    # Logging is configured here as well as in the API's main.py. Each is its own
    # operating-system process with its own logging setup, so neither can rely on
    # the other having done it.
    configure_json_logging(settings.log_level)

    connection = Redis.from_url(settings.redis_url)

    # A list, because RQ can watch several queues at once. Only the AI analysis
    # queue is watched here, even though queues.py also defines "evals" and
    # "maintenance" — those exist for work that is currently triggered by other
    # means. Adding them would be one entry in this list.
    queues = [Queue(AI_ANALYSIS_QUEUE, connection=connection)]

    # Logged before the blocking call below, so the logs show the worker came up
    # successfully. Without this line, a healthy idle worker and a worker that
    # crashed on startup would look identical: silent.
    logger.info("worker_starting", extra={"route": "worker", "job_id": AI_ANALYSIS_QUEUE})

    worker = Worker(queues, connection=connection)

    # THE LINE THAT NEVER RETURNS. work() enters an endless loop: wait for a job,
    # run it, wait for the next. This call is where the process spends its entire
    # life, and it only ends when the process is stopped.
    #
    # Note it WAITS rather than repeatedly asking "anything yet?" — Redis notifies
    # it when a job arrives, so an idle worker uses essentially no CPU.
    #
    # Each job runs in a forked child process (RQ's default on Linux). That is
    # why a job that crashes outright, or leaks memory, cannot take the worker
    # down with it — the parent survives and simply picks up the next job.
    worker.work()


# Only runs when this file is executed directly, not when it is imported.
if __name__ == "__main__":
    main()
