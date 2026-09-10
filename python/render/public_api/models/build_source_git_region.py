from enum import Enum


class BuildSourceGitRegion(str, Enum):
    FRANKFURT = "frankfurt"
    OHIO = "ohio"
    OREGON = "oregon"
    SINGAPORE = "singapore"
    VIRGINIA = "virginia"

    def __str__(self) -> str:
        return str(self.value)
