from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.team_member import TeamMember
from ...types import Response


def _get_kwargs(
    owner_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/owners/{owner_id}/members".format(
            owner_id=quote(str(owner_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Error | list[TeamMember] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemasteam_members_item_data in _response_200:
            componentsschemasteam_members_item = TeamMember.from_dict(componentsschemasteam_members_item_data)

            response_200.append(componentsschemasteam_members_item)

        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

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
) -> Response[Error | list[TeamMember]]:
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
) -> Response[Error | list[TeamMember]]:
    """List workspace members

     Retrieves the list of users belonging to the workspace with the provided ID.

    Args:
        owner_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[TeamMember]]
    """

    kwargs = _get_kwargs(
        owner_id=owner_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    owner_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Error | list[TeamMember] | None:
    """List workspace members

     Retrieves the list of users belonging to the workspace with the provided ID.

    Args:
        owner_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[TeamMember]
    """

    return sync_detailed(
        owner_id=owner_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    owner_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Error | list[TeamMember]]:
    """List workspace members

     Retrieves the list of users belonging to the workspace with the provided ID.

    Args:
        owner_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[TeamMember]]
    """

    kwargs = _get_kwargs(
        owner_id=owner_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    owner_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Error | list[TeamMember] | None:
    """List workspace members

     Retrieves the list of users belonging to the workspace with the provided ID.

    Args:
        owner_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[TeamMember]
    """

    return (
        await asyncio_detailed(
            owner_id=owner_id,
            client=client,
        )
    ).parsed
