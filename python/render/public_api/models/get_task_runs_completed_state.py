from enum import Enum


class GetTaskRunsCompletedState(str, Enum):
    FAILED = "failed"
    SUCCEEDED = "succeeded"

    def __str__(self) -> str:
        return str(self.value)
