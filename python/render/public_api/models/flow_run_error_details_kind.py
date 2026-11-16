from enum import StrEnum


class FlowRunErrorDetailsKind(StrEnum):
    INPUT_HASH = "input_hash"
    TYPE = "type"
    UNKNOWN_TYPE = "unknown_type"

    def __str__(self) -> str:
        return str(self.value)
