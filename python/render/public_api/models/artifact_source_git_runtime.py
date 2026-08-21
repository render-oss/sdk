from enum import Enum


class ArtifactSourceGitRuntime(str, Enum):
    DOCKER = "docker"
    ELIXIR = "elixir"
    GO = "go"
    NODE = "node"
    PYTHON = "python"
    RUBY = "ruby"
    RUST = "rust"

    def __str__(self) -> str:
        return str(self.value)
