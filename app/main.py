from fastapi import FastAPI

from app.api.routes.analyze import router as analyze_router
from app.api.routes.health import router as health_router
from app.core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="ExplainMyRepo API", version="0.1.0")
    app.state.settings = settings
    app.include_router(health_router)
    app.include_router(analyze_router)
    return app


app = create_app()
