from enum import StrEnum


class ServiceTypeShort(StrEnum):
    CRON = "cron"
    PSERV = "pserv"
    STATIC = "static"
    WEB = "web"
    WORKER = "worker"

    def __str__(self) -> str:
        return str(self.value)
