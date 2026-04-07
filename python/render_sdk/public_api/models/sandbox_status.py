from enum import Enum


class SandboxStatus(str, Enum):
    CREATING = "creating"
    ERRORED = "errored"
    RUNNING = "running"
    TERMINATED = "terminated"

    def __str__(self) -> str:
        return str(self.value)
