from enum import StrEnum


class CustomDomainVerificationStatus(StrEnum):
    UNVERIFIED = "unverified"
    VERIFIED = "verified"

    def __str__(self) -> str:
        return str(self.value)
