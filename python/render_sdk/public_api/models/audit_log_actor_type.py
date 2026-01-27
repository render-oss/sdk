from enum import Enum


class AuditLogActorType(str, Enum):
    REST_API = "rest_api"
    SYSTEM = "system"
    USER = "user"

    def __str__(self) -> str:
        return str(self.value)
