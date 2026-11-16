from enum import StrEnum


class ListPostgresSuspendedItem(StrEnum):
    NOT_SUSPENDED = "not_suspended"
    SUSPENDED = "suspended"

    def __str__(self) -> str:
        return str(self.value)
