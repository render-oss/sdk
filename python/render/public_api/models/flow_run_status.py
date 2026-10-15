from enum import Enum


class FlowRunStatus(str, Enum):
    CANCELED = "canceled"
    FAILED = "failed"
    PAUSED = "paused"
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"

    def __str__(self) -> str:
        return str(self.value)
