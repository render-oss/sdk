from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.sandbox_directory_listing import SandboxDirectoryListing
from ...types import UNSET, Response, Unset


def _get_kwargs(
    sandbox_id: str,
    *,
    path: str,
    depth: Union[Unset, int] = 1,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["path"] = path

    params["depth"] = depth

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/sandboxes/{sandbox_id}/files/list",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, SandboxDirectoryListing]]:
    if response.status_code == 200:
        response_200 = SandboxDirectoryListing.from_dict(response.json())

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

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        return response_409

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
) -> Response[Union[Error, SandboxDirectoryListing]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    sandbox_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    path: str,
    depth: Union[Unset, int] = 1,
) -> Response[Union[Error, SandboxDirectoryListing]]:
    """List directory contents in sandbox

     List the contents of a directory in a running sandbox. Returns file and
    directory metadata without transferring file contents. The sandbox must
    be `running`.

    Args:
        sandbox_id (str):  Example: sbx-cph1rs3idesc73a2b2mg.
        path (str):
        depth (Union[Unset, int]):  Default: 1.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, SandboxDirectoryListing]]
    """

    kwargs = _get_kwargs(
        sandbox_id=sandbox_id,
        path=path,
        depth=depth,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    sandbox_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    path: str,
    depth: Union[Unset, int] = 1,
) -> Optional[Union[Error, SandboxDirectoryListing]]:
    """List directory contents in sandbox

     List the contents of a directory in a running sandbox. Returns file and
    directory metadata without transferring file contents. The sandbox must
    be `running`.

    Args:
        sandbox_id (str):  Example: sbx-cph1rs3idesc73a2b2mg.
        path (str):
        depth (Union[Unset, int]):  Default: 1.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, SandboxDirectoryListing]
    """

    return sync_detailed(
        sandbox_id=sandbox_id,
        client=client,
        path=path,
        depth=depth,
    ).parsed


async def asyncio_detailed(
    sandbox_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    path: str,
    depth: Union[Unset, int] = 1,
) -> Response[Union[Error, SandboxDirectoryListing]]:
    """List directory contents in sandbox

     List the contents of a directory in a running sandbox. Returns file and
    directory metadata without transferring file contents. The sandbox must
    be `running`.

    Args:
        sandbox_id (str):  Example: sbx-cph1rs3idesc73a2b2mg.
        path (str):
        depth (Union[Unset, int]):  Default: 1.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, SandboxDirectoryListing]]
    """

    kwargs = _get_kwargs(
        sandbox_id=sandbox_id,
        path=path,
        depth=depth,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    sandbox_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    path: str,
    depth: Union[Unset, int] = 1,
) -> Optional[Union[Error, SandboxDirectoryListing]]:
    """List directory contents in sandbox

     List the contents of a directory in a running sandbox. Returns file and
    directory metadata without transferring file contents. The sandbox must
    be `running`.

    Args:
        sandbox_id (str):  Example: sbx-cph1rs3idesc73a2b2mg.
        path (str):
        depth (Union[Unset, int]):  Default: 1.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, SandboxDirectoryListing]
    """

    return (
        await asyncio_detailed(
            sandbox_id=sandbox_id,
            client=client,
            path=path,
            depth=depth,
        )
    ).parsed
