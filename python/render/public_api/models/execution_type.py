from enum import StrEnum


class ExecutionType(StrEnum):
    FILES = "files"
    RUNS = "runs"

    def __str__(self) -> str:
        return str(self.value)
