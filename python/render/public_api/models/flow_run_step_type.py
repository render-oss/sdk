from enum import Enum


class FlowRunStepType(str, Enum):
    DETACHED = "detached"
    INLINE = "inline"
    SLEEP = "sleep"

    def __str__(self) -> str:
        return str(self.value)
