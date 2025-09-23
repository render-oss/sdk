from enum import Enum


class GetHttpRequestsAggregateBy(str, Enum):
    HOST = "host"
    STATUSCODE = "statusCode"

    def __str__(self) -> str:
        return str(self.value)
