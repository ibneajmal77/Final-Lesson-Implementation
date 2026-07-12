from fastapi import FastAPI

from support_api.settings import get_settings
from support_api.routes import router

def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name)
    app.include_router(router)
    return app

app = create_app()