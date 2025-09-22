from enum import Enum


class PostgresVersion(str, Enum):
    VALUE_0 = "11"
    VALUE_1 = "12"
    VALUE_2 = "13"
    VALUE_3 = "14"
    VALUE_4 = "15"
    VALUE_5 = "16"
    VALUE_6 = "17"

    def __str__(self) -> str:
        return str(self.value)
