from enum import Enum


class SandboxPOSTPlan(str, Enum):
    VALUE_0 = "1-2gb"
    VALUE_1 = "2-4gb"
    VALUE_2 = "4-8gb"

    def __str__(self) -> str:
        return str(self.value)
