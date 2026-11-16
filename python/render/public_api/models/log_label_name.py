from enum import StrEnum


class LogLabelName(StrEnum):
    BLOCKED = "blocked"
    BUILD = "build"
    HOST = "host"
    INSTANCE = "instance"
    LEVEL = "level"
    METHOD = "method"
    PATH = "path"
    RESOURCE = "resource"
    SANDBOX = "sandbox"
    STATUSCODE = "statusCode"
    TASK = "task"
    TASKRUN = "taskRun"
    TEXT = "text"
    TYPE = "type"
    WORKFLOWSERVICE = "workflowService"
    WORKFLOWVERESION = "workflowVeresion"

    def __str__(self) -> str:
        return str(self.value)
