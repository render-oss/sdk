from enum import StrEnum


class BuildSkippedServiceReason(StrEnum):
    DEPLOYS_SHUT_OFF = "deploys_shut_off"
    SUSPENDED = "suspended"

    def __str__(self) -> str:
        return str(self.value)
