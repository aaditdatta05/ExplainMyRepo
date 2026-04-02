import json
from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse, StreamingResponse

from app.api.deps import get_analysis_orchestrator
from app.api.errors import AppError
from app.api.schemas import (
    AnalyzeExportRequest,
    AnalyzeRepositoryRequest,
    AnalyzeRepositoryResponse,
    CitationResponse,
)
from app.services.analysis import InvalidRepositoryUrlError, RepositoryAnalysisOrchestrator
from app.services.llm import LLMCallError

router = APIRouter(prefix="/analyze", tags=["analysis"])


@router.post("", response_model=AnalyzeRepositoryResponse, status_code=status.HTTP_200_OK)
async def analyze_repository(
    payload: AnalyzeRepositoryRequest,
    orchestrator: Annotated[
        RepositoryAnalysisOrchestrator,
        Depends(get_analysis_orchestrator),
    ],
) -> AnalyzeRepositoryResponse:
    try:
        result, markdown_output, structured_output = await orchestrator.analyze(
            str(payload.repository_url)
        )
    except InvalidRepositoryUrlError as exc:
        raise AppError(
            code="invalid_repository_url",
            message=str(exc),
            status_code=status.HTTP_400_BAD_REQUEST,
        ) from exc
    except LLMCallError as exc:
        raise AppError(
            code="llm_unavailable",
            message="LLM provider unavailable. Please retry.",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        ) from exc

    return AnalyzeRepositoryResponse(
        repository_url=result.context.repo_url,
        overview=result.sections.overview,
        modules=result.sections.modules,
        flow=result.sections.flow,
        markdown=markdown_output,
        structured=structured_output,
        citations=[
            CitationResponse(file_path=c.file_path, reason=c.reason) for c in result.citations
        ],
    )


@router.post("/stream", status_code=status.HTTP_200_OK)
async def stream_repository_analysis(
    payload: AnalyzeRepositoryRequest,
    orchestrator: Annotated[
        RepositoryAnalysisOrchestrator,
        Depends(get_analysis_orchestrator),
    ],
) -> StreamingResponse:
    repository_url = str(payload.repository_url)

    async def event_stream():
        try:
            async for item in orchestrator.stream_analyze(repository_url):
                yield f"event: {item['event']}\ndata: {json.dumps(item['data'])}\n\n"
        except InvalidRepositoryUrlError as exc:
            error_payload = {"code": "invalid_repository_url", "message": str(exc)}
            yield f"event: error\ndata: {json.dumps(error_payload)}\n\n"
        except LLMCallError:
            error_payload = {
                "code": "llm_unavailable",
                "message": "LLM provider unavailable. Please retry.",
            }
            yield f"event: error\ndata: {json.dumps(error_payload)}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@router.post("/export", status_code=status.HTTP_200_OK)
async def export_repository_analysis(
    payload: AnalyzeExportRequest,
    orchestrator: Annotated[
        RepositoryAnalysisOrchestrator,
        Depends(get_analysis_orchestrator),
    ],
) -> JSONResponse:
    try:
        _, markdown_output, structured_output = await orchestrator.analyze(
            str(payload.repository_url)
        )
    except InvalidRepositoryUrlError as exc:
        raise AppError(
            code="invalid_repository_url",
            message=str(exc),
            status_code=status.HTTP_400_BAD_REQUEST,
        ) from exc
    except LLMCallError as exc:
        raise AppError(
            code="llm_unavailable",
            message="LLM provider unavailable. Please retry.",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        ) from exc

    if payload.format == "markdown":
        return JSONResponse(
            content={"format": "markdown", "content": markdown_output},
            headers={"Content-Disposition": "attachment; filename=analysis.md"},
        )

    return JSONResponse(
        content={"format": "json", "content": structured_output},
        headers={"Content-Disposition": "attachment; filename=analysis.json"},
    )
