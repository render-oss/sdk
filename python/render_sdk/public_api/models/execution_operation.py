from enum import Enum


class ExecutionOperation(str, Enum):
    DOWNLOAD = "download"
    STREAM = "stream"
    SYNC = "sync"
    UPLOAD = "upload"

    def __str__(self) -> str:
        return str(self.value)
