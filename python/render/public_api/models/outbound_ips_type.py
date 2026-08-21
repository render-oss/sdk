from enum import Enum


class OutboundIpsType(str, Enum):
    DEDICATED = "dedicated"
    SHARED = "shared"

    def __str__(self) -> str:
        return str(self.value)
