from enum import Enum


class ConnectSandboxRunOperation(str, Enum):
    STREAM = "stream"
    SYNC = "sync"

    def __str__(self) -> str:
        return str(self.value)
