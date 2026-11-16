from enum import StrEnum


class SandboxCredentialInjectionType(StrEnum):
    BASIC = "basic"
    COOKIE = "cookie"
    HEADER = "header"
    QUERY = "query"

    def __str__(self) -> str:
        return str(self.value)
