from enum import Enum


class PaidPlan(str, Enum):
    PRO = "pro"
    PRO_MAX = "pro_max"
    PRO_PLUS = "pro_plus"
    PRO_ULTRA = "pro_ultra"
    STANDARD = "standard"
    STARTER = "starter"
    VALUE_10 = "2c-16g"
    VALUE_11 = "4c-8g"
    VALUE_12 = "4c-16g"
    VALUE_13 = "4c-32g"
    VALUE_14 = "8c-16g"
    VALUE_15 = "8c-32g"
    VALUE_16 = "8c-64g"
    VALUE_17 = "12c-24g"
    VALUE_18 = "12c-48g"
    VALUE_19 = "12c-96g"
    VALUE_6 = "0.5c-512mb"
    VALUE_7 = "1c-2g"
    VALUE_8 = "2c-4g"
    VALUE_9 = "2c-8g"

    def __str__(self) -> str:
        return str(self.value)
