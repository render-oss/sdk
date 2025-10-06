from enum import Enum


class DeployStatus(str, Enum):
    BUILD_FAILED = "build_failed"
    BUILD_IN_PROGRESS = "build_in_progress"
    CANCELED = "canceled"
    CREATED = "created"
    DEACTIVATED = "deactivated"
    LIVE = "live"
    PRE_DEPLOY_FAILED = "pre_deploy_failed"
    PRE_DEPLOY_IN_PROGRESS = "pre_deploy_in_progress"
    QUEUED = "queued"
    UPDATE_FAILED = "update_failed"
    UPDATE_IN_PROGRESS = "update_in_progress"

    def __str__(self) -> str:
        return str(self.value)
