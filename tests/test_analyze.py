from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_analyze_repository_success() -> None:
    response = client.post(
        "/analyze",
        json={"repository_url": "https://github.com/psf/requests"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["repository_url"] == "https://github.com/psf/requests"
    assert "overview" in payload
    assert "markdown" in payload
    assert isinstance(payload["citations"], list)


def test_analyze_repository_form_success() -> None:
    response = client.post(
        "/analyze/form",
        data={"repository_url": "https://github.com/psf/requests"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["repository_url"] == "https://github.com/psf/requests"


def test_analyze_repository_invalid_url_returns_error_model() -> None:
    response = client.post(
        "/analyze",
        json={"repository_url": "https://example.com/not-github/repo"},
    )

    assert response.status_code == 400
    payload = response.json()
    assert payload["code"] == "invalid_repository_url"
    assert "message" in payload


def test_analyze_stream_returns_sse_payload() -> None:
    with client.stream(
        "POST",
        "/analyze/stream",
        json={"repository_url": "https://github.com/psf/requests"},
    ) as response:
        body = "".join(response.iter_text())

    assert response.status_code == 200
    assert "event: status" in body
    assert "event: result" in body
    assert "event: complete" in body


def test_analyze_export_markdown() -> None:
    response = client.post(
        "/analyze/export",
        json={
            "repository_url": "https://github.com/psf/requests",
            "format": "markdown",
        },
    )

    assert response.status_code == 200
    assert response.json()["format"] == "markdown"


def test_analyze_export_json() -> None:
    response = client.post(
        "/analyze/export",
        json={
            "repository_url": "https://github.com/psf/requests",
            "format": "json",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["format"] == "json"
    assert "sections" in payload["content"]
