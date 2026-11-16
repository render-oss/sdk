from enum import StrEnum


class CustomDomainDomainType(StrEnum):
    APEX = "apex"
    SUBDOMAIN = "subdomain"

    def __str__(self) -> str:
        return str(self.value)
