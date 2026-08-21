from enum import Enum


class Status(str, Enum):
    CREATED = "created"
    ERROR = "error"
    IN_SYNC = "in_sync"
    PAUSED = "paused"
    SYNCING = "syncing"

    def __str__(self) -> str:
        return str(self.value)
