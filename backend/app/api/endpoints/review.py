from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.schemas.review import PRReviewRequest, PRReviewResponse
from app.skills.pr_review_skill import PRReviewSkill
from app.services.github_service import GitHubServiceError
from app.models.review import ReviewReportModel, PullRequestModel, RepositoryModel, FindingModel

router = APIRouter()


@router.post("/review", response_model=PRReviewResponse, status_code=status.HTTP_200_OK)
async def analyze_pull_request(
    request: PRReviewRequest,
    db: AsyncSession = Depends(get_db)
):
    try:
        skill = PRReviewSkill(db=db)
        response = await skill.execute(request)
        return response
    except GitHubServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected review error: {str(exc)}")


@router.get("/review/{report_id}", response_model=PRReviewResponse)
async def get_review_report(
    report_id: str,
    db: AsyncSession = Depends(get_db)
):
    stmt = (
        select(ReviewReportModel)
        .where(ReviewReportModel.id == report_id)
        .options(
            selectinload(ReviewReportModel.pull_request).selectinload(PullRequestModel.repository),
            selectinload(ReviewReportModel.findings)
        )
    )
    result = await db.execute(stmt)
    report = result.scalar_one_or_none()

    if not report:
        raise HTTPException(status_code=404, detail="Review report not found.")

    pr = report.pull_request
    repo = pr.repository

    from app.schemas.review import PRMetadata, SeverityBreakdown, FindingSchema
    from app.agents.aggregator import ReviewAggregator

    findings_schema = [FindingSchema.model_validate(f) for f in report.findings]
    breakdown = ReviewAggregator.get_severity_breakdown(findings_schema)

    return PRReviewResponse(
        id=report.id,
        pr_metadata=PRMetadata(
            owner=repo.owner,
            repo=repo.name,
            pr_number=pr.pr_number,
            title=pr.title,
            author=pr.author,
            html_url=pr.html_url,
            state=pr.state,
            base_branch=pr.base_branch,
            head_branch=pr.head_branch,
            changed_files_count=pr.changed_files_count,
            additions=pr.additions,
            deletions=pr.deletions
        ),
        overall_score=report.overall_score,
        summary=report.summary,
        findings_count=len(findings_schema),
        severity_breakdown=breakdown,
        findings=findings_schema,
        created_at=report.created_at.isoformat()
    )


@router.get("/recent", response_model=List[PRReviewResponse])
async def list_recent_reviews(
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    stmt = (
        select(ReviewReportModel)
        .order_by(ReviewReportModel.created_at.desc())
        .limit(limit)
        .options(
            selectinload(ReviewReportModel.pull_request).selectinload(PullRequestModel.repository),
            selectinload(ReviewReportModel.findings)
        )
    )
    result = await db.execute(stmt)
    reports = result.scalars().all()

    from app.schemas.review import PRMetadata, FindingSchema
    from app.agents.aggregator import ReviewAggregator

    responses = []
    for report in reports:
        pr = report.pull_request
        repo = pr.repository
        findings_schema = [FindingSchema.model_validate(f) for f in report.findings]
        breakdown = ReviewAggregator.get_severity_breakdown(findings_schema)

        responses.append(PRReviewResponse(
            id=report.id,
            pr_metadata=PRMetadata(
                owner=repo.owner,
                repo=repo.name,
                pr_number=pr.pr_number,
                title=pr.title,
                author=pr.author,
                html_url=pr.html_url,
                state=pr.state,
                base_branch=pr.base_branch,
                head_branch=pr.head_branch,
                changed_files_count=pr.changed_files_count,
                additions=pr.additions,
                deletions=pr.deletions
            ),
            overall_score=report.overall_score,
            summary=report.summary,
            findings_count=len(findings_schema),
            severity_breakdown=breakdown,
            findings=findings_schema,
            created_at=report.created_at.isoformat()
        ))

    return responses
