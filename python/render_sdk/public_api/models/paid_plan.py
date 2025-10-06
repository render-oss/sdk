from enum import Enum


class PaidPlan(str, Enum):
    PRO = "pro"
    PRO_MAX = "pro_max"
    PRO_PLUS = "pro_plus"
    PRO_ULTRA = "pro_ultra"
    STANDARD = "standard"
    STARTER = "starter"

    def __str__(self) -> str:
        return str(self.value)
