"""SupportOps API package."""

# ============================================================================
# FILE: apps/api/supportops_api/__init__.py
#
# WHAT THIS FILE IS: a package marker.
#
# The presence of an __init__.py file is what tells Python "this folder is a
# package you can import from". Without it, `from supportops_api.settings import
# ...` would not work.
#
# It is deliberately almost empty. Code placed here runs EVERY time anything in
# the package is imported, so keeping it bare means importing one small module
# does not drag in the whole application. The one-line docstring above is all it
# needs.
#
# WHAT LIVES IN THIS PACKAGE — the HTTP API:
#   main.py         - builds the app; the starting point when the server runs
#   dependencies.py - the front desk: authentication and database sessions
#   settings.py     - configuration read from environment variables
#   checks.py       - are the database and Redis reachable?
#   pilot.py        - is the AI switched on for this company and ticket type?
#   seed.py         - a script creating the demo company and user
#   routes/         - the endpoints themselves
#   schemas/        - the exact shape of the JSON going in and out
# ============================================================================
