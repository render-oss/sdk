from enum import Enum


class KeyValuePlan(str, Enum):
    CUSTOM = "custom"
    FREE = "free"
    PRO = "pro"
    PRO_PLUS = "pro_plus"
    STANDARD = "standard"
    STARTER = "starter"
    VALUE_10 = "20g"
    VALUE_11 = "40g"
    VALUE_6 = "256mb"
    VALUE_7 = "1g"
    VALUE_8 = "5g"
    VALUE_9 = "10g"

    def __str__(self) -> str:
        return str(self.value)
