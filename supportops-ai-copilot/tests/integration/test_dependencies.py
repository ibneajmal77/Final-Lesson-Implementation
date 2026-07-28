# ============================================================================
# FILE: tests/integration/test_dependencies.py
#
# WHAT THIS TESTS: whether the API can complete a real round trip to the
# PostgreSQL database and Redis queue used by the integration CI job.
#
# THINK OF THIS FILE AS: plugging the app into the wall and checking that both
# of its external services answer, after the smaller tests have checked the
# individual parts in isolation.
#
# An INTEGRATION test checks several real pieces working together. This one uses
# the actual psycopg and Redis clients in apps/api/supportops_api/checks.py, not
# stand-ins. .github/workflows/ci.yml starts disposable PostgreSQL and Redis
# containers, supplies their addresses, and explicitly turns this test on.
#
#     CI service containers
#       -> environment variables -> Settings
#          -> check_database + check_redis -> real network round trips
#
# HONEST LIMITATION: this proves reachability, login, and a minimal response. It
# does not apply migrations, inspect tables, exercise the AI queue, or test how
# the app recovers from an outage; other CI jobs and tests cover those concerns.
# ============================================================================
#
import os

import pytest

from supportops_api.checks import check_database, check_redis
from supportops_api.settings import Settings

# A pytest MARKER is a label attached to tests. Assigning it at module level
# labels every test in this file as `integration`, so commands can select or
# exclude this slower, externally dependent category. pyproject.toml registers
# the marker, and .github/workflows/ci.yml runs this directory in its own job.
pytestmark = pytest.mark.integration


# There is one test because the question is deliberately narrow: can this
# process reach both services using the same settings shape as the real API?
def test_postgres_and_redis_are_reachable_in_ci() -> None:
    # Normal local test runs do not promise that either service exists. A SKIP
    # is neither a pass nor a failure: pytest records that the required setup was
    # absent. CI sets this opt-in flag only after starting both service containers.
    if os.environ.get("RUN_INTEGRATION_TESTS") != "1":
        pytest.skip("set RUN_INTEGRATION_TESTS=1 to run external dependency checks")

    # Build Settings directly rather than relying on a local `.env` file. Square
    # brackets on os.environ deliberately fail loudly if CI turns the test on
    # but forgets either address. `mock` keeps unrelated AI credentials out of a
    # test concerned only with storage and queue infrastructure.
    settings = Settings(
        app_env="ci",
        database_url=os.environ["DATABASE_URL"],
        redis_url=os.environ["REDIS_URL"],
        model_provider="mock",
    )

    # check_database opens a real psycopg connection and executes `select 1`;
    # check_redis sends Redis its lightweight `PING` command. Both functions use
    # short timeouts, so broken infrastructure fails this job promptly.
    database = check_database(settings)
    redis = check_redis(settings)

    # The value after each comma is pytest's failure message. check_database and
    # check_redis intentionally expose only an exception TYPE, not a connection
    # string that might contain a password, so the CI log stays useful and safe.
    assert database.ok, database.error
    assert redis.ok, redis.error
