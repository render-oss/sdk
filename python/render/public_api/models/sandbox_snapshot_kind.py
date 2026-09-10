from enum import Enum


class SandboxSnapshotKind(str, Enum):
    FILESYSTEM = "filesystem"
    RUNTIME = "runtime"

    def __str__(self) -> str:
        return str(self.value)
