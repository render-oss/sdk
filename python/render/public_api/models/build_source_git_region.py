from enum import StrEnum


class BuildSourceGitRegion(StrEnum):
    FRANKFURT = "frankfurt"
    OHIO = "ohio"
    OREGON = "oregon"
    SINGAPORE = "singapore"
    VIRGINIA = "virginia"

    def __str__(self) -> str:
        return str(self.value)
