from http import HTTPStatus
from typing import Any

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.notification_override_with_cursor import NotificationOverrideWithCursor
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    owner_id: list[str] | Unset = UNSET,
    service_id: list[str] | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 20,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_owner_id: list[str] | Unset = UNSET
    if not isinstance(owner_id, Unset):
        json_owner_id = owner_id

    params["ownerId"] = json_owner_id

    json_service_id: list[str] | Unset = UNSET
    if not isinstance(service_id, Unset):
        json_service_id = service_id

    params["serviceId"] = json_service_id

    params["cursor"] = cursor

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/notification-settings/overrides",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Error | list[NotificationOverrideWithCursor] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = NotificationOverrideWithCursor.from_dict(response_200_item_data)

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
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Response[Error | list[NotificationOverrideWithCursor]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    owner_id: list[str] | Unset = UNSET,
    service_id: list[str] | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 20,
) -> Response[Error | list[NotificationOverrideWithCursor]]:
    """List notification overrides

     List notification overrides matching the provided filters. If no filters are provided, returns all
    notification overrides for all workspaces the user belongs to.

    Args:
        owner_id (list[str] | Unset):
        service_id (list[str] | Unset):
        cursor (str | Unset):
        limit (int | Unset): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[NotificationOverrideWithCursor]]
    """

    kwargs = _get_kwargs(
        owner_id=owner_id,
        service_id=service_id,
        cursor=cursor,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    owner_id: list[str] | Unset = UNSET,
    service_id: list[str] | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 20,
) -> Error | list[NotificationOverrideWithCursor] | None:
    """List notification overrides

     List notification overrides matching the provided filters. If no filters are provided, returns all
    notification overrides for all workspaces the user belongs to.

    Args:
        owner_id (list[str] | Unset):
        service_id (list[str] | Unset):
        cursor (str | Unset):
        limit (int | Unset): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[NotificationOverrideWithCursor]
    """

    return sync_detailed(
        client=client,
        owner_id=owner_id,
        service_id=service_id,
        cursor=cursor,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    owner_id: list[str] | Unset = UNSET,
    service_id: list[str] | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 20,
) -> Response[Error | list[NotificationOverrideWithCursor]]:
    """List notification overrides

     List notification overrides matching the provided filters. If no filters are provided, returns all
    notification overrides for all workspaces the user belongs to.

    Args:
        owner_id (list[str] | Unset):
        service_id (list[str] | Unset):
        cursor (str | Unset):
        limit (int | Unset): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[NotificationOverrideWithCursor]]
    """

    kwargs = _get_kwargs(
        owner_id=owner_id,
        service_id=service_id,
        cursor=cursor,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    owner_id: list[str] | Unset = UNSET,
    service_id: list[str] | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 20,
) -> Error | list[NotificationOverrideWithCursor] | None:
    """List notification overrides

     List notification overrides matching the provided filters. If no filters are provided, returns all
    notification overrides for all workspaces the user belongs to.

    Args:
        owner_id (list[str] | Unset):
        service_id (list[str] | Unset):
        cursor (str | Unset):
        limit (int | Unset): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[NotificationOverrideWithCursor]
    """

    return (
        await asyncio_detailed(
            client=client,
            owner_id=owner_id,
            service_id=service_id,
            cursor=cursor,
            limit=limit,
        )
    ).parsed
