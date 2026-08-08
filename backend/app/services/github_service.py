import re
from typing import Tuple, Dict, Any, Optional
import httpx
from app.core.config import settings
from app.schemas.review import PRMetadata


class GitHubServiceError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class GitHubService:
    def __init__(self, token: Optional[str] = None):
        self.token = token or settings.GITHUB_TOKEN
        self.base_url = "https://api.github.com"

    def _get_headers(self, accept: str = "application/vnd.github.v3+json") -> Dict[str, str]:
        headers = {
            "Accept": accept,
            "User-Agent": "CodeGuard-AI-App"
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    @staticmethod
    def parse_pr_url(pr_url: str) -> Tuple[str, str, int]:
        """
        Parses a GitHub PR URL into (owner, repo, pr_number).
        Example: https://github.com/facebook/react/pull/1024 -> ('facebook', 'react', 1024)
        """
        pattern = r"github\.com/([^/]+)/([^/]+)/pull/(\d+)"
        match = re.search(pattern, pr_url)
        if not match:
            raise GitHubServiceError("Invalid GitHub PR URL format. Expected: https://github.com/owner/repo/pull/123")
        owner, repo, pr_number = match.group(1), match.group(2), int(match.group(3))
        return owner, repo, pr_number

    async def get_pr_metadata(self, owner: str, repo: str, pr_number: int) -> PRMetadata:
        """Fetches PR details from GitHub REST API."""
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}"
        async with httpx.AsyncClient(timeout=15.0) as client:
            try:
                response = await client.get(url, headers=self._get_headers())
            except httpx.RequestError as exc:
                raise GitHubServiceError(f"Network error connecting to GitHub API: {str(exc)}", status_code=503)

            if response.status_code == 404:
                raise GitHubServiceError(f"GitHub PR #{pr_number} not found in repository {owner}/{repo}", status_code=404)
            elif response.status_code == 401:
                raise GitHubServiceError("Unauthorized GitHub API request. Check your GITHUB_TOKEN.", status_code=401)
            elif response.status_code != 200:
                raise GitHubServiceError(f"GitHub API error ({response.status_code}): {response.text}", status_code=response.status_code)

            data = response.json()
            return PRMetadata(
                owner=owner,
                repo=repo,
                pr_number=pr_number,
                title=data.get("title", f"PR #{pr_number}"),
                author=data.get("user", {}).get("login", "unknown"),
                html_url=data.get("html_url", f"https://github.com/{owner}/{repo}/pull/{pr_number}"),
                state=data.get("state", "open"),
                base_branch=data.get("base", {}).get("ref", "main"),
                head_branch=data.get("head", {}).get("ref", "patch"),
                changed_files_count=data.get("changed_files", 0),
                additions=data.get("additions", 0),
                deletions=data.get("deletions", 0)
            )

    async def get_pr_diff(self, owner: str, repo: str, pr_number: int) -> str:
        """Fetches the raw git unified diff for a PR."""
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}"
        headers = self._get_headers(accept="application/vnd.github.v3.diff")
        async with httpx.AsyncClient(timeout=20.0) as client:
            try:
                response = await client.get(url, headers=headers)
            except httpx.RequestError as exc:
                raise GitHubServiceError(f"Network error fetching PR diff: {str(exc)}", status_code=503)

            if response.status_code != 200:
                raise GitHubServiceError(f"Failed to fetch PR diff ({response.status_code}): {response.text}", status_code=response.status_code)

            return response.text
