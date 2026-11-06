from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.sandbox_build_status import SandboxBuildStatus
from ...models.sandbox_build_with_cursor import SandboxBuildWithCursor
from ...types import UNSET, Response, Unset


def _get_kwargs(
    sandbox_group_id: str,
    *,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
    name: Union[Unset, str] = UNSET,
    status: Union[Unset, list[SandboxBuildStatus]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["cursor"] = cursor

    params["limit"] = limit

    params["name"] = name

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
        "url": f"/sandbox-groups/{sandbox_group_id}/builds",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, list["SandboxBuildWithCursor"]]]:
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
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, list["SandboxBuildWithCursor"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    sandbox_group_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
    name: Union[Unset, str] = UNSET,
    status: Union[Unset, list[SandboxBuildStatus]] = UNSET,
) -> Response[Union[Error, list["SandboxBuildWithCursor"]]]:
    """List sandbox builds

     Builds in a sandbox group, newest first.

    400 with `code: invalid_sandbox_group_id` if `sandboxGroupId` is not a
    well-formed `sbg-` ID, `code: invalid_status` for a status outside the
    build status vocabulary, `code: invalid_cursor` for a malformed cursor,
    or `code: invalid_limit` for a limit outside 1 to 100.

    Args:
        sandbox_group_id (str):  Example: sbg-cph1rs3idesc73a2b2mg.
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.
        name (Union[Unset, str]):
        status (Union[Unset, list[SandboxBuildStatus]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, list['SandboxBuildWithCursor']]]
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
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
    name: Union[Unset, str] = UNSET,
    status: Union[Unset, list[SandboxBuildStatus]] = UNSET,
) -> Optional[Union[Error, list["SandboxBuildWithCursor"]]]:
    """List sandbox builds

     Builds in a sandbox group, newest first.

    400 with `code: invalid_sandbox_group_id` if `sandboxGroupId` is not a
    well-formed `sbg-` ID, `code: invalid_status` for a status outside the
    build status vocabulary, `code: invalid_cursor` for a malformed cursor,
    or `code: invalid_limit` for a limit outside 1 to 100.

    Args:
        sandbox_group_id (str):  Example: sbg-cph1rs3idesc73a2b2mg.
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.
        name (Union[Unset, str]):
        status (Union[Unset, list[SandboxBuildStatus]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, list['SandboxBuildWithCursor']]
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
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
    name: Union[Unset, str] = UNSET,
    status: Union[Unset, list[SandboxBuildStatus]] = UNSET,
) -> Response[Union[Error, list["SandboxBuildWithCursor"]]]:
    """List sandbox builds

     Builds in a sandbox group, newest first.

    400 with `code: invalid_sandbox_group_id` if `sandboxGroupId` is not a
    well-formed `sbg-` ID, `code: invalid_status` for a status outside the
    build status vocabulary, `code: invalid_cursor` for a malformed cursor,
    or `code: invalid_limit` for a limit outside 1 to 100.

    Args:
        sandbox_group_id (str):  Example: sbg-cph1rs3idesc73a2b2mg.
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.
        name (Union[Unset, str]):
        status (Union[Unset, list[SandboxBuildStatus]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, list['SandboxBuildWithCursor']]]
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
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
    name: Union[Unset, str] = UNSET,
    status: Union[Unset, list[SandboxBuildStatus]] = UNSET,
) -> Optional[Union[Error, list["SandboxBuildWithCursor"]]]:
    """List sandbox builds

     Builds in a sandbox group, newest first.

    400 with `code: invalid_sandbox_group_id` if `sandboxGroupId` is not a
    well-formed `sbg-` ID, `code: invalid_status` for a status outside the
    build status vocabulary, `code: invalid_cursor` for a malformed cursor,
    or `code: invalid_limit` for a limit outside 1 to 100.

    Args:
        sandbox_group_id (str):  Example: sbg-cph1rs3idesc73a2b2mg.
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.
        name (Union[Unset, str]):
        status (Union[Unset, list[SandboxBuildStatus]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, list['SandboxBuildWithCursor']]
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
