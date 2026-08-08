from unittest.mock import AsyncMock, patch

import pytest

from app.schemas.review import PRMetadata


@pytest.mark.asyncio
async def test_health_check_endpoint(client):
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "CodeGuard AI" in data["service"]


@pytest.mark.asyncio
async def test_review_endpoint_with_mock_github(client):
    mock_metadata = PRMetadata(
        owner="octocat",
        repo="Hello-World",
        pr_number=1,
        title="Correct typo in README",
        author="octocat",
        html_url="https://github.com/octocat/Hello-World/pull/1",
        state="open",
        base_branch="master",
        head_branch="patch-1",
        changed_files_count=1,
        additions=5,
        deletions=2,
    )
    mock_diff = """diff --git a/README.md b/README.md
index 7898192..2e65efe 100644
--- a/README.md
+++ b/README.md
@@ -1 +1 @@
-Hello World!
+Hello World!!
"""

    with (
        patch(
            "app.services.github_service.GitHubService.get_pr_metadata", new_callable=AsyncMock
        ) as mock_get_meta,
        patch(
            "app.services.github_service.GitHubService.get_pr_diff", new_callable=AsyncMock
        ) as mock_get_diff,
    ):
        mock_get_meta.return_value = mock_metadata
        mock_get_diff.return_value = mock_diff

        payload = {
            "repo_url": "https://github.com/octocat/Hello-World/pull/1",
            "ai_provider": "mock",
        }

        response = await client.post("/api/v1/review", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["pr_metadata"]["owner"] == "octocat"
        assert data["pr_metadata"]["repo"] == "Hello-World"
        assert "overall_score" in data
        assert len(data["findings"]) > 0


@pytest.mark.asyncio
async def test_get_review_and_recent_endpoints(client):
    mock_metadata = PRMetadata(
        owner="octocat",
        repo="Hello-World",
        pr_number=1,
        title="Correct typo in README",
        author="octocat",
        html_url="https://github.com/octocat/Hello-World/pull/1",
        state="open",
        base_branch="master",
        head_branch="patch-1",
        changed_files_count=1,
        additions=5,
        deletions=2,
    )
    mock_diff = """diff --git a/README.md b/README.md
index 7898192..2e65efe 100644
--- a/README.md
+++ b/README.md
@@ -1 +1 @@
-Hello World!
+Hello World!!
"""

    with (
        patch(
            "app.services.github_service.GitHubService.get_pr_metadata",
            new_callable=AsyncMock,
        ) as mock_get_meta,
        patch(
            "app.services.github_service.GitHubService.get_pr_diff",
            new_callable=AsyncMock,
        ) as mock_get_diff,
    ):
        mock_get_meta.return_value = mock_metadata
        mock_get_diff.return_value = mock_diff

        payload = {
            "repo_url": "https://github.com/octocat/Hello-World/pull/1",
            "ai_provider": "mock",
        }

        # 1. Create a review report
        response = await client.post("/api/v1/review", json=payload)
        assert response.status_code == 200
        report_data = response.json()
        report_id = report_data["id"]
        assert report_id != "temp-report-id"

        # 2. Get the specific report
        get_response = await client.get(f"/api/v1/review/{report_id}")
        assert get_response.status_code == 200
        get_data = get_response.json()
        assert get_data["id"] == report_id
        assert get_data["pr_metadata"]["owner"] == "octocat"
        assert get_data["overall_score"] == report_data["overall_score"]

        # 3. Get recent reviews list
        recent_response = await client.get("/api/v1/recent")
        assert recent_response.status_code == 200
        recent_data = recent_response.json()
        assert len(recent_data) > 0
        assert recent_data[0]["id"] == report_id

        # 4. Get invalid report returns 404
        invalid_response = await client.get("/api/v1/review/invalid-uuid-or-id")
        assert invalid_response.status_code == 404


@pytest.mark.asyncio
async def test_review_endpoint_returns_400_on_value_error(client):
    """POST /review with bad payload should return 400"""
    with patch(
        "app.skills.pr_review_skill.PRReviewSkill.execute",
        new_callable=AsyncMock,
        side_effect=ValueError("Must provide either repo_url or owner, repo, and pr_number."),
    ):
        response = await client.post(
            "/api/v1/review",
            json={"ai_provider": "mock"},
        )
    assert response.status_code == 400
    assert "Must provide either" in response.json()["detail"]


@pytest.mark.asyncio
async def test_review_endpoint_returns_500_on_unhandled_exception(client):
    """POST /review when skill raises unexpected error → 500"""
    with patch(
        "app.skills.pr_review_skill.PRReviewSkill.execute",
        new_callable=AsyncMock,
        side_effect=RuntimeError("unexpected failure"),
    ):
        response = await client.post(
            "/api/v1/review",
            json={"repo_url": "https://github.com/owner/repo/pull/1", "ai_provider": "mock"},
        )
    assert response.status_code == 500
    assert "unexpected failure" in response.json()["detail"]


@pytest.mark.asyncio
async def test_review_endpoint_returns_404_on_github_service_error(client):
    """POST /review when GitHub service raises 404 → 404"""
    from app.services.github_service import GitHubServiceError

    with patch(
        "app.skills.pr_review_skill.PRReviewSkill.execute",
        new_callable=AsyncMock,
        side_effect=GitHubServiceError("PR not found", status_code=404),
    ):
        response = await client.post(
            "/api/v1/review",
            json={"repo_url": "https://github.com/owner/repo/pull/999", "ai_provider": "mock"},
        )
    assert response.status_code == 404
    assert "PR not found" in response.json()["detail"]
