from enum import StrEnum


class GetBandwidthSourcesResponse200DataItemLabelsTrafficSource(StrEnum):
    HTTP = "http"
    NAT = "nat"
    PRIVATELINK = "privatelink"
    TOTAL = "total"
    WEBSOCKET = "websocket"

    def __str__(self) -> str:
        return str(self.value)
