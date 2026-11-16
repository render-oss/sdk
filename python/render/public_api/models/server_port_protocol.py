from enum import StrEnum


class ServerPortProtocol(StrEnum):
    TCP = "TCP"
    UDP = "UDP"

    def __str__(self) -> str:
        return str(self.value)
