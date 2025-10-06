from enum import Enum


class FilterApplicationValuesCollectionItemFilter(str, Enum):
    INSTANCE = "instance"

    def __str__(self) -> str:
        return str(self.value)
