from enum import Enum


class ListCustomDomainsDomainType(str, Enum):
    APEX = "apex"
    SUBDOMAIN = "subdomain"

    def __str__(self) -> str:
        return str(self.value)
