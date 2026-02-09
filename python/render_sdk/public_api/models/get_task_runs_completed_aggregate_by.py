from enum import Enum


class GetTaskRunsCompletedAggregateBy(str, Enum):
    STATE = "state"

    def __str__(self) -> str:
        return str(self.value)
