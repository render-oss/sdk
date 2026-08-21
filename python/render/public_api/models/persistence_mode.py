from enum import Enum


class PersistenceMode(str, Enum):
    JOURNAL_SNAPSHOT = "journal_snapshot"
    OFF = "off"
    SNAPSHOT = "snapshot"

    def __str__(self) -> str:
        return str(self.value)
