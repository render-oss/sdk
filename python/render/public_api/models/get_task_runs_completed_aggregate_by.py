from enum import StrEnum


class GetTaskRunsCompletedAggregateBy(StrEnum):
    STATE = "state"

    def __str__(self) -> str:
        return str(self.value)
