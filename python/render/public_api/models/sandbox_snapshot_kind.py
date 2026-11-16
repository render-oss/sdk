from enum import StrEnum


class SandboxSnapshotKind(StrEnum):
    FILESYSTEM = "filesystem"
    RUNTIME = "runtime"

    def __str__(self) -> str:
        return str(self.value)
