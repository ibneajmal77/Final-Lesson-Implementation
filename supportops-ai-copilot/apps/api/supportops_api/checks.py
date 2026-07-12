from dataclasses import dataclass

import psycopg
import redis

from supportops_api.settings import Settings


@dataclass(frozen=True)
class CheckResult:
    ok: bool
    error: str | None = None


def check_database(settings: Settings) -> CheckResult:
    try:
        with psycopg.connect(settings.database_url, connect_timeout=2) as connection:
            with connection.cursor() as cursor:
                cursor.execute("select 1")
                cursor.fetchone()
    except Exception as exc:
        return CheckResult(ok=False, error=exc.__class__.__name__)

    return CheckResult(ok=True)


def check_redis(settings: Settings) -> CheckResult:
    try:
        client = redis.Redis.from_url(
            settings.redis_url,
            socket_connect_timeout=2,
            socket_timeout=2,
        )
        client.ping()
    except Exception as exc:
        return CheckResult(ok=False, error=exc.__class__.__name__)

    return CheckResult(ok=True)
