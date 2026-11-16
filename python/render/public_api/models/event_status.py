from enum import StrEnum


class EventStatus(StrEnum):
    CANCELED = "canceled"
    FAILED = "failed"
    SUCCEEDED = "succeeded"

    def __str__(self) -> str:
        return str(self.value)
