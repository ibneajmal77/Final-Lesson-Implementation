# ============================================================================
# FILE: packages/db/supportops_db/migrations/env.py
#
# THINK OF THIS FILE AS: the setup script the migration tool runs before
# applying any database change.
#
# WHAT "MIGRATIONS" ARE, AND WHY THEY EXIST:
#   models.py describes what the tables SHOULD look like. But a database that is
#   already running, with real data in it, cannot be reshaped by editing a Python
#   file. Something has to issue the actual "add this column", "create this
#   table" commands — in the right order, exactly once each, on every copy of the
#   database (your laptop, staging, production).
#
#   That is a migration: a small numbered script recording one change. Run them
#   in order from an empty database and you arrive at the current schema. The
#   tool managing all this is called Alembic, and it keeps a table inside your
#   database recording which migrations have already been applied, so it always
#   knows what is left to do.
#
#   The numbered scripts live in versions/ next door. THIS file is the shared
#   setup they all rely on.
#
# WHAT IT ACTUALLY DOES, in three steps:
#   1. Makes the project's packages importable (the sys.path block below)
#   2. Works out the database address, reusing the app's own settings
#   3. Opens a connection and runs whichever migrations are outstanding
#
# HOW IT GETS RUN: by the `alembic upgrade head` command. "head" means "the
# newest migration". The command is configured by alembic.ini in the project
# root, and appears in the setup steps in README.md.
#
# NOTE THIS FILE HAS NO main() AND NO if __name__ GUARD. The code at the very
# bottom runs on import, because Alembic imports this file rather than calling
# into it. That is the tool's convention, not a mistake.
# ============================================================================

import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config, pool

# --- Step 1: make the project's own packages importable ---------------------
#
# This project is a "monorepo": several separate packages (api, worker, db,
# domain, ...) living in one repository, each in its own folder. Normally they
# would be installed so Python could find them. Alembic, however, runs this file
# directly, without the project's usual startup, so those packages are invisible.
#
# The loop below adds each package folder to sys.path — the list of places Python
# searches for imports — so the lines further down can import them.
#
# `parents[4]` climbs four folders up from this file to reach the project root:
#   migrations -> supportops_db -> db -> packages -> the repository root
# Counting folder levels like this is brittle: MOVING THIS FILE WOULD SILENTLY
# BREAK IT, because the number would no longer be right.
_REPO_ROOT = Path(__file__).resolve().parents[4]
for _relative_path in (
    "apps/api",
    "apps/worker",
    "packages/db",
    "packages/domain",
    "packages/model_gateway",
    "packages/prompts",
    "packages/evals",
    "packages/observability",
):
    _package_path = str(_REPO_ROOT / _relative_path)
    if _package_path not in sys.path:      # don't add the same folder twice
        sys.path.insert(0, _package_path)  # insert(0) puts it FIRST, so the project's
                                           # own packages win over any installed ones

# These imports sit BELOW the path setup because they depend on it — they would
# fail if placed at the top of the file in the usual way.
#
# `# noqa: E402` switches off the style checker's complaint about exactly that
# ("module level import not at top of file"). A rare case where breaking the
# convention is genuinely necessary, and the marker documents that it was
# deliberate rather than careless.
from supportops_api.settings import get_settings  # noqa: E402
from supportops_db.models import Base  # noqa: E402
from supportops_db.session import to_sqlalchemy_url  # noqa: E402

# Alembic's own configuration object, holding whatever alembic.ini contains.
config = context.config

# Sets up logging from that same file, if there is one, so the migration output
# is readable.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# THE IMPORTANT LINE. `Base.metadata` is the complete picture of what the tables
# SHOULD look like, gathered automatically from every model class in models.py
# (see base.py for how that registry works).
#
# Handing it to Alembic is what enables `alembic revision --autogenerate`:
# comparing this intended shape against the real database and writing a
# migration for the differences. Autogeneration is a helpful first draft, not a
# finished answer — it misses things like renames, which it sees as one column
# dropped and another added, destroying the data in the process.
target_metadata = Base.metadata


# The database address, taken from the app's own settings.
#
# Reusing get_settings() rather than reading a separate value out of alembic.ini
# matters: it guarantees migrations are applied to exactly the database the
# application uses. Two sources of truth here would eventually mean migrating one
# database while the app talks to another — a confusing failure, since the app
# would report missing columns that you just watched being created.
def _database_url() -> str:
    settings = get_settings()
    return to_sqlalchemy_url(settings.database_url)     # adds the "+psycopg" driver part


# --- The two ways migrations can run ----------------------------------------

# OFFLINE mode: connects to nothing. Instead of applying changes, it PRINTS the
# SQL that would be run.
#
# Useful when the person writing the migration is not allowed to touch the
# production database — a common arrangement in regulated environments. The SQL
# is generated here, reviewed, and handed to a database administrator to run.
def run_migrations_offline() -> None:
    context.configure(
        url=_database_url(),
        target_metadata=target_metadata,
        # `literal_binds=True` writes values directly into the SQL text rather
        # than using placeholders. Necessary because the output is meant to be
        # run by hand later, when the separate list of parameter values would
        # not be available.
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# ONLINE mode: the normal path. Connects to the database and applies the changes.
def run_migrations_online() -> None:
    config.set_main_option("sqlalchemy.url", _database_url())
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        # `NullPool` means "no connection pooling" — open one connection, use it,
        # close it. Right for a migration: it is a one-off command that runs and
        # exits, so a pool of reusable connections would be pure overhead, and
        # lingering connections could hold locks on tables being altered.
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        # Everything inside one transaction, so a migration that fails halfway
        # is rolled back entirely rather than leaving the database in a
        # half-changed state that neither matches the old shape nor the new one.
        with context.begin_transaction():
            context.run_migrations()


# The entry point. Runs on import, which is how Alembic expects this file to work.
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
