from enum import Enum


class PostgresPlans(str, Enum):
    ACCELERATED_1024GB = "accelerated_1024gb"
    ACCELERATED_128GB = "accelerated_128gb"
    ACCELERATED_16GB = "accelerated_16gb"
    ACCELERATED_256GB = "accelerated_256gb"
    ACCELERATED_32GB = "accelerated_32gb"
    ACCELERATED_384GB = "accelerated_384gb"
    ACCELERATED_512GB = "accelerated_512gb"
    ACCELERATED_64GB = "accelerated_64gb"
    ACCELERATED_768GB = "accelerated_768gb"
    BASIC_1GB = "basic_1gb"
    BASIC_256MB = "basic_256mb"
    BASIC_4GB = "basic_4gb"
    CUSTOM = "custom"
    FREE = "free"
    PRO = "pro"
    PRO_128GB = "pro_128gb"
    PRO_16GB = "pro_16gb"
    PRO_192GB = "pro_192gb"
    PRO_256GB = "pro_256gb"
    PRO_32GB = "pro_32gb"
    PRO_384GB = "pro_384gb"
    PRO_4GB = "pro_4gb"
    PRO_512GB = "pro_512gb"
    PRO_64GB = "pro_64gb"
    PRO_8GB = "pro_8gb"
    PRO_PLUS = "pro_plus"
    STANDARD = "standard"
    STARTER = "starter"

    def __str__(self) -> str:
        return str(self.value)
