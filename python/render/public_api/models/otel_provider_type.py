from enum import Enum


class OtelProviderType(str, Enum):
    BETTER_STACK = "BETTER_STACK"
    CUSTOM = "CUSTOM"
    DATADOG = "DATADOG"
    GRAFANA = "GRAFANA"
    HONEYCOMB = "HONEYCOMB"
    NEW_RELIC = "NEW_RELIC"

    def __str__(self) -> str:
        return str(self.value)
