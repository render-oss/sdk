from enum import Enum


class ProtectedStatus(str, Enum):
    PROTECTED = "protected"
    UNPROTECTED = "unprotected"

    def __str__(self) -> str:
        return str(self.value)
