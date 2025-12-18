from dataclasses import dataclass
from typing import Optional
from .enums import RuleStatus, Severity, Action

@dataclass
class RuleResult:
    rule_name: str
    status: RuleStatus
    severity: Severity
    action: Action
    message: str
    metadata: Optional[dict] = None
