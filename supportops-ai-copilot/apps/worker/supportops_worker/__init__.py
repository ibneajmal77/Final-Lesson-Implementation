"""Background worker package."""

# ============================================================================
# FILE: apps/worker/supportops_worker/__init__.py
#
# A package marker — its presence makes this folder importable. Intentionally
# empty of code.
#
# WHAT THIS PACKAGE IS: the second half of the system. A completely separate
# program from the API, with no web server and no endpoints. It runs as its own
# container (see docker-compose.yml) and does one thing forever: watch the Redis
# queue and process whatever appears on it.
#
# WHY IT EXISTS: asking an AI a question takes seconds. Doing that inside a web
# request would freeze the page and tie up a server connection the whole time.
# So the API writes down "this job needs doing" and replies immediately; this
# program picks the job up and does the slow part on its own time.
#
# THE FILES:
#   main.py      - the "on" switch. Connects to Redis and enters the work loop
#   queues.py    - how jobs get ONTO the queue (used by the API, not by the worker)
#   jobs.py      - the heart of it: what actually happens when a job is picked up
#   retention.py - the privacy cleanup routine (counting is done; deletion is not)
#
# Note it reuses the API's settings module rather than defining its own, so both
# halves are guaranteed to agree about which database, which Redis, and which
# pilot rules apply.
# ============================================================================
