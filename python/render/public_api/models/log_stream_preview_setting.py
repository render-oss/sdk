from enum import StrEnum


class LogStreamPreviewSetting(StrEnum):
    DROP = "drop"
    SEND = "send"

    def __str__(self) -> str:
        return str(self.value)
