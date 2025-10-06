from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.redis_connection_info import RedisConnectionInfo
from ...types import Response


def _get_kwargs(
    redis_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/redis/{redis_id}/connection-info",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, RedisConnectionInfo]]:
    if response.status_code == 200:
        response_200 = RedisConnectionInfo.from_dict(response.json())

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
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, RedisConnectionInfo]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    redis_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Error, RedisConnectionInfo]]:
    """Retrieve Redis connection info

     Retrieve connection info for a Redis instance by ID. Connection info includes sensitive information.

    Args:
        redis_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, RedisConnectionInfo]]
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
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Error, RedisConnectionInfo]]:
    """Retrieve Redis connection info

     Retrieve connection info for a Redis instance by ID. Connection info includes sensitive information.

    Args:
        redis_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, RedisConnectionInfo]
    """

    return sync_detailed(
        redis_id=redis_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    redis_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Error, RedisConnectionInfo]]:
    """Retrieve Redis connection info

     Retrieve connection info for a Redis instance by ID. Connection info includes sensitive information.

    Args:
        redis_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, RedisConnectionInfo]]
    """

    kwargs = _get_kwargs(
        redis_id=redis_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    redis_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Error, RedisConnectionInfo]]:
    """Retrieve Redis connection info

     Retrieve connection info for a Redis instance by ID. Connection info includes sensitive information.

    Args:
        redis_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, RedisConnectionInfo]
    """

    return (
        await asyncio_detailed(
            redis_id=redis_id,
            client=client,
        )
    ).parsed
