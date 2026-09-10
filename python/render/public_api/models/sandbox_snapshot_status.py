from enum import Enum


class SandboxSnapshotStatus(str, Enum):
    AVAILABLE = "available"
    CREATING = "creating"
    FAILED = "failed"

    def __str__(self) -> str:
        return str(self.value)
