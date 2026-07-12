from fastapi import FastAPI

from supportops_api.routes.approvals import router as approvals_router
from supportops_api.routes.health import router as health_router
from supportops_api.routes.metrics import router as metrics_router
from supportops_api.routes.tickets import router as tickets_router
from supportops_api.settings import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name)
    app.include_router(health_router)
    app.include_router(metrics_router)
    app.include_router(approvals_router)
    app.include_router(tickets_router)
    return app


app = create_app()
