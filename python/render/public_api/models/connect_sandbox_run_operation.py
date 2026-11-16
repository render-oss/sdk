from enum import StrEnum


class ConnectSandboxRunOperation(StrEnum):
    STREAM = "stream"
    SYNC = "sync"

    def __str__(self) -> str:
        return str(self.value)
