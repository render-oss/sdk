from enum import StrEnum


class BuildDeployServiceScope(StrEnum):
    AUTODEPLOY_ONLY = "autodeploy_only"
    CUSTOM = "custom"
    NONE = "none"

    def __str__(self) -> str:
        return str(self.value)
