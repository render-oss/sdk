from enum import StrEnum


class DeployMode(StrEnum):
    BUILD_AND_DEPLOY = "build_and_deploy"
    DEPLOY_ONLY = "deploy_only"

    def __str__(self) -> str:
        return str(self.value)
