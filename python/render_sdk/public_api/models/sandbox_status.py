from enum import Enum


class SandboxStatus(str, Enum):
    CREATING = "creating"
    ERRORED = "errored"
    RESUMING = "resuming"
    RUNNING = "running"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"

    def __str__(self) -> str:
        return str(self.value)
