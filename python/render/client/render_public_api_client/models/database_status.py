from enum import Enum


class DatabaseStatus(str, Enum):
    AVAILABLE = "available"
    CONFIG_RESTART = "config_restart"
    CREATING = "creating"
    MAINTENANCE_IN_PROGRESS = "maintenance_in_progress"
    MAINTENANCE_SCHEDULED = "maintenance_scheduled"
    RECOVERY_FAILED = "recovery_failed"
    RECOVERY_IN_PROGRESS = "recovery_in_progress"
    SUSPENDED = "suspended"
    UNAVAILABLE = "unavailable"
    UNKNOWN = "unknown"
    UPDATING_INSTANCE = "updating_instance"

    def __str__(self) -> str:
        return str(self.value)
