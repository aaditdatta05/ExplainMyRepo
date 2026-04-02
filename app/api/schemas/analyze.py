from typing import Literal

from pydantic import BaseModel, Field, HttpUrl


class AnalyzeRepositoryRequest(BaseModel):
    repository_url: HttpUrl = Field(description="GitHub repository URL to analyze")


class CitationResponse(BaseModel):
    file_path: str
    reason: str


class AnalyzeRepositoryResponse(BaseModel):
    repository_url: str
    overview: str
    modules: str
    flow: str
    markdown: str
    structured: dict[str, object]
    citations: list[CitationResponse]


class AnalyzeExportRequest(BaseModel):
    repository_url: HttpUrl = Field(description="GitHub repository URL to analyze")
    format: Literal["markdown", "json"] = "markdown"
