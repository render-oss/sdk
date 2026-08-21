from enum import Enum


class ExecutionType(str, Enum):
    FILES = "files"
    RUNS = "runs"

    def __str__(self) -> str:
        return str(self.value)
