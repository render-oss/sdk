from enum import Enum


class ServerPortProtocol(str, Enum):
    TCP = "TCP"
    UDP = "UDP"

    def __str__(self) -> str:
        return str(self.value)
