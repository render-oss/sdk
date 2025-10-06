from enum import Enum


class NotifySettingV2(str, Enum):
    ALL = "all"
    FAILURE = "failure"
    NONE = "none"

    def __str__(self) -> str:
        return str(self.value)
