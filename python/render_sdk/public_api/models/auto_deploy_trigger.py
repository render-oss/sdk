from enum import Enum


class AutoDeployTrigger(str, Enum):
    CHECKSPASS = "checksPass"
    COMMIT = "commit"
    OFF = "off"

    def __str__(self) -> str:
        return str(self.value)
