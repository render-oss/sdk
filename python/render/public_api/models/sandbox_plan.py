from enum import Enum


class SandboxPlan(str, Enum):
    PRO = "pro"
    STANDARD = "standard"
    STARTER = "starter"
    VALUE_3 = "1c-2g"
    VALUE_4 = "2c-4g"
    VALUE_5 = "4c-8g"
    VALUE_6 = "8c-16g"

    def __str__(self) -> str:
        return str(self.value)
