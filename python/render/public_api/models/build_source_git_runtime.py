from enum import Enum


class BuildSourceGitRuntime(str, Enum):
    DOCKER = "docker"
    ELIXIR = "elixir"
    GO = "go"
    NODE = "node"
    PYTHON = "python"
    RUBY = "ruby"
    RUST = "rust"

    def __str__(self) -> str:
        return str(self.value)
