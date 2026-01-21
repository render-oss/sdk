from enum import Enum


class TaskOptionsPlan(str, Enum):
    PRO = "pro"
    STANDARD = "standard"
    STARTER = "starter"

    def __str__(self) -> str:
        return str(self.value)
