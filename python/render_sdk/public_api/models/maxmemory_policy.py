from enum import Enum


class MaxmemoryPolicy(str, Enum):
    ALLKEYS_LFU = "allkeys_lfu"
    ALLKEYS_LRU = "allkeys_lru"
    ALLKEYS_RANDOM = "allkeys_random"
    NOEVICTION = "noeviction"
    VOLATILE_LFU = "volatile_lfu"
    VOLATILE_LRU = "volatile_lru"
    VOLATILE_RANDOM = "volatile_random"
    VOLATILE_TTL = "volatile_ttl"

    def __str__(self) -> str:
        return str(self.value)
