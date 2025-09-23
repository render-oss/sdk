from enum import Enum


class RouteType(str, Enum):
    REDIRECT = "redirect"
    REWRITE = "rewrite"

    def __str__(self) -> str:
        return str(self.value)
