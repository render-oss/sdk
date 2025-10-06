from enum import Enum


class StreamTaskRunsEventsAccept(str, Enum):
    TEXTEVENT_STREAM = "text/event-stream"

    def __str__(self) -> str:
        return str(self.value)
