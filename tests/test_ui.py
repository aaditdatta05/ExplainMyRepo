from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_ui_index_renders() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "ExplainMyRepo" in response.text
