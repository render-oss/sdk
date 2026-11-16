from enum import StrEnum


class LogDirection(StrEnum):
    BACKWARD = "backward"
    FORWARD = "forward"

    def __str__(self) -> str:
        return str(self.value)
