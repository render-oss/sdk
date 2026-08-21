from enum import Enum


class CronJobRunStatus(str, Enum):
    CANCELED = "canceled"
    PENDING = "pending"
    SUCCESSFUL = "successful"
    UNSUCCESSFUL = "unsuccessful"

    def __str__(self) -> str:
        return str(self.value)
