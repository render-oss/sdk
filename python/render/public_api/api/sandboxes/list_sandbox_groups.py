from http import HTTPStatus
from typing import Any

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.sandbox_group_with_cursor import SandboxGroupWithCursor
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    owner_id: str,
    cursor: str | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["ownerId"] = owner_id

    params["cursor"] = cursor

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/sandbox-groups",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Error | list[SandboxGroupWithCursor] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = SandboxGroupWithCursor.from_dict(response_200_item_data)

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
) -> Response[Error | list[SandboxGroupWithCursor]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    owner_id: str,
    cursor: str | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> Response[Error | list[SandboxGroupWithCursor]]:
    """List sandbox groups

     List sandbox groups in a workspace, newest first. Returns up to 20 groups by default, with a maximum
    of 100. To fetch the next page, pass the last result's cursor as `cursor`. Continue until the
    response is empty.

    Args:
        owner_id (str):
        cursor (str | Unset):
        limit (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[SandboxGroupWithCursor]]
    """

    kwargs = _get_kwargs(
        owner_id=owner_id,
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
    owner_id: str,
    cursor: str | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> Error | list[SandboxGroupWithCursor] | None:
    """List sandbox groups

     List sandbox groups in a workspace, newest first. Returns up to 20 groups by default, with a maximum
    of 100. To fetch the next page, pass the last result's cursor as `cursor`. Continue until the
    response is empty.

    Args:
        owner_id (str):
        cursor (str | Unset):
        limit (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[SandboxGroupWithCursor]
    """

    return sync_detailed(
        client=client,
        owner_id=owner_id,
        cursor=cursor,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    owner_id: str,
    cursor: str | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> Response[Error | list[SandboxGroupWithCursor]]:
    """List sandbox groups

     List sandbox groups in a workspace, newest first. Returns up to 20 groups by default, with a maximum
    of 100. To fetch the next page, pass the last result's cursor as `cursor`. Continue until the
    response is empty.

    Args:
        owner_id (str):
        cursor (str | Unset):
        limit (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[SandboxGroupWithCursor]]
    """

    kwargs = _get_kwargs(
        owner_id=owner_id,
        cursor=cursor,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    owner_id: str,
    cursor: str | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> Error | list[SandboxGroupWithCursor] | None:
    """List sandbox groups

     List sandbox groups in a workspace, newest first. Returns up to 20 groups by default, with a maximum
    of 100. To fetch the next page, pass the last result's cursor as `cursor`. Continue until the
    response is empty.

    Args:
        owner_id (str):
        cursor (str | Unset):
        limit (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[SandboxGroupWithCursor]
    """

    return (
        await asyncio_detailed(
            client=client,
            owner_id=owner_id,
            cursor=cursor,
            limit=limit,
        )
    ).parsed
