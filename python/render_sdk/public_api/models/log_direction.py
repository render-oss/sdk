from enum import Enum


class LogDirection(str, Enum):
    BACKWARD = "backward"
    FORWARD = "forward"

    def __str__(self) -> str:
        return str(self.value)
