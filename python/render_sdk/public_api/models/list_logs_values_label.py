from enum import Enum


class ListLogsValuesLabel(str, Enum):
    HOST = "host"
    INSTANCE = "instance"
    LEVEL = "level"
    METHOD = "method"
    STATUSCODE = "statusCode"
    TYPE = "type"

    def __str__(self) -> str:
        return str(self.value)
