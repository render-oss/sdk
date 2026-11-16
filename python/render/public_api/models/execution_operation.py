from enum import StrEnum


class ExecutionOperation(StrEnum):
    DOWNLOAD = "download"
    STREAM = "stream"
    SYNC = "sync"
    UPLOAD = "upload"

    def __str__(self) -> str:
        return str(self.value)
