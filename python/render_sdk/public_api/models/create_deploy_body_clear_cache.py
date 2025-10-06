from enum import Enum


class CreateDeployBodyClearCache(str, Enum):
    CLEAR = "clear"
    DO_NOT_CLEAR = "do_not_clear"

    def __str__(self) -> str:
        return str(self.value)
