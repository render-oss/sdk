from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.disk_details import DiskDetails
from ...models.disk_patch import DiskPATCH
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    disk_id: str,
    *,
    body: DiskPATCH,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": f"/disks/{disk_id}",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DiskDetails, Error]]:
    if response.status_code == 200:
        response_200 = DiskDetails.from_dict(response.json())

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
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[DiskDetails, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    disk_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: DiskPATCH,
) -> Response[Union[DiskDetails, Error]]:
    """Update disk

     Update the persistent disk with the provided ID.

    The disk's associated service must be deployed and active for updates to take effect.

    When resizing a disk, the new size must be greater than the current size.

    Args:
        disk_id (str):  Example: dsk-cph1rs3idesc73a2b2mg.
        body (DiskPATCH):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DiskDetails, Error]]
    """

    kwargs = _get_kwargs(
        disk_id=disk_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    disk_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: DiskPATCH,
) -> Optional[Union[DiskDetails, Error]]:
    """Update disk

     Update the persistent disk with the provided ID.

    The disk's associated service must be deployed and active for updates to take effect.

    When resizing a disk, the new size must be greater than the current size.

    Args:
        disk_id (str):  Example: dsk-cph1rs3idesc73a2b2mg.
        body (DiskPATCH):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DiskDetails, Error]
    """

    return sync_detailed(
        disk_id=disk_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    disk_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: DiskPATCH,
) -> Response[Union[DiskDetails, Error]]:
    """Update disk

     Update the persistent disk with the provided ID.

    The disk's associated service must be deployed and active for updates to take effect.

    When resizing a disk, the new size must be greater than the current size.

    Args:
        disk_id (str):  Example: dsk-cph1rs3idesc73a2b2mg.
        body (DiskPATCH):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DiskDetails, Error]]
    """

    kwargs = _get_kwargs(
        disk_id=disk_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    disk_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: DiskPATCH,
) -> Optional[Union[DiskDetails, Error]]:
    """Update disk

     Update the persistent disk with the provided ID.

    The disk's associated service must be deployed and active for updates to take effect.

    When resizing a disk, the new size must be greater than the current size.

    Args:
        disk_id (str):  Example: dsk-cph1rs3idesc73a2b2mg.
        body (DiskPATCH):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DiskDetails, Error]
    """

    return (
        await asyncio_detailed(
            disk_id=disk_id,
            client=client,
            body=body,
        )
    ).parsed
