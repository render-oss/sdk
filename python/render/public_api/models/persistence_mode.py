from enum import StrEnum


class PersistenceMode(StrEnum):
    JOURNAL_SNAPSHOT = "journal_snapshot"
    OFF = "off"
    SNAPSHOT = "snapshot"

    def __str__(self) -> str:
        return str(self.value)
