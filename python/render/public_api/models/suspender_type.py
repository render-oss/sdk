from enum import StrEnum


class SuspenderType(StrEnum):
    ADMIN = "admin"
    BILLING = "billing"
    HIPAA_ENABLEMENT = "hipaa_enablement"
    PARENT_SERVICE = "parent_service"
    STUCK_CRASHLOOPING = "stuck_crashlooping"
    UNKNOWN = "unknown"
    USER = "user"

    def __str__(self) -> str:
        return str(self.value)
