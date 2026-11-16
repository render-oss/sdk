from enum import StrEnum


class ListLogsValuesLabel(StrEnum):
    HOST = "host"
    INSTANCE = "instance"
    LEVEL = "level"
    METHOD = "method"
    STATUSCODE = "statusCode"
    TYPE = "type"

    def __str__(self) -> str:
        return str(self.value)
