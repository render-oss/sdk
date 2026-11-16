import datetime
from http import HTTPStatus
from typing import Any

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.get_bandwidth_sources_response_200 import GetBandwidthSourcesResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    start_time: datetime.datetime | Unset = UNSET,
    end_time: datetime.datetime | Unset = UNSET,
    resource: str | Unset = UNSET,
    service: str | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_start_time: str | Unset = UNSET
    if not isinstance(start_time, Unset):
        json_start_time = start_time.isoformat()
    params["startTime"] = json_start_time

    json_end_time: str | Unset = UNSET
    if not isinstance(end_time, Unset):
        json_end_time = end_time.isoformat()
    params["endTime"] = json_end_time

    params["resource"] = resource

    params["service"] = service

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/metrics/bandwidth-sources",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Error | GetBandwidthSourcesResponse200 | None:
    if response.status_code == 200:
        response_200 = GetBandwidthSourcesResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Response[Error | GetBandwidthSourcesResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    start_time: datetime.datetime | Unset = UNSET,
    end_time: datetime.datetime | Unset = UNSET,
    resource: str | Unset = UNSET,
    service: str | Unset = UNSET,
) -> Response[Error | GetBandwidthSourcesResponse200]:
    """Get bandwidth usage breakdown by traffic source

     Get bandwidth usage for one or more resources broken down by traffic source (HTTP, WebSocket, NAT,
    PrivateLink).

    Returns hourly data points with traffic source breakdown. Traffic source data is available from
    March 9, 2025 onwards.
    Queries for earlier dates will return a 400 Bad Request error.

    Args:
        start_time (datetime.datetime | Unset):  Example: 2021-06-17T08:15:30Z.
        end_time (datetime.datetime | Unset):  Example: 2021-06-17T08:30:30Z.
        resource (str | Unset):  Example: srv-xxxxx.
        service (str | Unset):  Example: srv-xxxxx.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GetBandwidthSourcesResponse200]
    """

    kwargs = _get_kwargs(
        start_time=start_time,
        end_time=end_time,
        resource=resource,
        service=service,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    start_time: datetime.datetime | Unset = UNSET,
    end_time: datetime.datetime | Unset = UNSET,
    resource: str | Unset = UNSET,
    service: str | Unset = UNSET,
) -> Error | GetBandwidthSourcesResponse200 | None:
    """Get bandwidth usage breakdown by traffic source

     Get bandwidth usage for one or more resources broken down by traffic source (HTTP, WebSocket, NAT,
    PrivateLink).

    Returns hourly data points with traffic source breakdown. Traffic source data is available from
    March 9, 2025 onwards.
    Queries for earlier dates will return a 400 Bad Request error.

    Args:
        start_time (datetime.datetime | Unset):  Example: 2021-06-17T08:15:30Z.
        end_time (datetime.datetime | Unset):  Example: 2021-06-17T08:30:30Z.
        resource (str | Unset):  Example: srv-xxxxx.
        service (str | Unset):  Example: srv-xxxxx.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GetBandwidthSourcesResponse200
    """

    return sync_detailed(
        client=client,
        start_time=start_time,
        end_time=end_time,
        resource=resource,
        service=service,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    start_time: datetime.datetime | Unset = UNSET,
    end_time: datetime.datetime | Unset = UNSET,
    resource: str | Unset = UNSET,
    service: str | Unset = UNSET,
) -> Response[Error | GetBandwidthSourcesResponse200]:
    """Get bandwidth usage breakdown by traffic source

     Get bandwidth usage for one or more resources broken down by traffic source (HTTP, WebSocket, NAT,
    PrivateLink).

    Returns hourly data points with traffic source breakdown. Traffic source data is available from
    March 9, 2025 onwards.
    Queries for earlier dates will return a 400 Bad Request error.

    Args:
        start_time (datetime.datetime | Unset):  Example: 2021-06-17T08:15:30Z.
        end_time (datetime.datetime | Unset):  Example: 2021-06-17T08:30:30Z.
        resource (str | Unset):  Example: srv-xxxxx.
        service (str | Unset):  Example: srv-xxxxx.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GetBandwidthSourcesResponse200]
    """

    kwargs = _get_kwargs(
        start_time=start_time,
        end_time=end_time,
        resource=resource,
        service=service,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    start_time: datetime.datetime | Unset = UNSET,
    end_time: datetime.datetime | Unset = UNSET,
    resource: str | Unset = UNSET,
    service: str | Unset = UNSET,
) -> Error | GetBandwidthSourcesResponse200 | None:
    """Get bandwidth usage breakdown by traffic source

     Get bandwidth usage for one or more resources broken down by traffic source (HTTP, WebSocket, NAT,
    PrivateLink).

    Returns hourly data points with traffic source breakdown. Traffic source data is available from
    March 9, 2025 onwards.
    Queries for earlier dates will return a 400 Bad Request error.

    Args:
        start_time (datetime.datetime | Unset):  Example: 2021-06-17T08:15:30Z.
        end_time (datetime.datetime | Unset):  Example: 2021-06-17T08:30:30Z.
        resource (str | Unset):  Example: srv-xxxxx.
        service (str | Unset):  Example: srv-xxxxx.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GetBandwidthSourcesResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            start_time=start_time,
            end_time=end_time,
            resource=resource,
            service=service,
        )
    ).parsed
