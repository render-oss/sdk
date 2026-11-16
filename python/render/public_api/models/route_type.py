from enum import StrEnum


class RouteType(StrEnum):
    REDIRECT = "redirect"
    REWRITE = "rewrite"

    def __str__(self) -> str:
        return str(self.value)
