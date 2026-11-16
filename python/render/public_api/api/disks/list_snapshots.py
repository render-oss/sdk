from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.disk_snapshot import DiskSnapshot
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    disk_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/disks/{disk_id}/snapshots".format(
            disk_id=quote(str(disk_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Error | list[DiskSnapshot] | None:
    if response.status_code == 201:
        response_201 = []
        _response_201 = response.json()
        for response_201_item_data in _response_201:
            response_201_item = DiskSnapshot.from_dict(response_201_item_data)

            response_201.append(response_201_item)

        return response_201

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
) -> Response[Error | list[DiskSnapshot]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    disk_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Error | list[DiskSnapshot]]:
    """List snapshots

     List snapshots for the persistent disk with the provided ID. Each snapshot is a point-in-time copy
    of the disk's data.

    Args:
        disk_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[DiskSnapshot]]
    """

    kwargs = _get_kwargs(
        disk_id=disk_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    disk_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Error | list[DiskSnapshot] | None:
    """List snapshots

     List snapshots for the persistent disk with the provided ID. Each snapshot is a point-in-time copy
    of the disk's data.

    Args:
        disk_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[DiskSnapshot]
    """

    return sync_detailed(
        disk_id=disk_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    disk_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Error | list[DiskSnapshot]]:
    """List snapshots

     List snapshots for the persistent disk with the provided ID. Each snapshot is a point-in-time copy
    of the disk's data.

    Args:
        disk_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[DiskSnapshot]]
    """

    kwargs = _get_kwargs(
        disk_id=disk_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    disk_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Error | list[DiskSnapshot] | None:
    """List snapshots

     List snapshots for the persistent disk with the provided ID. Each snapshot is a point-in-time copy
    of the disk's data.

    Args:
        disk_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[DiskSnapshot]
    """

    return (
        await asyncio_detailed(
            disk_id=disk_id,
            client=client,
        )
    ).parsed
