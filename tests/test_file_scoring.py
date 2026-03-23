from app.services.file_scoring import rank_important_files, score_file_importance


def test_score_file_importance_prefers_core_project_files() -> None:
    assert score_file_importance("README.md") > score_file_importance("notes/todo.txt")
    assert score_file_importance("app/main.py") > score_file_importance("scripts/helper.sh")


def test_rank_important_files_orders_by_score_then_path() -> None:
    ranked = rank_important_files(
        [
            "docs/notes.md",
            "README.md",
            "app/main.py",
            "tests/test_service.py",
        ],
        limit=3,
    )

    assert len(ranked) == 3
    assert ranked[0].path == "README.md"
