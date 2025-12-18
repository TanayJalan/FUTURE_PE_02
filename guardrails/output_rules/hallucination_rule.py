import re
from guardrails.core.base_rule import OutputRule
from guardrails.core.rule_result import RuleResult
from guardrails.core.enums import RuleStatus, Severity, Action


class HallucinationDetectionRule(OutputRule):
    """
    Detects potential hallucinations in LLM outputs using
    signal-based risk scoring.
    """

    name = "HallucinationDetectionRule"

    # --- Hallucination signals ---

    ABSOLUTE_CLAIMS = [
        r"\balways\b",
        r"\bnever\b",
        r"\bdefinitely\b",
        r"\bguaranteed\b",
        r"\b100%\b",
    ]

    FAKE_CITATIONS = [
        r"according to a study",
        r"research shows that",
        r"study from .* university",
        r"report from .* institute",
    ]

    UNSOURCED_STATS = [
        r"\d+(\.\d+)?%",
        r"\d+\s+million",
        r"\d+\s+billion",
    ]

    def check(self, text: str, context=None) -> RuleResult:
        lowered = text.lower()
        risk_score = 0
        reasons = []

        # 1️⃣ Absolute / overconfident language
        for pattern in self.ABSOLUTE_CLAIMS:
            if re.search(pattern, lowered):
                risk_score += 1
                reasons.append(f"Absolute claim detected ({pattern})")

        # 2️⃣ Fake or unverifiable citations
        for pattern in self.FAKE_CITATIONS:
            if re.search(pattern, lowered):
                risk_score += 2
                reasons.append("Unverifiable citation detected")

        # 3️⃣ Statistics without sources
        for pattern in self.UNSOURCED_STATS:
            if re.search(pattern, lowered):
                risk_score += 1
                reasons.append("Statistic mentioned without source")

        # --- Decision logic ---

        # 🔴 HIGH RISK → REWRITE
        if risk_score >= 3:
            return RuleResult(
                rule_name=self.name,
                status=RuleStatus.WARN,
                severity=Severity.HIGH,
                action=Action.REWRITE,
                message="High hallucination risk detected",
                metadata={
                    "risk_score": risk_score,
                    "reasons": reasons
                }
            )

        # 🟡 MEDIUM RISK → WARN
        if risk_score >= 1:
            return RuleResult(
                rule_name=self.name,
                status=RuleStatus.WARN,
                severity=Severity.MEDIUM,
                action=Action.WARN,
                message="Moderate hallucination risk detected",
                metadata={
                    "risk_score": risk_score,
                    "reasons": reasons
                }
            )

        # 🟢 LOW RISK → ALLOW
        return RuleResult(
            rule_name=self.name,
            status=RuleStatus.PASS,
            severity=Severity.LOW,
            action=Action.ALLOW,
            message="Low hallucination risk",
            metadata=None
        )
