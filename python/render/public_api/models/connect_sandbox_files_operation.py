from enum import StrEnum


class ConnectSandboxFilesOperation(StrEnum):
    DOWNLOAD = "download"
    UPLOAD = "upload"

    def __str__(self) -> str:
        return str(self.value)
