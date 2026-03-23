from app.services.language_detection import classify_files_by_language, detect_language


def test_detect_language_by_extension() -> None:
    assert detect_language("app/main.py") == "Python"
    assert detect_language("ui/page.tsx") == "TypeScript"
    assert detect_language("README.md") == "Markdown"
    assert detect_language("artifact.bin") == "Unknown"


def test_classify_files_by_language() -> None:
    grouped = classify_files_by_language(["a.py", "b.py", "ui.tsx", "README.md"])
    assert grouped["Python"] == 2
    assert grouped["TypeScript"] == 1
    assert grouped["Markdown"] == 1
