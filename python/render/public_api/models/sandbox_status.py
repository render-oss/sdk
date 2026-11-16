from enum import StrEnum


class SandboxStatus(StrEnum):
    CREATING = "creating"
    ERRORED = "errored"
    RESUMING = "resuming"
    RUNNING = "running"
    SUSPENDED = "suspended"
    SUSPENDING = "suspending"
    TERMINATED = "terminated"

    def __str__(self) -> str:
        return str(self.value)
