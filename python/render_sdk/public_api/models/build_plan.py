from enum import Enum


class BuildPlan(str, Enum):
    PERFORMANCE = "performance"
    STARTER = "starter"

    def __str__(self) -> str:
        return str(self.value)
