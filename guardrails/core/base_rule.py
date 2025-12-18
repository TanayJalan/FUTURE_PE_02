from abc import ABC, abstractmethod
from .rule_result import RuleResult
from .enums import Severity

class GuardrailRule(ABC):
    name: str
    severity: Severity

    @abstractmethod
    def check(self, text: str, context: dict | None = None) -> RuleResult:
        pass


class InputRule(GuardrailRule):
    pass


class OutputRule(GuardrailRule):
    pass
