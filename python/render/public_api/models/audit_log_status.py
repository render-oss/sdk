from enum import StrEnum


class AuditLogStatus(StrEnum):
    ERROR = "error"
    SUCCESS = "success"

    def __str__(self) -> str:
        return str(self.value)
