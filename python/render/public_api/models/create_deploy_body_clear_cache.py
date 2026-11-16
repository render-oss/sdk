from enum import StrEnum


class CreateDeployBodyClearCache(StrEnum):
    CLEAR = "clear"
    DO_NOT_CLEAR = "do_not_clear"

    def __str__(self) -> str:
        return str(self.value)
