from enum import Enum


class SuspenderType(str, Enum):
    ADMIN = "admin"
    BILLING = "billing"
    HIPAA_ENABLEMENT = "hipaa_enablement"
    PARENT_SERVICE = "parent_service"
    STUCK_CRASHLOOPING = "stuck_crashlooping"
    UNKNOWN = "unknown"
    USER = "user"

    def __str__(self) -> str:
        return str(self.value)
