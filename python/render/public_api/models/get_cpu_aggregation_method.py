from enum import Enum


class GetCpuAggregationMethod(str, Enum):
    AVG = "AVG"
    MAX = "MAX"
    MIN = "MIN"

    def __str__(self) -> str:
        return str(self.value)
