from enum import Enum


class PreviewsGeneration(str, Enum):
    AUTOMATIC = "automatic"
    MANUAL = "manual"
    OFF = "off"

    def __str__(self) -> str:
        return str(self.value)
