from enum import StrEnum


class BuildRunStatus(StrEnum):
    CANCELED = "canceled"
    CREATED = "created"
    FAILED = "failed"
    INPROGRESS = "inProgress"
    SUCCEEDED = "succeeded"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
