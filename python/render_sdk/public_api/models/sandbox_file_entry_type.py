from enum import Enum


class SandboxFileEntryType(str, Enum):
    DIRECTORY = "directory"
    FILE = "file"
    SYMLINK = "symlink"

    def __str__(self) -> str:
        return str(self.value)
