from enum import StrEnum


class FlowRunStepStatus(StrEnum):
    FAILED = "failed"
    RUNNING = "running"
    SUCCEEDED = "succeeded"

    def __str__(self) -> str:
        return str(self.value)
