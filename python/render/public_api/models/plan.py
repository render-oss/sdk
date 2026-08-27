from enum import Enum


class Plan(str, Enum):
    CUSTOM = "custom"
    FREE = "free"
    PRO = "pro"
    PRO_LEGACY = "pro_legacy"
    PRO_MAX = "pro_max"
    PRO_PLUS = "pro_plus"
    PRO_PLUS_LEGACY = "pro_plus_legacy"
    PRO_ULTRA = "pro_ultra"
    STANDARD = "standard"
    STANDARD_LEGACY = "standard_legacy"
    STANDARD_PLUS = "standard_plus"
    STANDARD_PLUS_LEGACY = "standard_plus_legacy"
    STARTER = "starter"
    STARTER_LEGACY = "starter_legacy"
    STARTER_PLUS = "starter_plus"
    VALUE_15 = "0.5c-512mb"
    VALUE_16 = "1c-2g"
    VALUE_17 = "2c-4g"
    VALUE_18 = "2c-8g"
    VALUE_19 = "2c-16g"
    VALUE_20 = "4c-8g"
    VALUE_21 = "4c-16g"
    VALUE_22 = "4c-32g"
    VALUE_23 = "8c-16g"
    VALUE_24 = "8c-32g"
    VALUE_25 = "8c-64g"
    VALUE_26 = "12c-24g"
    VALUE_27 = "12c-48g"
    VALUE_28 = "12c-96g"

    def __str__(self) -> str:
        return str(self.value)
