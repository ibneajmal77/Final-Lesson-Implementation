"""Database package for SupportOps."""

# ============================================================================
# FILE: packages/db/supportops_db/__init__.py
#
# A package marker — its presence makes this folder importable. Intentionally
# empty of code.
#
# WHAT THIS PACKAGE IS: everything to do with the database. Shared by the API,
# the worker, the seeding script, and the tests, which is why it is a separate
# package rather than living inside either application.
#
# THE FILES AND FOLDERS:
#   models.py      - the blueprint: every table and column, as Python classes
#   base.py        - the two foundations every model builds on
#   session.py     - opening the connection and handing out sessions
#   repositories/  - ALL the database queries. Nothing else writes SQL
#   migrations/    - the numbered scripts that actually create and alter tables
#
# THE TWO IDEAS WORTH CARRYING AWAY:
#
#   1. THE REPOSITORY PATTERN. Routes and worker code never write queries; they
#      call functions in repositories/. That keeps the SQL in one place, and —
#      because those functions take tenant_id as a REQUIRED argument — makes it
#      impossible to write a query that accidentally reads another company's
#      data.
#
#   2. models.py DOES NOT CREATE THE TABLES. Changing a line there does nothing
#      to a running database; only a migration does. The two must be kept in step
#      by hand, and CI runs `alembic check` to catch it when they are not.
# ============================================================================
