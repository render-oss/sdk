from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.metrics_stream import MetricsStream
from ...models.metrics_stream_input import MetricsStreamInput
from ...types import Response


def _get_kwargs(
    owner_id: str,
    *,
    body: MetricsStreamInput,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/metrics-stream/{owner_id}".format(
            owner_id=quote(str(owner_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx2.Response) -> Error | MetricsStream | None:
    if response.status_code == 200:
        response_200 = MetricsStream.from_dict(response.json())

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
) -> Response[Error | MetricsStream]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    owner_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: MetricsStreamInput,
) -> Response[Error | MetricsStream]:
    """Create or update metrics stream

     Creates or updates the metrics stream for the specified workspace.

    Args:
        owner_id (str):
        body (MetricsStreamInput): Input for creating or updating a metrics stream

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | MetricsStream]
    """

    kwargs = _get_kwargs(
        owner_id=owner_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    owner_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: MetricsStreamInput,
) -> Error | MetricsStream | None:
    """Create or update metrics stream

     Creates or updates the metrics stream for the specified workspace.

    Args:
        owner_id (str):
        body (MetricsStreamInput): Input for creating or updating a metrics stream

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | MetricsStream
    """

    return sync_detailed(
        owner_id=owner_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    owner_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: MetricsStreamInput,
) -> Response[Error | MetricsStream]:
    """Create or update metrics stream

     Creates or updates the metrics stream for the specified workspace.

    Args:
        owner_id (str):
        body (MetricsStreamInput): Input for creating or updating a metrics stream

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | MetricsStream]
    """

    kwargs = _get_kwargs(
        owner_id=owner_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    owner_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: MetricsStreamInput,
) -> Error | MetricsStream | None:
    """Create or update metrics stream

     Creates or updates the metrics stream for the specified workspace.

    Args:
        owner_id (str):
        body (MetricsStreamInput): Input for creating or updating a metrics stream

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | MetricsStream
    """

    return (
        await asyncio_detailed(
            owner_id=owner_id,
            client=client,
            body=body,
        )
    ).parsed
