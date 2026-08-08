from app.agents.aggregator import ReviewAggregator
from app.schemas.review import FindingCategory, FindingSchema, FindingSeverity


def _make(severity: FindingSeverity, i: int = 0) -> FindingSchema:
    return FindingSchema(
        severity=severity,
        category=FindingCategory.SECURITY,
        file_path=f"app_{i}.py",
        title=f"Issue {i}",
        description="desc",
        why_it_matters="matters",
        suggested_fix="fix it",
        confidence=0.90,
    )


def test_calculate_health_score():
    findings = [
        _make(FindingSeverity.CRITICAL),  # -30
        _make(FindingSeverity.HIGH, 1),  # -15
    ]
    # Score = 100 - 30 - 15 = 55
    score = ReviewAggregator.calculate_health_score(findings)
    assert score == 55


def test_calculate_health_score_low_and_info():
    findings = [
        _make(FindingSeverity.LOW),  # -2
        _make(FindingSeverity.INFO, 1),  # -0
    ]
    score = ReviewAggregator.calculate_health_score(findings)
    assert score == 98  # 100 - 2 - 0


def test_severity_breakdown_all_levels():
    findings = [
        _make(FindingSeverity.CRITICAL, 0),
        _make(FindingSeverity.HIGH, 1),
        _make(FindingSeverity.MEDIUM, 2),
        _make(FindingSeverity.LOW, 3),
        _make(FindingSeverity.INFO, 4),
    ]
    breakdown = ReviewAggregator.get_severity_breakdown(findings)
    assert breakdown.CRITICAL == 1
    assert breakdown.HIGH == 1
    assert breakdown.MEDIUM == 1
    assert breakdown.LOW == 1
    assert breakdown.INFO == 1


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
        confidence=0.95,
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
        confidence=0.95,
    )

    deduped = ReviewAggregator.deduplicate_findings([f1, f2])
    assert len(deduped) == 1


def test_aggregate_produces_summary_excellent():
    """Score >= 90 -> Excellent summary"""
    findings: list[FindingSchema] = []  # no findings = score 100
    score, _breakdown, sorted_f, summary = ReviewAggregator.aggregate(findings)
    assert score == 100
    assert "Excellent" in summary
    assert len(sorted_f) == 0


def test_aggregate_produces_summary_good():
    """Score >= 75 -> Good summary (5 x MEDIUM = -25 -> score=75)"""
    five_medium = [_make(FindingSeverity.MEDIUM, i) for i in range(5)]
    score, _, _, summary = ReviewAggregator.aggregate(five_medium)
    assert 75 <= score < 90
    assert "Good" in summary


def test_aggregate_produces_summary_moderate():
    """Score in [50, 75) -> Moderate summary (3 x HIGH = -45 -> score=55)"""
    three_high = [_make(FindingSeverity.HIGH, i) for i in range(3)]
    score, _, _, summary = ReviewAggregator.aggregate(three_high)
    assert 50 <= score < 75
    assert "Moderate" in summary


def test_aggregate_produces_summary_critical():
    """Score < 50 -> CRITICAL RISK summary (3 x CRITICAL = -90 -> score=10)"""
    findings = [_make(FindingSeverity.CRITICAL, i) for i in range(3)]
    score, _, _, summary = ReviewAggregator.aggregate(findings)
    assert score < 50
    assert "CRITICAL RISK" in summary
