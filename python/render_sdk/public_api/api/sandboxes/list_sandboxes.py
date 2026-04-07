from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.sandbox_status import SandboxStatus
from ...models.sandbox_with_cursor import SandboxWithCursor
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    owner_id: Union[Unset, list[str]] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
    status: Union[Unset, list[SandboxStatus]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_owner_id: Union[Unset, list[str]] = UNSET
    if not isinstance(owner_id, Unset):
        json_owner_id = owner_id

    params["ownerId"] = json_owner_id

    params["cursor"] = cursor

    params["limit"] = limit

    json_status: Union[Unset, list[str]] = UNSET
    if not isinstance(status, Unset):
        json_status = []
        for status_item_data in status:
            status_item = status_item_data.value
            json_status.append(status_item)

    params["status"] = json_status

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/sandboxes",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, list["SandboxWithCursor"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = SandboxWithCursor.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())

        return response_403

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
) -> Response[Union[Error, list["SandboxWithCursor"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    owner_id: Union[Unset, list[str]] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
    status: Union[Unset, list[SandboxStatus]] = UNSET,
) -> Response[Union[Error, list["SandboxWithCursor"]]]:
    """List sandboxes

     List sandboxes for the specified workspaces. If no workspaces are provided, returns
    all sandboxes the API key has access to.

    Args:
        owner_id (Union[Unset, list[str]]):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.
        status (Union[Unset, list[SandboxStatus]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, list['SandboxWithCursor']]]
    """

    kwargs = _get_kwargs(
        owner_id=owner_id,
        cursor=cursor,
        limit=limit,
        status=status,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    owner_id: Union[Unset, list[str]] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
    status: Union[Unset, list[SandboxStatus]] = UNSET,
) -> Optional[Union[Error, list["SandboxWithCursor"]]]:
    """List sandboxes

     List sandboxes for the specified workspaces. If no workspaces are provided, returns
    all sandboxes the API key has access to.

    Args:
        owner_id (Union[Unset, list[str]]):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.
        status (Union[Unset, list[SandboxStatus]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, list['SandboxWithCursor']]
    """

    return sync_detailed(
        client=client,
        owner_id=owner_id,
        cursor=cursor,
        limit=limit,
        status=status,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    owner_id: Union[Unset, list[str]] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
    status: Union[Unset, list[SandboxStatus]] = UNSET,
) -> Response[Union[Error, list["SandboxWithCursor"]]]:
    """List sandboxes

     List sandboxes for the specified workspaces. If no workspaces are provided, returns
    all sandboxes the API key has access to.

    Args:
        owner_id (Union[Unset, list[str]]):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.
        status (Union[Unset, list[SandboxStatus]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, list['SandboxWithCursor']]]
    """

    kwargs = _get_kwargs(
        owner_id=owner_id,
        cursor=cursor,
        limit=limit,
        status=status,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    owner_id: Union[Unset, list[str]] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
    status: Union[Unset, list[SandboxStatus]] = UNSET,
) -> Optional[Union[Error, list["SandboxWithCursor"]]]:
    """List sandboxes

     List sandboxes for the specified workspaces. If no workspaces are provided, returns
    all sandboxes the API key has access to.

    Args:
        owner_id (Union[Unset, list[str]]):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.
        status (Union[Unset, list[SandboxStatus]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, list['SandboxWithCursor']]
    """

    return (
        await asyncio_detailed(
            client=client,
            owner_id=owner_id,
            cursor=cursor,
            limit=limit,
            status=status,
        )
    ).parsed
