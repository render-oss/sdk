from enum import StrEnum


class BuildSourcePATCHGitRegion(StrEnum):
    FRANKFURT = "frankfurt"
    OHIO = "ohio"
    OREGON = "oregon"
    SINGAPORE = "singapore"
    VIRGINIA = "virginia"

    def __str__(self) -> str:
        return str(self.value)
