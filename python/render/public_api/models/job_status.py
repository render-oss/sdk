from enum import StrEnum


class JobStatus(StrEnum):
    CANCELED = "canceled"
    FAILED = "failed"
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"

    def __str__(self) -> str:
        return str(self.value)
