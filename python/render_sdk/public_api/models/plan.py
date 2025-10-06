from enum import Enum


class Plan(str, Enum):
    CUSTOM = "custom"
    FREE = "free"
    PRO = "pro"
    PRO_MAX = "pro_max"
    PRO_PLUS = "pro_plus"
    PRO_ULTRA = "pro_ultra"
    STANDARD = "standard"
    STANDARD_PLUS = "standard_plus"
    STARTER = "starter"
    STARTER_PLUS = "starter_plus"

    def __str__(self) -> str:
        return str(self.value)
