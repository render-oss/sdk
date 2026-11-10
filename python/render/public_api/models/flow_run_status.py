from enum import Enum


class FlowRunStatus(str, Enum):
    CANCELED = "canceled"
    FAILED = "failed"
    PAUSED = "paused"
    PENDING = "pending"
    RUNNING = "running"
    SLEEPING = "sleeping"
    SUCCEEDED = "succeeded"
    SUSPENDED = "suspended"

    def __str__(self) -> str:
        return str(self.value)
