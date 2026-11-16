from enum import StrEnum


class ListCustomDomainsVerificationStatus(StrEnum):
    UNVERIFIED = "unverified"
    VERIFIED = "verified"

    def __str__(self) -> str:
        return str(self.value)
