from enum import StrEnum


class SandboxEgressRuleProtocol(StrEnum):
    HTTPS = "https"

    def __str__(self) -> str:
        return str(self.value)
