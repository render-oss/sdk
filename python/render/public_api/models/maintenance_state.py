from enum import StrEnum


class MaintenanceState(StrEnum):
    CANCELLED = "cancelled"
    FAILED = "failed"
    IN_PROGRESS = "in_progress"
    SCHEDULED = "scheduled"
    SUCCEEDED = "succeeded"
    USER_FIX_REQUIRED = "user_fix_required"

    def __str__(self) -> str:
        return str(self.value)
