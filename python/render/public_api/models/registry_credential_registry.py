from enum import StrEnum


class RegistryCredentialRegistry(StrEnum):
    AWS_ECR = "AWS_ECR"
    DOCKER = "DOCKER"
    GITHUB = "GITHUB"
    GITLAB = "GITLAB"
    GOOGLE_ARTIFACT = "GOOGLE_ARTIFACT"

    def __str__(self) -> str:
        return str(self.value)
