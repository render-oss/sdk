from enum import Enum


class PullRequestPreviewsEnabled(str, Enum):
    NO = "no"
    YES = "yes"

    def __str__(self) -> str:
        return str(self.value)
