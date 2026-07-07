from enum import Enum


class ExecSandboxSyncAccept(str, Enum):
    APPLICATIONJSON = "application/json"
    TEXTEVENT_STREAM = "text/event-stream"

    def __str__(self) -> str:
        return str(self.value)
