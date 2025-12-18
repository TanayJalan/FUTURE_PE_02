import re
from guardrails.core.base_rule import InputRule
from guardrails.core.rule_result import RuleResult
from guardrails.core.enums import RuleStatus, Severity, Action


class SafetyPolicyRule(InputRule):
    name = "SafetyPolicyRule"
    severity = Severity.CRITICAL

    UNSAFE_PATTERNS = [
        # Violence / weapons
        r"make\s+a\s+bomb",
        r"build\s+a\s+gun",
        r"kill\s+someone",
        r"how\s+to\s+shoot",

        # Illegal activities
        r"hack\s+into",
        r"steal\s+credit\s+card",
        r"bypass\s+security",

        # Self-harm
        r"how\s+to\s+kill\s+myself",
        r"suicide\s+method",
    ]

    def check(self, text: str, context=None) -> RuleResult:
        lowered = text.lower()

        for pattern in self.UNSAFE_PATTERNS:
            if re.search(pattern, lowered):
                return RuleResult(
                    rule_name=self.name,
                    status=RuleStatus.FAIL,
                    severity=self.severity,
                    action=Action.BLOCK,
                    message=f"Unsafe content detected: pattern '{pattern}'",
                    metadata={"matched_pattern": pattern}
                )

        return RuleResult(
            rule_name=self.name,
            status=RuleStatus.PASS,
            severity=Severity.LOW,
            action=Action.ALLOW,
            message="No unsafe content detected"
        )
