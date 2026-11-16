from enum import StrEnum


class DedicatedIPStatus(StrEnum):
    CREATING = "CREATING"
    DELETED = "DELETED"
    DELETING = "DELETING"
    FAILED = "FAILED"
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    UNKNOWN = "UNKNOWN"

    def __str__(self) -> str:
        return str(self.value)
