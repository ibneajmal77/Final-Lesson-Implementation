"""Repo-root import shim for the SupportOps evaluation runner.

This keeps `python -m supportops_evals.runner` working from a source checkout without
requiring an editable install during the lesson stages.
"""

# ============================================================================
# FILE: supportops_evals/__init__.py   (at the REPOSITORY ROOT)
#
# THINK OF THIS FILE AS: a signpost. It is not the real evaluation package — it
# is a small piece of trickery that makes the real one importable without
# installing anything.
#
# DO NOT CONFUSE IT WITH packages/evals/supportops_evals/, which holds the
# actual code. Two folders share a name, and this one exists purely to point at
# the other.
#
# THE PROBLEM IT SOLVES:
#   You want to run `python -m supportops_evals.runner` from the project root.
#   But the real package lives at packages/evals/supportops_evals/, and Python
#   only searches a fixed list of locations. Normally you would install the
#   package to fix that. This project deliberately avoids an install step, so
#   that a fresh checkout runs immediately.
#
#   This file bridges the gap by editing Python's search paths at import time.
#
# IS THIS GOOD PRACTICE? Honestly, no — it is a workaround. Path manipulation at
# import time is the kind of thing that produces confusing failures later, and it
# is why the mypy configuration in pyproject.toml excludes this file. A
# production project would use a proper editable install (`pip install -e .`).
# It is a reasonable trade for a teaching repository, where "clone it and run"
# matters more.
# ============================================================================

import sys
from pathlib import Path

# `.parent.parent` climbs two levels: this file -> supportops_evals/ -> the
# repository root. Note this is brittle in the usual way — moving this file would
# silently make the path wrong.
_ROOT = Path(__file__).resolve().parent.parent

# The package folders that need to be findable. Roughly the same list as in
# Dockerfile.api, pyproject.toml, and migrations/env.py — four copies of the same
# information, which is exactly the maintenance burden a proper install would
# remove.
_PACKAGE_ROOTS = (
    _ROOT / "apps" / "api",
    _ROOT / "apps" / "worker",
    _ROOT / "packages" / "db",
    _ROOT / "packages" / "domain",
    _ROOT / "packages" / "model_gateway",
    _ROOT / "packages" / "prompts",
    _ROOT / "packages" / "observability",
)

# Adds each folder to the FRONT of Python's search path.
#
# `reversed(...)` combined with `insert(0, ...)` is a small piece of care: each
# insertion goes to position 0, so processing the list backwards leaves the final
# order matching the list as written. Without the reverse, the order would be
# inverted — which only matters if two packages ever shadowed each other, but
# getting it right costs nothing.
#
# The two conditions prevent adding a folder that does not exist, and adding the
# same one twice.
for package_root in reversed(_PACKAGE_ROOTS):
    package_root_text = str(package_root)
    if package_root.exists() and package_root_text not in sys.path:
        sys.path.insert(0, package_root_text)

# THE ACTUAL TRICK, and the most unusual two lines in the codebase.
#
# `__path__` is a special variable on a package: it tells Python where to look
# for that package's own submodules. Appending to it here means "when someone
# asks for supportops_evals.runner, also look inside
# packages/evals/supportops_evals/".
#
# The effect is that this nearly-empty folder BEHAVES AS IF it contained the real
# runner.py, reports.py, and scoring.py. Python calls this a namespace extension;
# it is legitimate, rarely seen, and the reason `python -m supportops_evals.runner`
# works from the repository root with nothing installed.
_EVALS_PACKAGE = _ROOT / "packages" / "evals" / "supportops_evals"
_evals_package_text = str(_EVALS_PACKAGE)
if _EVALS_PACKAGE.exists() and _evals_package_text not in __path__:
    __path__.append(_evals_package_text)
