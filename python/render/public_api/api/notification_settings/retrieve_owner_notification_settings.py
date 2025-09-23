from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.notification_setting import NotificationSetting
from ...types import Response


def _get_kwargs(
    owner_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/notification-settings/owners/{owner_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, NotificationSetting]]:
    if response.status_code == 200:
        response_200 = NotificationSetting.from_dict(response.json())

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
) -> Response[Union[Error, NotificationSetting]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    owner_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Error, NotificationSetting]]:
    """Retrieve notification settings

     Retrieve notification settings for the owner with the provided ID.

    Note that you provide an owner ID to this endpoint, not the ID for a particular resource.

    Args:
        owner_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, NotificationSetting]]
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
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Error, NotificationSetting]]:
    """Retrieve notification settings

     Retrieve notification settings for the owner with the provided ID.

    Note that you provide an owner ID to this endpoint, not the ID for a particular resource.

    Args:
        owner_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, NotificationSetting]
    """

    return sync_detailed(
        owner_id=owner_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    owner_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Error, NotificationSetting]]:
    """Retrieve notification settings

     Retrieve notification settings for the owner with the provided ID.

    Note that you provide an owner ID to this endpoint, not the ID for a particular resource.

    Args:
        owner_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, NotificationSetting]]
    """

    kwargs = _get_kwargs(
        owner_id=owner_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    owner_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Error, NotificationSetting]]:
    """Retrieve notification settings

     Retrieve notification settings for the owner with the provided ID.

    Note that you provide an owner ID to this endpoint, not the ID for a particular resource.

    Args:
        owner_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, NotificationSetting]
    """

    return (
        await asyncio_detailed(
            owner_id=owner_id,
            client=client,
        )
    ).parsed
