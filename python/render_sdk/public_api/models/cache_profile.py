from enum import Enum


class CacheProfile(str, Enum):
    NO_CACHE = "no-cache"
    ORIGIN_CONTROLLED = "origin-controlled"
    ORIGIN_CONTROLLED_ALL = "origin-controlled-all"

    def __str__(self) -> str:
        return str(self.value)
