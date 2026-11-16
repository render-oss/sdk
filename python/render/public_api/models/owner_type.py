from enum import StrEnum


class OwnerType(StrEnum):
    TEAM = "team"
    USER = "user"

    def __str__(self) -> str:
        return str(self.value)
