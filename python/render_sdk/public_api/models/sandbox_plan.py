from enum import Enum


class SandboxPlan(str, Enum):
    PRO = "pro"
    STANDARD = "standard"
    STARTER = "starter"

    def __str__(self) -> str:
        return str(self.value)
