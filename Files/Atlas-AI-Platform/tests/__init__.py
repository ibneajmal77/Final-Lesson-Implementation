"""Test package marker.

Python treats directories with `__init__.py` as importable packages. Keeping the
tests package importable helps pytest and mypy resolve local test helpers.
"""
