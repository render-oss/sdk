from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.key_value_connection_info import KeyValueConnectionInfo
from ...types import Response


def _get_kwargs(
    redis_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/key-value/{redis_id}/connection-info".format(
            redis_id=quote(str(redis_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Error | KeyValueConnectionInfo | None:
    if response.status_code == 200:
        response_200 = KeyValueConnectionInfo.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404

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
) -> Response[Error | KeyValueConnectionInfo]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    redis_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Error | KeyValueConnectionInfo]:
    """Retrieve Key Value connection info

     Retrieve connection info for a Key Value instance by ID. Connection info includes sensitive
    information.

    Args:
        redis_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | KeyValueConnectionInfo]
    """

    kwargs = _get_kwargs(
        redis_id=redis_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    redis_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Error | KeyValueConnectionInfo | None:
    """Retrieve Key Value connection info

     Retrieve connection info for a Key Value instance by ID. Connection info includes sensitive
    information.

    Args:
        redis_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | KeyValueConnectionInfo
    """

    return sync_detailed(
        redis_id=redis_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    redis_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Error | KeyValueConnectionInfo]:
    """Retrieve Key Value connection info

     Retrieve connection info for a Key Value instance by ID. Connection info includes sensitive
    information.

    Args:
        redis_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | KeyValueConnectionInfo]
    """

    kwargs = _get_kwargs(
        redis_id=redis_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    redis_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Error | KeyValueConnectionInfo | None:
    """Retrieve Key Value connection info

     Retrieve connection info for a Key Value instance by ID. Connection info includes sensitive
    information.

    Args:
        redis_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | KeyValueConnectionInfo
    """

    return (
        await asyncio_detailed(
            redis_id=redis_id,
            client=client,
        )
    ).parsed
