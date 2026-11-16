from enum import StrEnum


class NotifySettingV2(StrEnum):
    ALL = "all"
    FAILURE = "failure"
    NONE = "none"

    def __str__(self) -> str:
        return str(self.value)
