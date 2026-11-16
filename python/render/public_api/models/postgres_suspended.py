from enum import StrEnum


class PostgresSuspended(StrEnum):
    NOT_SUSPENDED = "not_suspended"
    SUSPENDED = "suspended"

    def __str__(self) -> str:
        return str(self.value)
