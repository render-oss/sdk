from enum import StrEnum


class FlowRunStepType(StrEnum):
    DETACHED = "detached"
    INLINE = "inline"
    SLEEP = "sleep"

    def __str__(self) -> str:
        return str(self.value)
