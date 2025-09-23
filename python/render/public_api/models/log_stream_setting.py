from enum import Enum


class LogStreamSetting(str, Enum):
    DROP = "drop"
    SEND = "send"

    def __str__(self) -> str:
        return str(self.value)
