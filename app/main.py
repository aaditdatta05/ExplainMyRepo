from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.deps import get_metrics_registry
from app.api.errors import AppError
from app.api.routes.analyze import router as analyze_router
from app.api.routes.health import router as health_router
from app.api.routes.metrics import router as metrics_router
from app.api.routes.ui import router as ui_router
from app.api.schemas import ErrorResponse
from app.core.config import get_settings
from app.core.observability import metrics_middleware


def create_app() -> FastAPI:
    settings = get_settings()
    metrics_registry = get_metrics_registry()

    app = FastAPI(title="ExplainMyRepo API", version="0.1.0")
    app.state.settings = settings

    @app.exception_handler(AppError)
    async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
        payload = ErrorResponse(code=exc.code, message=exc.message)
        return JSONResponse(status_code=exc.status_code, content=payload.model_dump())

    @app.middleware("http")
    async def metrics_http_middleware(request: Request, call_next):
        return await metrics_middleware(request, call_next, metrics_registry)

    app.include_router(health_router)
    app.include_router(ui_router)
    app.include_router(metrics_router)
    app.include_router(analyze_router)
    return app


app = create_app()
