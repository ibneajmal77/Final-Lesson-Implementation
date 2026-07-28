# ============================================================================
# FILE: packages/db/supportops_db/base.py
#
# THINK OF THIS FILE AS: the two foundation stones every database table is
# built on. Tiny file, but everything in models.py depends on it.
#
# WHAT IS IN HERE:
#   Base      - the parent class every table model inherits from
#   utc_now   - the function that supplies "right now" for timestamp columns
#
# WHY THEY LIVE IN THEIR OWN FILE RATHER THAN IN models.py:
#   The migration system (Alembic) needs to import Base to discover what the
#   tables should look like. If Base lived in models.py, importing it would drag
#   in every model and their imports too. Keeping it separate means
#   migrations/env.py can pick up just this one small piece.
# ============================================================================

from datetime import UTC, datetime

from sqlalchemy.orm import DeclarativeBase


# The shared parent of every table class in models.py.
#
# It looks empty, and its body genuinely is — but inheriting from
# DeclarativeBase is what activates SQLAlchemy's machinery. Behind the scenes it
# gives every subclass the ability to turn `mapped_column` declarations into
# real table definitions, and it keeps a registry of every table it has seen.
#
# That registry is the important part. `Base.metadata` ends up holding the
# complete picture of the intended database, which is what
# migrations/env.py compares against the real one to detect drift.
#
# Practical consequence: a model class that does NOT inherit from Base is
# invisible to the migration system. It will simply be missed.
class Base(DeclarativeBase):
    pass


# Returns the current time, always in UTC.
#
# Used as the `default=` for nearly every timestamp column in models.py. Note
# how it is passed there — `default=utc_now` with no brackets — so SQLAlchemy
# calls it afresh for each new row.
#
# WHY UTC, ALWAYS:
#   UTC is the world's single reference timezone, with no daylight saving. The
#   alternative — recording local time — causes real, well-known problems:
#     - Servers in different regions would disagree about when things happened,
#       making it impossible to order events correctly.
#     - Every autumn, the hour when clocks go back HAPPENS TWICE locally. Two
#       different events can carry the same local timestamp, and no amount of
#       later cleverness can tell them apart.
#   Store everything in UTC and convert to the reader's local time only when
#   displaying it. The columns are declared `DateTime(timezone=True)`, so the
#   timezone travels with the value rather than being assumed.
#
# The `UTC` argument is what makes this an "aware" datetime — one that knows its
# own timezone. A plain `datetime.now()` returns a "naive" one, which claims no
# timezone at all, and mixing the two raises errors in comparisons. Hence the
# consistency here.
def utc_now() -> datetime:
    return datetime.now(UTC)
