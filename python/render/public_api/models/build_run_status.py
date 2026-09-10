from enum import Enum


class BuildRunStatus(str, Enum):
    CANCELED = "canceled"
    CREATED = "created"
    FAILED = "failed"
    INPROGRESS = "inProgress"
    SUCCEEDED = "succeeded"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
