from enum import StrEnum


class GetHttpRequestsAggregateBy(StrEnum):
    HOST = "host"
    STATUSCODE = "statusCode"

    def __str__(self) -> str:
        return str(self.value)
