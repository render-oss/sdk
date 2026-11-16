from enum import StrEnum


class CronJobRunStatus(StrEnum):
    CANCELED = "canceled"
    PENDING = "pending"
    SUCCESSFUL = "successful"
    UNSUCCESSFUL = "unsuccessful"

    def __str__(self) -> str:
        return str(self.value)
