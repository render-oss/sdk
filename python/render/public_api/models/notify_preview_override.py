from enum import StrEnum


class NotifyPreviewOverride(StrEnum):
    DEFAULT = "default"
    FALSE = "false"
    TRUE = "true"

    def __str__(self) -> str:
        return str(self.value)
