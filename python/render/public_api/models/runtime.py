from enum import StrEnum


class Runtime(StrEnum):
    ELIXIR = "elixir"
    GO = "go"
    NODE = "node"
    PYTHON = "python"
    RUBY = "ruby"

    def __str__(self) -> str:
        return str(self.value)
