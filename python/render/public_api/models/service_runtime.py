from enum import StrEnum


class ServiceRuntime(StrEnum):
    DOCKER = "docker"
    ELIXIR = "elixir"
    GO = "go"
    IMAGE = "image"
    NODE = "node"
    PYTHON = "python"
    RUBY = "ruby"
    RUST = "rust"

    def __str__(self) -> str:
        return str(self.value)
