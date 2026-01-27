from enum import Enum


class GetBandwidthSourcesResponse200DataItemLabelsTrafficSource(str, Enum):
    HTTP = "http"
    NAT = "nat"
    PRIVATELINK = "privatelink"
    TOTAL = "total"
    WEBSOCKET = "websocket"

    def __str__(self) -> str:
        return str(self.value)
