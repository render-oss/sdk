from enum import StrEnum


class AuditLogActorType(StrEnum):
    REST_API = "rest_api"
    SYSTEM = "system"
    USER = "user"

    def __str__(self) -> str:
        return str(self.value)
