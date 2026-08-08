from enum import Enum
from typing import List, Optional, Dict
from pydantic import BaseModel, Field, HttpUrl, ConfigDict


class FindingSeverity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


class FindingCategory(str, Enum):
    BUG = "BUG"
    SECURITY = "SECURITY"
    CODE_QUALITY = "CODE_QUALITY"
    TESTING = "TESTING"
    PERFORMANCE = "PERFORMANCE"
    MAINTAINABILITY = "MAINTAINABILITY"


class FindingSchema(BaseModel):
    id: Optional[str] = None
    severity: FindingSeverity
    category: FindingCategory
    file_path: str = Field(..., description="File path relative to repository root")
    line_start: Optional[int] = Field(None, description="Starting line number of finding")
    line_end: Optional[int] = Field(None, description="Ending line number of finding")
    title: str = Field(..., description="Short summary title of finding")
    description: str = Field(..., description="Detailed description of problem")
    why_it_matters: str = Field(..., description="Impact explanation for developer")
    suggested_fix: str = Field(..., description="Actionable code fix or guidance snippet")
    confidence: float = Field(..., ge=0.0, le=1.0, description="AI confidence score between 0.0 and 1.0")

    model_config = ConfigDict(from_attributes=True)


class SeverityBreakdown(BaseModel):
    CRITICAL: int = 0
    HIGH: int = 0
    MEDIUM: int = 0
    LOW: int = 0
    INFO: int = 0


class PRMetadata(BaseModel):
    owner: str
    repo: str
    pr_number: int
    title: str
    author: str
    html_url: str
    state: str
    base_branch: str
    head_branch: str
    changed_files_count: int
    additions: int
    deletions: int


class PRReviewRequest(BaseModel):
    repo_url: Optional[str] = Field(None, description="Full GitHub PR URL e.g. https://github.com/owner/repo/pull/1")
    owner: Optional[str] = None
    repo: Optional[str] = None
    pr_number: Optional[int] = None
    ai_provider: Optional[str] = Field(None, description="Override AI provider (gemini, nvidia, mock)")


class PRReviewResponse(BaseModel):
    id: str
    pr_metadata: PRMetadata
    overall_score: int = Field(..., ge=0, le=100, description="Overall PR Health Score from 0 to 100")
    summary: str
    findings_count: int
    severity_breakdown: SeverityBreakdown
    findings: List[FindingSchema]
    created_at: str

    model_config = ConfigDict(from_attributes=True)
