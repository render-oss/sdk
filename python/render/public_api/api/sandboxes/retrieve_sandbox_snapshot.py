from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.sandbox_snapshot import SandboxSnapshot
from ...types import UNSET, Response, Unset


def _get_kwargs(
    sandbox_group_id: str,
    snapshot_id: str,
    *,
    owner_id: str | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["ownerId"] = owner_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/sandbox-groups/{sandbox_group_id}/snapshots/{snapshot_id}".format(
            sandbox_group_id=quote(str(sandbox_group_id), safe=""),
            snapshot_id=quote(str(snapshot_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Error | SandboxSnapshot | None:
    if response.status_code == 200:
        response_200 = SandboxSnapshot.from_dict(response.json())

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
) -> Response[Error | SandboxSnapshot]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    sandbox_group_id: str,
    snapshot_id: str,
    *,
    client: AuthenticatedClient | Client,
    owner_id: str | Unset = UNSET,
) -> Response[Error | SandboxSnapshot]:
    """Retrieve sandbox snapshot

     Retrieve a snapshot by ID.

    Args:
        sandbox_group_id (str): The ID of the sandbox group. Example: sbg-cph1rs3idesc73a2b2mg.
        snapshot_id (str): The ID of the sandbox snapshot. Example: snp-cph1rs3idesc73a2b2mg.
        owner_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SandboxSnapshot]
    """

    kwargs = _get_kwargs(
        sandbox_group_id=sandbox_group_id,
        snapshot_id=snapshot_id,
        owner_id=owner_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    sandbox_group_id: str,
    snapshot_id: str,
    *,
    client: AuthenticatedClient | Client,
    owner_id: str | Unset = UNSET,
) -> Error | SandboxSnapshot | None:
    """Retrieve sandbox snapshot

     Retrieve a snapshot by ID.

    Args:
        sandbox_group_id (str): The ID of the sandbox group. Example: sbg-cph1rs3idesc73a2b2mg.
        snapshot_id (str): The ID of the sandbox snapshot. Example: snp-cph1rs3idesc73a2b2mg.
        owner_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SandboxSnapshot
    """

    return sync_detailed(
        sandbox_group_id=sandbox_group_id,
        snapshot_id=snapshot_id,
        client=client,
        owner_id=owner_id,
    ).parsed


async def asyncio_detailed(
    sandbox_group_id: str,
    snapshot_id: str,
    *,
    client: AuthenticatedClient | Client,
    owner_id: str | Unset = UNSET,
) -> Response[Error | SandboxSnapshot]:
    """Retrieve sandbox snapshot

     Retrieve a snapshot by ID.

    Args:
        sandbox_group_id (str): The ID of the sandbox group. Example: sbg-cph1rs3idesc73a2b2mg.
        snapshot_id (str): The ID of the sandbox snapshot. Example: snp-cph1rs3idesc73a2b2mg.
        owner_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SandboxSnapshot]
    """

    kwargs = _get_kwargs(
        sandbox_group_id=sandbox_group_id,
        snapshot_id=snapshot_id,
        owner_id=owner_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    sandbox_group_id: str,
    snapshot_id: str,
    *,
    client: AuthenticatedClient | Client,
    owner_id: str | Unset = UNSET,
) -> Error | SandboxSnapshot | None:
    """Retrieve sandbox snapshot

     Retrieve a snapshot by ID.

    Args:
        sandbox_group_id (str): The ID of the sandbox group. Example: sbg-cph1rs3idesc73a2b2mg.
        snapshot_id (str): The ID of the sandbox snapshot. Example: snp-cph1rs3idesc73a2b2mg.
        owner_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SandboxSnapshot
    """

    return (
        await asyncio_detailed(
            sandbox_group_id=sandbox_group_id,
            snapshot_id=snapshot_id,
            client=client,
            owner_id=owner_id,
        )
    ).parsed
