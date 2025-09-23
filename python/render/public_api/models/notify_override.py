from enum import Enum


class NotifyOverride(str, Enum):
    ALL = "all"
    DEFAULT = "default"
    FAILURE = "failure"
    NONE = "none"

    def __str__(self) -> str:
        return str(self.value)
