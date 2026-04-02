from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_metrics_endpoint_returns_counters() -> None:
    client.get("/health")

    response = client.get("/metrics")

    assert response.status_code == 200
    payload = response.json()
    assert "total_requests" in payload
    assert "total_errors" in payload
    assert "average_latency_ms" in payload
