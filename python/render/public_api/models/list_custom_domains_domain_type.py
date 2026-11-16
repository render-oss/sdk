from enum import StrEnum


class ListCustomDomainsDomainType(StrEnum):
    APEX = "apex"
    SUBDOMAIN = "subdomain"

    def __str__(self) -> str:
        return str(self.value)
