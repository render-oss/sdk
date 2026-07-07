from enum import Enum


class SandboxNetworkPolicyDefault(str, Enum):
    ALLOW_ALL = "allow-all"
    DENY_ALL = "deny-all"

    def __str__(self) -> str:
        return str(self.value)
