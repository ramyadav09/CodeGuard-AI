from app.schemas.review import FindingSchema, FindingSeverity, FindingCategory
from app.agents.aggregator import ReviewAggregator


def test_calculate_health_score():
    findings = [
        FindingSchema(
            severity=FindingSeverity.CRITICAL,
            category=FindingCategory.SECURITY,
            file_path="app.py",
            title="Hardcoded Secret",
            description="Secret committed",
            why_it_matters="Security risk",
            suggested_fix="Remove secret",
            confidence=0.95
        ),
        FindingSchema(
            severity=FindingSeverity.HIGH,
            category=FindingCategory.BUG,
            file_path="app.py",
            title="Null Pointer",
            description="Unhandled null",
            why_it_matters="Crash risk",
            suggested_fix="Add null check",
            confidence=0.90
        )
    ]
    # Score = 100 - 30 - 15 = 55
    score = ReviewAggregator.calculate_health_score(findings)
    assert score == 55


def test_deduplicate_findings():
    f1 = FindingSchema(
        severity=FindingSeverity.CRITICAL,
        category=FindingCategory.SECURITY,
        file_path="app.py",
        line_start=10,
        title="Hardcoded Secret",
        description="Secret committed",
        why_it_matters="Security risk",
        suggested_fix="Remove secret",
        confidence=0.95
    )
    f2 = FindingSchema(
        severity=FindingSeverity.CRITICAL,
        category=FindingCategory.SECURITY,
        file_path="app.py",
        line_start=10,
        title="Hardcoded Secret",
        description="Duplicate finding",
        why_it_matters="Security risk",
        suggested_fix="Remove secret",
        confidence=0.95
    )

    deduped = ReviewAggregator.deduplicate_findings([f1, f2])
    assert len(deduped) == 1
