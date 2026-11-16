from enum import StrEnum


class BuildPlan(StrEnum):
    PERFORMANCE = "performance"
    STARTER = "starter"

    def __str__(self) -> str:
        return str(self.value)
