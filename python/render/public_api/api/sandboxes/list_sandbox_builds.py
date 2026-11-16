from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.sandbox_build_status import SandboxBuildStatus
from ...models.sandbox_build_with_cursor import SandboxBuildWithCursor
from ...types import UNSET, Response, Unset


def _get_kwargs(
    sandbox_group_id: str,
    *,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 20,
    name: str | Unset = UNSET,
    status: list[SandboxBuildStatus] | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["cursor"] = cursor

    params["limit"] = limit

    params["name"] = name

    json_status: list[str] | Unset = UNSET
    if not isinstance(status, Unset):
        json_status = []
        for status_item_data in status:
            status_item = status_item_data.value
            json_status.append(status_item)

    params["status"] = json_status

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/sandbox-groups/{sandbox_group_id}/builds".format(
            sandbox_group_id=quote(str(sandbox_group_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Error | list[SandboxBuildWithCursor] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = SandboxBuildWithCursor.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[Error | list[SandboxBuildWithCursor]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    sandbox_group_id: str,
    *,
    client: AuthenticatedClient | Client,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 20,
    name: str | Unset = UNSET,
    status: list[SandboxBuildStatus] | Unset = UNSET,
) -> Response[Error | list[SandboxBuildWithCursor]]:
    """List sandbox builds

     List builds in a sandbox group, newest first.

    Args:
        sandbox_group_id (str): The ID of the sandbox group. Example: sbg-cph1rs3idesc73a2b2mg.
        cursor (str | Unset):
        limit (int | Unset): Defaults to 20 Default: 20.
        name (str | Unset):
        status (list[SandboxBuildStatus] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[SandboxBuildWithCursor]]
    """

    kwargs = _get_kwargs(
        sandbox_group_id=sandbox_group_id,
        cursor=cursor,
        limit=limit,
        name=name,
        status=status,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    sandbox_group_id: str,
    *,
    client: AuthenticatedClient | Client,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 20,
    name: str | Unset = UNSET,
    status: list[SandboxBuildStatus] | Unset = UNSET,
) -> Error | list[SandboxBuildWithCursor] | None:
    """List sandbox builds

     List builds in a sandbox group, newest first.

    Args:
        sandbox_group_id (str): The ID of the sandbox group. Example: sbg-cph1rs3idesc73a2b2mg.
        cursor (str | Unset):
        limit (int | Unset): Defaults to 20 Default: 20.
        name (str | Unset):
        status (list[SandboxBuildStatus] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[SandboxBuildWithCursor]
    """

    return sync_detailed(
        sandbox_group_id=sandbox_group_id,
        client=client,
        cursor=cursor,
        limit=limit,
        name=name,
        status=status,
    ).parsed


async def asyncio_detailed(
    sandbox_group_id: str,
    *,
    client: AuthenticatedClient | Client,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 20,
    name: str | Unset = UNSET,
    status: list[SandboxBuildStatus] | Unset = UNSET,
) -> Response[Error | list[SandboxBuildWithCursor]]:
    """List sandbox builds

     List builds in a sandbox group, newest first.

    Args:
        sandbox_group_id (str): The ID of the sandbox group. Example: sbg-cph1rs3idesc73a2b2mg.
        cursor (str | Unset):
        limit (int | Unset): Defaults to 20 Default: 20.
        name (str | Unset):
        status (list[SandboxBuildStatus] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[SandboxBuildWithCursor]]
    """

    kwargs = _get_kwargs(
        sandbox_group_id=sandbox_group_id,
        cursor=cursor,
        limit=limit,
        name=name,
        status=status,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    sandbox_group_id: str,
    *,
    client: AuthenticatedClient | Client,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 20,
    name: str | Unset = UNSET,
    status: list[SandboxBuildStatus] | Unset = UNSET,
) -> Error | list[SandboxBuildWithCursor] | None:
    """List sandbox builds

     List builds in a sandbox group, newest first.

    Args:
        sandbox_group_id (str): The ID of the sandbox group. Example: sbg-cph1rs3idesc73a2b2mg.
        cursor (str | Unset):
        limit (int | Unset): Defaults to 20 Default: 20.
        name (str | Unset):
        status (list[SandboxBuildStatus] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[SandboxBuildWithCursor]
    """

    return (
        await asyncio_detailed(
            sandbox_group_id=sandbox_group_id,
            client=client,
            cursor=cursor,
            limit=limit,
            name=name,
            status=status,
        )
    ).parsed
