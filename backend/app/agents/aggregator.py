from app.schemas.review import FindingSchema, FindingSeverity, SeverityBreakdown


class ReviewAggregator:
    @staticmethod
    def deduplicate_findings(findings: list[FindingSchema]) -> list[FindingSchema]:
        """
        Removes duplicate findings with identical file_path, title, and line overlap.
        """
        seen_keys = set()
        unique_findings = []

        for finding in findings:
            key = (finding.file_path, finding.title.strip().lower(), finding.line_start)
            if key not in seen_keys:
                seen_keys.add(key)
                unique_findings.append(finding)

        return unique_findings

    @staticmethod
    def calculate_health_score(findings: list[FindingSchema]) -> int:
        """
        Calculates an overall PR Health Score from 0 to 100 based on weighted finding severities.
        """
        penalty = 0
        for f in findings:
            if f.severity == FindingSeverity.CRITICAL:
                penalty += 30
            elif f.severity == FindingSeverity.HIGH:
                penalty += 15
            elif f.severity == FindingSeverity.MEDIUM:
                penalty += 5
            elif f.severity == FindingSeverity.LOW:
                penalty += 2
            elif f.severity == FindingSeverity.INFO:
                penalty += 0

        score = max(0, 100 - penalty)
        return score

    @staticmethod
    def get_severity_breakdown(findings: list[FindingSchema]) -> SeverityBreakdown:
        breakdown = SeverityBreakdown()
        for f in findings:
            if f.severity == FindingSeverity.CRITICAL:
                breakdown.CRITICAL += 1
            elif f.severity == FindingSeverity.HIGH:
                breakdown.HIGH += 1
            elif f.severity == FindingSeverity.MEDIUM:
                breakdown.MEDIUM += 1
            elif f.severity == FindingSeverity.LOW:
                breakdown.LOW += 1
            elif f.severity == FindingSeverity.INFO:
                breakdown.INFO += 1
        return breakdown

    @classmethod
    def aggregate(
        cls, raw_findings: list[FindingSchema]
    ) -> tuple[int, SeverityBreakdown, list[FindingSchema], str]:
        unique_findings = cls.deduplicate_findings(raw_findings)

        # Sort findings by severity priority
        severity_order = {
            FindingSeverity.CRITICAL: 0,
            FindingSeverity.HIGH: 1,
            FindingSeverity.MEDIUM: 2,
            FindingSeverity.LOW: 3,
            FindingSeverity.INFO: 4,
        }
        sorted_findings = sorted(
            unique_findings, key=lambda f: (severity_order.get(f.severity, 5), -f.confidence)
        )

        score = cls.calculate_health_score(sorted_findings)
        breakdown = cls.get_severity_breakdown(sorted_findings)

        if score >= 90:
            summary = "Excellent code quality. Minor or no risks identified in pull request."
        elif score >= 75:
            summary = "Good code quality overall. A few medium/low priority improvements suggested."
        elif score >= 50:
            summary = (
                "Moderate risk pull request. Several high/medium severity findings "
                "require developer review."
            )
        else:
            summary = (
                "CRITICAL RISK: Multiple severe security or bug vulnerabilities detected. "
                "Immediate revision required."
            )

        return score, breakdown, sorted_findings, summary
