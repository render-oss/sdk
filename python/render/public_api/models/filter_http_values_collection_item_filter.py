from enum import StrEnum


class FilterHTTPValuesCollectionItemFilter(StrEnum):
    HOST = "host"
    STATUSCODE = "statusCode"

    def __str__(self) -> str:
        return str(self.value)
