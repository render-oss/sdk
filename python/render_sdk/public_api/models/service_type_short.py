from enum import Enum


class ServiceTypeShort(str, Enum):
    CRON = "cron"
    PSERV = "pserv"
    STATIC = "static"
    WEB = "web"
    WORKER = "worker"

    def __str__(self) -> str:
        return str(self.value)
