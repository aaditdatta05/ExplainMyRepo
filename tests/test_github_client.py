import httpx
import pytest

from app.services.github_client import GitHubClient, GitHubClientError


def test_github_client_reads_repository_payload() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/repos/psf/requests"
        return httpx.Response(
            200,
            json={
                "full_name": "psf/requests",
                "default_branch": "main",
                "description": "Python HTTP for Humans.",
            },
        )

    transport = httpx.MockTransport(handler)
    client = GitHubClient()
    client._client = httpx.Client(base_url="https://api.github.com", transport=transport)

    repo = client.get_repository("psf", "requests")

    assert repo.full_name == "psf/requests"
    assert repo.default_branch == "main"


def test_github_client_raises_on_http_error() -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(404, text="Not Found")

    transport = httpx.MockTransport(handler)
    client = GitHubClient()
    client._client = httpx.Client(base_url="https://api.github.com", transport=transport)

    with pytest.raises(GitHubClientError):
        client.get_repository("missing", "repo")
