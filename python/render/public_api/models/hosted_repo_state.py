from enum import StrEnum


class HostedRepoState(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"

    def __str__(self) -> str:
        return str(self.value)
