from enum import Enum


class OtelProviderType(str, Enum):
    BETTER_STACK = "BETTER_STACK"
    CUSTOM = "CUSTOM"
    DATADOG = "DATADOG"
    GRAFANA = "GRAFANA"
    GROUNDCOVER = "GROUNDCOVER"
    HONEYCOMB = "HONEYCOMB"
    NEW_RELIC = "NEW_RELIC"
    SIGNOZ = "SIGNOZ"

    def __str__(self) -> str:
        return str(self.value)
