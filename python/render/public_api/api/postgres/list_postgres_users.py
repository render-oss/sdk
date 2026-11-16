from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.list_postgres_users_response_200_item import ListPostgresUsersResponse200Item
from ...types import Response


def _get_kwargs(
    postgres_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/postgres/{postgres_id}/credentials".format(
            postgres_id=quote(str(postgres_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Error | list[ListPostgresUsersResponse200Item] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ListPostgresUsersResponse200Item.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[Error | list[ListPostgresUsersResponse200Item]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    postgres_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Error | list[ListPostgresUsersResponse200Item]]:
    """List PostgreSQL Users

     List PostgreSQL users for the Render Postgres instance with the provided ID.

    Args:
        postgres_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[ListPostgresUsersResponse200Item]]
    """

    kwargs = _get_kwargs(
        postgres_id=postgres_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    postgres_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Error | list[ListPostgresUsersResponse200Item] | None:
    """List PostgreSQL Users

     List PostgreSQL users for the Render Postgres instance with the provided ID.

    Args:
        postgres_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[ListPostgresUsersResponse200Item]
    """

    return sync_detailed(
        postgres_id=postgres_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    postgres_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Error | list[ListPostgresUsersResponse200Item]]:
    """List PostgreSQL Users

     List PostgreSQL users for the Render Postgres instance with the provided ID.

    Args:
        postgres_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[ListPostgresUsersResponse200Item]]
    """

    kwargs = _get_kwargs(
        postgres_id=postgres_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    postgres_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Error | list[ListPostgresUsersResponse200Item] | None:
    """List PostgreSQL Users

     List PostgreSQL users for the Render Postgres instance with the provided ID.

    Args:
        postgres_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[ListPostgresUsersResponse200Item]
    """

    return (
        await asyncio_detailed(
            postgres_id=postgres_id,
            client=client,
        )
    ).parsed
