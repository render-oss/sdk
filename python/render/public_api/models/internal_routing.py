from enum import StrEnum


class InternalRouting(StrEnum):
    IPONLY = "ipOnly"

    def __str__(self) -> str:
        return str(self.value)
