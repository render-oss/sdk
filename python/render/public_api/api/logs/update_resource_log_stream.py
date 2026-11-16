from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.log_stream_resource_update import LogStreamResourceUpdate
from ...models.resource_log_stream_setting import ResourceLogStreamSetting
from ...types import Response


def _get_kwargs(
    resource_id: str,
    *,
    body: LogStreamResourceUpdate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/logs/streams/resource/{resource_id}".format(
            resource_id=quote(str(resource_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Error | ResourceLogStreamSetting | None:
    if response.status_code == 200:
        response_200 = ResourceLogStreamSetting.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404

    if response.status_code == 406:
        response_406 = Error.from_dict(response.json())

        return response_406

    if response.status_code == 410:
        response_410 = Error.from_dict(response.json())

        return response_410

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())

        return response_500

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Response[Error | ResourceLogStreamSetting]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    resource_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: LogStreamResourceUpdate,
) -> Response[Error | ResourceLogStreamSetting]:
    """Update log stream override

     Updates log stream override information for the specified resource. A log stream override takes
    precedence over a workspace's default log stream.

    Args:
        resource_id (str):
        body (LogStreamResourceUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ResourceLogStreamSetting]
    """

    kwargs = _get_kwargs(
        resource_id=resource_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    resource_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: LogStreamResourceUpdate,
) -> Error | ResourceLogStreamSetting | None:
    """Update log stream override

     Updates log stream override information for the specified resource. A log stream override takes
    precedence over a workspace's default log stream.

    Args:
        resource_id (str):
        body (LogStreamResourceUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ResourceLogStreamSetting
    """

    return sync_detailed(
        resource_id=resource_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    resource_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: LogStreamResourceUpdate,
) -> Response[Error | ResourceLogStreamSetting]:
    """Update log stream override

     Updates log stream override information for the specified resource. A log stream override takes
    precedence over a workspace's default log stream.

    Args:
        resource_id (str):
        body (LogStreamResourceUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ResourceLogStreamSetting]
    """

    kwargs = _get_kwargs(
        resource_id=resource_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    resource_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: LogStreamResourceUpdate,
) -> Error | ResourceLogStreamSetting | None:
    """Update log stream override

     Updates log stream override information for the specified resource. A log stream override takes
    precedence over a workspace's default log stream.

    Args:
        resource_id (str):
        body (LogStreamResourceUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ResourceLogStreamSetting
    """

    return (
        await asyncio_detailed(
            resource_id=resource_id,
            client=client,
            body=body,
        )
    ).parsed
