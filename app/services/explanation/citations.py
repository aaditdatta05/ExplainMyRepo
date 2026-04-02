from app.models.analysis import Citation


def build_grounding_citations(important_files: list[str]) -> list[Citation]:
    citations: list[Citation] = []
    for path in important_files:
        citations.append(
            Citation(
                file_path=path,
                reason="File was identified as a high-signal project artifact.",
            )
        )
    return citations
