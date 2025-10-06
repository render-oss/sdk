from enum import Enum


class RenderSubdomainPolicy(str, Enum):
    DISABLED = "disabled"
    ENABLED = "enabled"

    def __str__(self) -> str:
        return str(self.value)
