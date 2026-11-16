from enum import StrEnum


class TeamMemberRole(StrEnum):
    ADMIN = "ADMIN"
    DEVELOPER = "DEVELOPER"
    WORKSPACE_BILLING = "WORKSPACE_BILLING"
    WORKSPACE_CONTRIBUTOR = "WORKSPACE_CONTRIBUTOR"
    WORKSPACE_VIEWER = "WORKSPACE_VIEWER"

    def __str__(self) -> str:
        return str(self.value)
