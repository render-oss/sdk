from enum import Enum


class InternalRouting(str, Enum):
    IPONLY = "ipOnly"

    def __str__(self) -> str:
        return str(self.value)
