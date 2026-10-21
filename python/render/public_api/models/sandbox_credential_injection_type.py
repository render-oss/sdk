from enum import Enum


class SandboxCredentialInjectionType(str, Enum):
    BASIC = "basic"
    COOKIE = "cookie"
    HEADER = "header"
    QUERY = "query"

    def __str__(self) -> str:
        return str(self.value)
