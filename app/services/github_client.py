from dataclasses import dataclass

import httpx


class GitHubClientError(RuntimeError):
    """Raised when GitHub API requests fail."""


@dataclass(frozen=True)
class GitHubRepository:
    full_name: str
    default_branch: str
    description: str | None


class GitHubClient:
    def __init__(self, token: str | None = None, timeout: float = 15.0) -> None:
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "ExplainMyRepo/0.1.0",
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"

        self._client = httpx.Client(
            base_url="https://api.github.com",
            headers=headers,
            timeout=timeout,
        )

    def close(self) -> None:
        self._client.close()

    def get_repository(self, owner: str, name: str) -> GitHubRepository:
        response = self._client.get(f"/repos/{owner}/{name}")
        if response.status_code >= 400:
            raise GitHubClientError(
                f"GitHub API request failed with status {response.status_code}: {response.text}"
            )

        payload = response.json()
        return GitHubRepository(
            full_name=payload["full_name"],
            default_branch=payload["default_branch"],
            description=payload.get("description"),
        )

    def __enter__(self) -> "GitHubClient":
        return self

    def __exit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        self.close()
