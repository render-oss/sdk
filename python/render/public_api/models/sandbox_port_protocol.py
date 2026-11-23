from enum import StrEnum


class SandboxPortProtocol(StrEnum):
    TCP = "tcp"

    def __str__(self) -> str:
        return str(self.value)
