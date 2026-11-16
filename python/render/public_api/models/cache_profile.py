from enum import StrEnum


class CacheProfile(StrEnum):
    NO_CACHE = "no-cache"
    ORIGIN_CONTROLLED = "origin-controlled"
    ORIGIN_CONTROLLED_ALL = "origin-controlled-all"

    def __str__(self) -> str:
        return str(self.value)
