from enum import StrEnum


class GetCpuAggregationMethod(StrEnum):
    AVG = "AVG"
    MAX = "MAX"
    MIN = "MIN"

    def __str__(self) -> str:
        return str(self.value)
