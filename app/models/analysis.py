from dataclasses import dataclass, field


@dataclass(slots=True)
class Citation:
    file_path: str
    reason: str


@dataclass(slots=True)
class AnalysisContext:
    repo_url: str
    repo_owner: str
    repo_name: str
    important_files: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    detected_languages: list[str] = field(default_factory=list)


@dataclass(slots=True)
class ExplanationSections:
    overview: str
    modules: str
    flow: str


@dataclass(slots=True)
class ExplanationResult:
    context: AnalysisContext
    sections: ExplanationSections
    citations: list[Citation]
