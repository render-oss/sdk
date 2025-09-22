from enum import Enum


class FilterHTTPValuesCollectionItemFilter(str, Enum):
    HOST = "host"
    STATUSCODE = "statusCode"

    def __str__(self) -> str:
        return str(self.value)
