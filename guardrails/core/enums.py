from enum import Enum

class RuleStatus(Enum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"


class Severity(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Action(Enum):
    ALLOW = "ALLOW"
    WARN = "WARN"
    REWRITE = "REWRITE"
    BLOCK = "BLOCK"
