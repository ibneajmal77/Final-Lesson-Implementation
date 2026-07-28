# ============================================================================
# FILE: apps/api/supportops_api/checks.py
#
# THINK OF THIS FILE AS: the app's self-test kit.
#
# It answers one question: "are the things I depend on actually reachable
# right now?" There are two such things — the Postgres database and Redis —
# and there is one small test for each.
#
# WHY THIS MATTERS:
#   The API can start up perfectly happily while the database is still booting
#   or has fallen over. If traffic were sent to it in that state, every request
#   would fail. So deployment systems (Docker, Kubernetes) repeatedly call the
#   /ready endpoint, which uses these functions, and only send real users to
#   the app once it answers "yes, everything I need is working".
#
# WHO USES IT:
#   routes/health.py  - the only caller; wraps these into the /ready endpoint
#   docker-compose.yml - its `healthcheck:` sections call that endpoint
# ============================================================================

from dataclasses import dataclass

import psycopg  # the low-level driver for talking to Postgres
import redis  # the client library for talking to Redis

from supportops_api.settings import Settings


# The answer from one check. Deliberately tiny: did it work, and if not, what
# kind of failure was it? "frozen=True" means the result can't be edited after
# it is created.
@dataclass(frozen=True)
class CheckResult:
    ok: bool
    error: str | None = None      # only filled in when ok is False


# Is the database reachable and answering?
#
# It runs "select 1" — a query that asks Postgres for the number 1 and nothing
# more. It touches no tables, so it is as cheap as a query can be, while still
# proving the whole path works: network reachable, login accepted, database
# able to respond.
def check_database(settings: Settings) -> CheckResult:
    try:
        # connect_timeout=2 means "give up after 2 seconds". Vital for a health
        # check: without it, an unreachable database would leave this hanging,
        # and the health check itself would become the thing that is broken.
        #
        # The `with` blocks guarantee the connection and cursor are closed
        # afterwards, whether this succeeds or fails. A "cursor" is just the
        # handle used to run a query and read its results.
        with psycopg.connect(settings.database_url, connect_timeout=2) as connection:
            with connection.cursor() as cursor:
                cursor.execute("select 1")
                cursor.fetchone()     # actually read the answer back, proving the
                                      # round trip completed rather than just started
    except Exception as exc:
        # Catching every possible error on purpose: the point of a health check
        # is to REPORT a problem, never to crash because of one.
        #
        # Only the error's type name is returned (e.g. "OperationalError"), not
        # its full message. That is a security decision — the full message from
        # a database driver often contains the host name, user name, or even
        # the password from the connection string, and this result is sent out
        # over the internet to whoever called /ready.
        return CheckResult(ok=False, error=exc.__class__.__name__)

    return CheckResult(ok=True)


# Is Redis reachable and answering?
#
# Same shape as the database check above. "ping" is Redis's built-in "are you
# there?" command; a healthy server replies "PONG".
def check_redis(settings: Settings) -> CheckResult:
    try:
        # Two separate timeouts, because there are two different ways to hang:
        #   socket_connect_timeout - how long to wait to establish the connection
        #   socket_timeout         - how long to wait for a reply once connected
        client = redis.Redis.from_url(
            settings.redis_url,
            socket_connect_timeout=2,
            socket_timeout=2,
        )
        client.ping()
    except Exception as exc:
        return CheckResult(ok=False, error=exc.__class__.__name__)

    return CheckResult(ok=True)
