from enum import StrEnum


class OtelProviderType(StrEnum):
    BETTER_STACK = "BETTER_STACK"
    CUSTOM = "CUSTOM"
    DATADOG = "DATADOG"
    GRAFANA = "GRAFANA"
    GROUNDCOVER = "GROUNDCOVER"
    HONEYCOMB = "HONEYCOMB"
    LOGFIRE = "LOGFIRE"
    NEW_RELIC = "NEW_RELIC"
    SIGNOZ = "SIGNOZ"

    def __str__(self) -> str:
        return str(self.value)
