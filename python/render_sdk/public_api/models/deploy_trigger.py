from enum import Enum


class DeployTrigger(str, Enum):
    API = "api"
    BLUEPRINT_SYNC = "blueprint_sync"
    DEPLOYED_BY_RENDER = "deployed_by_render"
    DEPLOY_HOOK = "deploy_hook"
    MANUAL = "manual"
    NEW_COMMIT = "new_commit"
    OTHER = "other"
    ROLLBACK = "rollback"
    SERVICE_RESUMED = "service_resumed"
    SERVICE_UPDATED = "service_updated"

    def __str__(self) -> str:
        return str(self.value)
