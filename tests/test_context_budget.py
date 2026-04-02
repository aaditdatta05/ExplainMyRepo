from app.services.context_budget import apply_context_budget


def test_apply_context_budget_keeps_within_limit() -> None:
    files = {
        "README.md": "a" * 30,
        "app/main.py": "b" * 40,
        "app/service.py": "c" * 50,
    }
    result = apply_context_budget(
        ["README.md", "app/main.py", "app/service.py"],
        files,
        max_chars=70,
    )

    assert result.selected_paths == ["README.md", "app/main.py"]
    assert result.dropped_paths == ["app/service.py"]
    assert result.consumed_chars == 70
