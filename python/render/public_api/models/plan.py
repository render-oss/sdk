from enum import Enum


class Plan(str, Enum):
    CUSTOM = "custom"
    FREE = "free"
    PRO = "pro"
    PRO_LEGACY = "pro_legacy"
    PRO_MAX = "pro_max"
    PRO_PLUS = "pro_plus"
    PRO_PLUS_LEGACY = "pro_plus_legacy"
    PRO_ULTRA = "pro_ultra"
    STANDARD = "standard"
    STANDARD_LEGACY = "standard_legacy"
    STANDARD_PLUS = "standard_plus"
    STANDARD_PLUS_LEGACY = "standard_plus_legacy"
    STARTER = "starter"
    STARTER_LEGACY = "starter_legacy"
    STARTER_PLUS = "starter_plus"

    def __str__(self) -> str:
        return str(self.value)
