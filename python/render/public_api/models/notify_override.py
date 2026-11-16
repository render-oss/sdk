from enum import StrEnum


class NotifyOverride(StrEnum):
    ALL = "all"
    DEFAULT = "default"
    FAILURE = "failure"
    NONE = "none"

    def __str__(self) -> str:
        return str(self.value)
