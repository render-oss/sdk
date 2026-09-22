from enum import Enum


class ExistingResourceMode(str, Enum):
    ADOPT = "adopt"
    CREATE_NEW = "create_new"

    def __str__(self) -> str:
        return str(self.value)
