from enum import StrEnum


class FilterApplicationValuesCollectionItemFilter(StrEnum):
    INSTANCE = "instance"

    def __str__(self) -> str:
        return str(self.value)
