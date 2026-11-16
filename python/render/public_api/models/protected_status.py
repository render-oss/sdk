from enum import StrEnum


class ProtectedStatus(StrEnum):
    PROTECTED = "protected"
    UNPROTECTED = "unprotected"

    def __str__(self) -> str:
        return str(self.value)
