from enum import Enum


class NotifySetting(str, Enum):
    DEFAULT = "default"
    IGNORE = "ignore"
    NOTIFY = "notify"

    def __str__(self) -> str:
        return str(self.value)
