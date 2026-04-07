from enum import Enum


class CreateSandboxAccept(str, Enum):
    TEXTEVENT_STREAM = "text/event-stream"

    def __str__(self) -> str:
        return str(self.value)
