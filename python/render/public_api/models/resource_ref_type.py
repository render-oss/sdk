from enum import Enum


class ResourceRefType(str, Enum):
    BACKGROUND_WORKER = "background_worker"
    BUILD_SOURCE = "build_source"
    CRON_JOB = "cron_job"
    ENVIRONMENT_GROUP = "environment_group"
    KEY_VALUE = "key_value"
    POSTGRES = "postgres"
    PRIVATE_SERVICE = "private_service"
    REDIS = "redis"
    STATIC_SITE = "static_site"
    WEB_SERVICE = "web_service"
    WORKFLOW = "workflow"

    def __str__(self) -> str:
        return str(self.value)
