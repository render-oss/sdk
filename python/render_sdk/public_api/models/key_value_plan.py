from enum import Enum


class KeyValuePlan(str, Enum):
    CUSTOM = "custom"
    FREE = "free"
    PRO = "pro"
    PRO_PLUS = "pro_plus"
    STANDARD = "standard"
    STARTER = "starter"

    def __str__(self) -> str:
        return str(self.value)
