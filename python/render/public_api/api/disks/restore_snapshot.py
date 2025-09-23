from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.disk_details import DiskDetails
from ...models.error import Error
from ...models.snapshot_restore_post import SnapshotRestorePOST
from ...types import Response


def _get_kwargs(
    disk_id: str,
    *,
    body: SnapshotRestorePOST,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/disks/{disk_id}/snapshots/restore",
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
    body: SnapshotRestorePOST,
) -> Response[Union[DiskDetails, Error]]:
    """Restore snapshot

     Restore a persistent disk to an available snapshot.

    **This operation is irreversible.** It will overwrite the current disk data. It might also trigger a
    service deploy.

    Snapshot keys returned from the [List snapshots](https://api-docs.render.com/reference/list-
    snapshots) endpoint expire after 24 hours. If a snapshot key has expired, query the endpoint again
    for a new key.

    Args:
        disk_id (str):
        body (SnapshotRestorePOST):

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
    body: SnapshotRestorePOST,
) -> Optional[Union[DiskDetails, Error]]:
    """Restore snapshot

     Restore a persistent disk to an available snapshot.

    **This operation is irreversible.** It will overwrite the current disk data. It might also trigger a
    service deploy.

    Snapshot keys returned from the [List snapshots](https://api-docs.render.com/reference/list-
    snapshots) endpoint expire after 24 hours. If a snapshot key has expired, query the endpoint again
    for a new key.

    Args:
        disk_id (str):
        body (SnapshotRestorePOST):

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
    body: SnapshotRestorePOST,
) -> Response[Union[DiskDetails, Error]]:
    """Restore snapshot

     Restore a persistent disk to an available snapshot.

    **This operation is irreversible.** It will overwrite the current disk data. It might also trigger a
    service deploy.

    Snapshot keys returned from the [List snapshots](https://api-docs.render.com/reference/list-
    snapshots) endpoint expire after 24 hours. If a snapshot key has expired, query the endpoint again
    for a new key.

    Args:
        disk_id (str):
        body (SnapshotRestorePOST):

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
    body: SnapshotRestorePOST,
) -> Optional[Union[DiskDetails, Error]]:
    """Restore snapshot

     Restore a persistent disk to an available snapshot.

    **This operation is irreversible.** It will overwrite the current disk data. It might also trigger a
    service deploy.

    Snapshot keys returned from the [List snapshots](https://api-docs.render.com/reference/list-
    snapshots) endpoint expire after 24 hours. If a snapshot key has expired, query the endpoint again
    for a new key.

    Args:
        disk_id (str):
        body (SnapshotRestorePOST):

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
