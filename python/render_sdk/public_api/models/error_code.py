from enum import Enum


class ErrorCode(str, Enum):
    DUPLICATE_SAVED_SEARCH_NAME = "duplicate_saved_search_name"
    MULTIPLE_REGIONS = "multiple_regions"
    TOO_MANY_RESOURCES = "too_many_resources"

    def __str__(self) -> str:
        return str(self.value)
