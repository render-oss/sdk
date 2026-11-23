from enum import StrEnum


class SandboxPortLimitErrorCode(StrEnum):
    PORT_LIMIT_EXCEEDED = "port_limit_exceeded"

    def __str__(self) -> str:
        return str(self.value)
