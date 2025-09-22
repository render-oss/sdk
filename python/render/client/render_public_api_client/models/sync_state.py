from enum import Enum


class SyncState(str, Enum):
    CREATED = "created"
    ERROR = "error"
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"

    def __str__(self) -> str:
        return str(self.value)
