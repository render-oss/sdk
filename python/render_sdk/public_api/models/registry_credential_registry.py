from enum import Enum


class RegistryCredentialRegistry(str, Enum):
    AWS_ECR = "AWS_ECR"
    DOCKER = "DOCKER"
    GITHUB = "GITHUB"
    GITLAB = "GITLAB"
    GOOGLE_ARTIFACT = "GOOGLE_ARTIFACT"

    def __str__(self) -> str:
        return str(self.value)
