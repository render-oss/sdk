from enum import StrEnum


class WorkflowVersionStatus(StrEnum):
    BUILDING = "building"
    BUILD_FAILED = "build_failed"
    CREATED = "created"
    READY = "ready"
    REGISTERING = "registering"
    REGISTRATION_FAILED = "registration_failed"

    def __str__(self) -> str:
        return str(self.value)
