import re
from guardrails.core.base_rule import InputRule
from guardrails.core.rule_result import RuleResult
from guardrails.core.enums import RuleStatus, Severity, Action


class InjectionDetectionRule(InputRule):
    name = "InjectionDetectionRule"
    severity = Severity.CRITICAL

    # Common prompt injection patterns
    INJECTION_PATTERNS = [
        r"ignore\s+previous\s+instructions",
        r"forget\s+all\s+rules",
        r"you\s+are\s+now",
        r"act\s+as",
        r"system\s*:",
        r"developer\s*:",
        r"jailbreak",
        r"do\s+anything\s+now"
    ]

    def check(self, text: str, context=None) -> RuleResult:
        lowered = text.lower()

        for pattern in self.INJECTION_PATTERNS:
            if re.search(pattern, lowered):
                return RuleResult(
                    rule_name=self.name,
                    status=RuleStatus.FAIL,
                    severity=self.severity,
                    action=Action.BLOCK,
                    message=f"Prompt injection attempt detected: pattern '{pattern}'",
                    metadata={"matched_pattern": pattern}
                )

        return RuleResult(
            rule_name=self.name,
            status=RuleStatus.PASS,
            severity=Severity.LOW,
            action=Action.ALLOW,
            message="No prompt injection detected"
        )
