from enum import StrEnum


class GetTaskRunsCompletedState(StrEnum):
    FAILED = "failed"
    SUCCEEDED = "succeeded"

    def __str__(self) -> str:
        return str(self.value)
