import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.schemas.review import FindingCategory, FindingSeverity


def generate_uuid() -> str:
    return str(uuid.uuid4())


class RepositoryModel(Base):
    __tablename__ = "repositories"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(String(512), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    pull_requests: Mapped[list["PullRequestModel"]] = relationship(
        "PullRequestModel", back_populates="repository", cascade="all, delete-orphan"
    )


class PullRequestModel(Base):
    __tablename__ = "pull_requests"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    repository_id: Mapped[str] = mapped_column(ForeignKey("repositories.id"), nullable=False)
    pr_number: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    html_url: Mapped[str] = mapped_column(String(512), nullable=False)
    state: Mapped[str] = mapped_column(String(50), default="open")
    base_branch: Mapped[str] = mapped_column(String(255), nullable=False)
    head_branch: Mapped[str] = mapped_column(String(255), nullable=False)
    changed_files_count: Mapped[int] = mapped_column(Integer, default=0)
    additions: Mapped[int] = mapped_column(Integer, default=0)
    deletions: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    repository: Mapped["RepositoryModel"] = relationship(
        "RepositoryModel", back_populates="pull_requests"
    )
    reviews: Mapped[list["ReviewReportModel"]] = relationship(
        "ReviewReportModel", back_populates="pull_request", cascade="all, delete-orphan"
    )


class ReviewReportModel(Base):
    __tablename__ = "review_reports"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    pull_request_id: Mapped[str] = mapped_column(ForeignKey("pull_requests.id"), nullable=False)
    overall_score: Mapped[int] = mapped_column(Integer, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    pull_request: Mapped["PullRequestModel"] = relationship(
        "PullRequestModel", back_populates="reviews"
    )
    findings: Mapped[list["FindingModel"]] = relationship(
        "FindingModel", back_populates="review_report", cascade="all, delete-orphan"
    )


class FindingModel(Base):
    __tablename__ = "findings"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    review_report_id: Mapped[str] = mapped_column(ForeignKey("review_reports.id"), nullable=False)
    severity: Mapped[FindingSeverity] = mapped_column(SQLEnum(FindingSeverity), nullable=False)
    category: Mapped[FindingCategory] = mapped_column(SQLEnum(FindingCategory), nullable=False)
    file_path: Mapped[str] = mapped_column(String(512), nullable=False)
    line_start: Mapped[int | None] = mapped_column(Integer, nullable=True)
    line_end: Mapped[int | None] = mapped_column(Integer, nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    why_it_matters: Mapped[str] = mapped_column(Text, nullable=False)
    suggested_fix: Mapped[str] = mapped_column(Text, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)

    review_report: Mapped["ReviewReportModel"] = relationship(
        "ReviewReportModel", back_populates="findings"
    )
