from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.owner_with_cursor import OwnerWithCursor
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    name: Union[Unset, list[str]] = UNSET,
    email: Union[Unset, list[str]] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_name: Union[Unset, list[str]] = UNSET
    if not isinstance(name, Unset):
        json_name = name

    params["name"] = json_name

    json_email: Union[Unset, list[str]] = UNSET
    if not isinstance(email, Unset):
        json_email = email

    params["email"] = json_email

    params["cursor"] = cursor

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/owners",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, list["OwnerWithCursor"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = OwnerWithCursor.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 406:
        response_406 = Error.from_dict(response.json())

        return response_406

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
) -> Response[Union[Error, list["OwnerWithCursor"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    name: Union[Unset, list[str]] = UNSET,
    email: Union[Unset, list[str]] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> Response[Union[Error, list["OwnerWithCursor"]]]:
    """List workspaces

     List the workspaces that your API key has access to, optionally filtered by name or owner email
    address.

    Args:
        name (Union[Unset, list[str]]):
        email (Union[Unset, list[str]]):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, list['OwnerWithCursor']]]
    """

    kwargs = _get_kwargs(
        name=name,
        email=email,
        cursor=cursor,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    name: Union[Unset, list[str]] = UNSET,
    email: Union[Unset, list[str]] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> Optional[Union[Error, list["OwnerWithCursor"]]]:
    """List workspaces

     List the workspaces that your API key has access to, optionally filtered by name or owner email
    address.

    Args:
        name (Union[Unset, list[str]]):
        email (Union[Unset, list[str]]):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, list['OwnerWithCursor']]
    """

    return sync_detailed(
        client=client,
        name=name,
        email=email,
        cursor=cursor,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    name: Union[Unset, list[str]] = UNSET,
    email: Union[Unset, list[str]] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> Response[Union[Error, list["OwnerWithCursor"]]]:
    """List workspaces

     List the workspaces that your API key has access to, optionally filtered by name or owner email
    address.

    Args:
        name (Union[Unset, list[str]]):
        email (Union[Unset, list[str]]):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, list['OwnerWithCursor']]]
    """

    kwargs = _get_kwargs(
        name=name,
        email=email,
        cursor=cursor,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    name: Union[Unset, list[str]] = UNSET,
    email: Union[Unset, list[str]] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> Optional[Union[Error, list["OwnerWithCursor"]]]:
    """List workspaces

     List the workspaces that your API key has access to, optionally filtered by name or owner email
    address.

    Args:
        name (Union[Unset, list[str]]):
        email (Union[Unset, list[str]]):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, list['OwnerWithCursor']]
    """

    return (
        await asyncio_detailed(
            client=client,
            name=name,
            email=email,
            cursor=cursor,
            limit=limit,
        )
    ).parsed
