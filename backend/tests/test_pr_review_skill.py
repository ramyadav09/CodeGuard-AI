from unittest.mock import AsyncMock, patch

import pytest

from app.schemas.review import PRMetadata, PRReviewRequest
from app.skills.pr_review_skill import PRReviewSkill


@pytest.mark.asyncio
async def test_pr_review_skill_direct_owner_repo(db_session):
    skill = PRReviewSkill(db=db_session)
    request = PRReviewRequest(owner="octocat", repo="Hello-World", pr_number=1, ai_provider="mock")

    mock_metadata = PRMetadata(
        owner="octocat",
        repo="Hello-World",
        pr_number=1,
        title="Direct PR details",
        author="octocat",
        html_url="https://github.com/octocat/Hello-World/pull/1",
        state="open",
        base_branch="master",
        head_branch="patch-1",
        changed_files_count=1,
        additions=5,
        deletions=2,
    )
    mock_diff = "diff --git a/README.md b/README.md"

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

        response = await skill.execute(request)
        assert response.pr_metadata.owner == "octocat"
        assert response.id != "temp-report-id"


@pytest.mark.asyncio
async def test_pr_review_skill_no_db():
    skill = PRReviewSkill(db=None)
    request = PRReviewRequest(
        repo_url="https://github.com/octocat/Hello-World/pull/1", ai_provider="mock"
    )

    mock_metadata = PRMetadata(
        owner="octocat",
        repo="Hello-World",
        pr_number=1,
        title="Direct PR details",
        author="octocat",
        html_url="https://github.com/octocat/Hello-World/pull/1",
        state="open",
        base_branch="master",
        head_branch="patch-1",
        changed_files_count=1,
        additions=5,
        deletions=2,
    )
    mock_diff = "diff --git a/README.md b/README.md"

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

        response = await skill.execute(request)
        assert response.pr_metadata.owner == "octocat"
        assert response.id == "temp-report-id"


@pytest.mark.asyncio
async def test_pr_review_skill_invalid_input():
    skill = PRReviewSkill(db=None)
    request = PRReviewRequest(ai_provider="mock")

    with pytest.raises(
        ValueError, match="Must provide either repo_url or owner, repo, and pr_number"
    ):
        await skill.execute(request)


@pytest.mark.asyncio
async def test_pr_review_skill_db_error(db_session):
    skill = PRReviewSkill(db=db_session)
    request = PRReviewRequest(owner="octocat", repo="Hello-World", pr_number=1, ai_provider="mock")

    mock_metadata = PRMetadata(
        owner="octocat",
        repo="Hello-World",
        pr_number=1,
        title="DB error PR",
        author="octocat",
        html_url="https://github.com/octocat/Hello-World/pull/1",
        state="open",
        base_branch="master",
        head_branch="patch-1",
        changed_files_count=1,
        additions=5,
        deletions=2,
    )
    mock_diff = "diff --git a/README.md b/README.md"

    with (
        patch(
            "app.services.github_service.GitHubService.get_pr_metadata",
            new_callable=AsyncMock,
        ) as mock_get_meta,
        patch(
            "app.services.github_service.GitHubService.get_pr_diff",
            new_callable=AsyncMock,
        ) as mock_get_diff,
        patch.object(db_session, "execute", side_effect=Exception("Simulated DB failure")),
    ):
        mock_get_meta.return_value = mock_metadata
        mock_get_diff.return_value = mock_diff

        response = await skill.execute(request)
        # Rollback was called, returned response with fallback ID
        assert response.id == "temp-report-id"
