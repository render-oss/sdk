from enum import Enum


class LogLabelName(str, Enum):
    BLOCKED = "blocked"
    HOST = "host"
    INSTANCE = "instance"
    LEVEL = "level"
    METHOD = "method"
    PATH = "path"
    RESOURCE = "resource"
    STATUSCODE = "statusCode"
    TASK = "task"
    TASKRUN = "taskRun"
    TEXT = "text"
    TYPE = "type"
    WORKFLOWSERVICE = "workflowService"
    WORKFLOWVERESION = "workflowVeresion"

    def __str__(self) -> str:
        return str(self.value)
