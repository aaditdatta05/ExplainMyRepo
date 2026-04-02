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
