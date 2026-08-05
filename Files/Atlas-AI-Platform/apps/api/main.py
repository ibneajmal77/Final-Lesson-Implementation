"""ASGI entry point used by Uvicorn.

This module is intentionally tiny: importing `app` gives the server a concrete
FastAPI instance, equivalent to exposing the built web host in ASP.NET Core.
"""

from apps.api.app import create_app

app = create_app()
