from enum import StrEnum


class StreamTaskRunsEventsAccept(StrEnum):
    TEXTEVENT_STREAM = "text/event-stream"

    def __str__(self) -> str:
        return str(self.value)
