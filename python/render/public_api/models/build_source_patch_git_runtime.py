from enum import StrEnum


class BuildSourcePATCHGitRuntime(StrEnum):
    DOCKER = "docker"
    ELIXIR = "elixir"
    GO = "go"
    NODE = "node"
    PYTHON = "python"
    RUBY = "ruby"
    RUST = "rust"

    def __str__(self) -> str:
        return str(self.value)
