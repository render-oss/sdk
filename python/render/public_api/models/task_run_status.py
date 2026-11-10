from enum import Enum


class TaskRunStatus(str, Enum):
    CANCELED = "canceled"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"
    PENDING = "pending"
    RUNNING = "running"
    SLEEPING = "sleeping"
    SUCCEEDED = "succeeded"
    SUSPENDED = "suspended"

    def __str__(self) -> str:
        return str(self.value)
