from enum import Enum


class ServiceType(str, Enum):
    BACKGROUND_WORKER = "background_worker"
    CRON_JOB = "cron_job"
    PRIVATE_SERVICE = "private_service"
    STATIC_SITE = "static_site"
    WEB_SERVICE = "web_service"

    def __str__(self) -> str:
        return str(self.value)
