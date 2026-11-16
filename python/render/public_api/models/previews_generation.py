from enum import StrEnum


class PreviewsGeneration(StrEnum):
    AUTOMATIC = "automatic"
    MANUAL = "manual"
    OFF = "off"

    def __str__(self) -> str:
        return str(self.value)
