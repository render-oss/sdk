from enum import Enum


class BuildClearCache(str, Enum):
    CLEAR = "clear"
    DO_NOT_CLEAR = "do_not_clear"

    def __str__(self) -> str:
        return str(self.value)
