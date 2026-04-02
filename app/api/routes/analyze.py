from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_analysis_orchestrator
from app.api.schemas import AnalyzeRepositoryRequest, AnalyzeRepositoryResponse, CitationResponse
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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except LLMCallError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="LLM provider unavailable. Please retry.",
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
