from enum import StrEnum


class PullRequestPreviewsEnabled(StrEnum):
    NO = "no"
    YES = "yes"

    def __str__(self) -> str:
        return str(self.value)
