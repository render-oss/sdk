from enum import StrEnum


class DatabaseRole(StrEnum):
    PRIMARY = "primary"
    REPLICA = "replica"

    def __str__(self) -> str:
        return str(self.value)
