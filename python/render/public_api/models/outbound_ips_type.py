from enum import StrEnum


class OutboundIpsType(StrEnum):
    DEDICATED = "dedicated"
    SHARED = "shared"

    def __str__(self) -> str:
        return str(self.value)
