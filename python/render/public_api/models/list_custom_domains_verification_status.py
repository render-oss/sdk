from enum import Enum


class ListCustomDomainsVerificationStatus(str, Enum):
    UNVERIFIED = "unverified"
    VERIFIED = "verified"

    def __str__(self) -> str:
        return str(self.value)
