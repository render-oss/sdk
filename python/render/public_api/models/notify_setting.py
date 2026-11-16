from enum import StrEnum


class NotifySetting(StrEnum):
    DEFAULT = "default"
    IGNORE = "ignore"
    NOTIFY = "notify"

    def __str__(self) -> str:
        return str(self.value)
