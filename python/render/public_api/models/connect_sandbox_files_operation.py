from enum import Enum


class ConnectSandboxFilesOperation(str, Enum):
    DOWNLOAD = "download"
    UPLOAD = "upload"

    def __str__(self) -> str:
        return str(self.value)
