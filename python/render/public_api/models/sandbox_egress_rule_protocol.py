from enum import Enum


class SandboxEgressRuleProtocol(str, Enum):
    HTTPS = "https"

    def __str__(self) -> str:
        return str(self.value)
