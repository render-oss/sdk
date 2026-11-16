from enum import StrEnum


class SandboxSnapshotStatus(StrEnum):
    AVAILABLE = "available"
    CREATING = "creating"
    FAILED = "failed"

    def __str__(self) -> str:
        return str(self.value)
