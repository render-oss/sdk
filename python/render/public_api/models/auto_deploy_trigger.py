from enum import StrEnum


class AutoDeployTrigger(StrEnum):
    CHECKSPASS = "checksPass"
    COMMIT = "commit"
    OFF = "off"

    def __str__(self) -> str:
        return str(self.value)
