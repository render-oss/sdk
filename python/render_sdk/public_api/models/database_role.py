from enum import Enum


class DatabaseRole(str, Enum):
    PRIMARY = "primary"
    REPLICA = "replica"

    def __str__(self) -> str:
        return str(self.value)
