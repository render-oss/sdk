from enum import Enum


class EventStatus(str, Enum):
    CANCELED = "canceled"
    FAILED = "failed"
    SUCCEEDED = "succeeded"

    def __str__(self) -> str:
        return str(self.value)
