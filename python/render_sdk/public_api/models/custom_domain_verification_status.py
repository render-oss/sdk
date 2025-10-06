from enum import Enum


class CustomDomainVerificationStatus(str, Enum):
    UNVERIFIED = "unverified"
    VERIFIED = "verified"

    def __str__(self) -> str:
        return str(self.value)
