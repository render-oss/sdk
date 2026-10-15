from enum import Enum


class FlowRunStepStatus(str, Enum):
    FAILED = "failed"
    RUNNING = "running"
    SUCCEEDED = "succeeded"

    def __str__(self) -> str:
        return str(self.value)
