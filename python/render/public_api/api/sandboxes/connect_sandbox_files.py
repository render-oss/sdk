from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.connect_sandbox_files_operation import ConnectSandboxFilesOperation
from ...models.error import Error
from ...models.sandbox_connect_response import SandboxConnectResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    sandbox_id: str,
    operation: ConnectSandboxFilesOperation,
    *,
    owner_id: Union[Unset, str] = UNSET,
    path: str,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["ownerId"] = owner_id

    params["path"] = path

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/sandboxes/{sandbox_id}/files/{operation}/token",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, SandboxConnectResponse]]:
    if response.status_code == 201:
        response_201 = SandboxConnectResponse.from_dict(response.json())

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
) -> Response[Union[Error, SandboxConnectResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    sandbox_id: str,
    operation: ConnectSandboxFilesOperation,
    *,
    client: Union[AuthenticatedClient, Client],
    owner_id: Union[Unset, str] = UNSET,
    path: str,
) -> Response[Union[Error, SandboxConnectResponse]]:
    """Mint a connect token for a sandbox file transfer

     Mint a short-lived, capability-scoped connect token that authorizes a
    single file upload or download against the sandbox, and return the
    sandbox-proxy endpoint to invoke with it. The caller streams the file
    bytes directly to (or from) that endpoint with the token as a bearer
    credential. `application/octet-stream` carries a single file and
    `application/x-tar` a directory archive, with compression carried
    separately by `Content-Encoding: gzip` in either direction; directory
    downloads return `application/x-tar` with `Content-Encoding: gzip`. The
    token is bound to this sandbox, operation, and path, and expires
    shortly after issuance.

    Args:
        sandbox_id (str):  Example: sbx-1cd4gcph1rs3idesc73a2b2mg.
        operation (ConnectSandboxFilesOperation):
        owner_id (Union[Unset, str]):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, SandboxConnectResponse]]
    """

    kwargs = _get_kwargs(
        sandbox_id=sandbox_id,
        operation=operation,
        owner_id=owner_id,
        path=path,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    sandbox_id: str,
    operation: ConnectSandboxFilesOperation,
    *,
    client: Union[AuthenticatedClient, Client],
    owner_id: Union[Unset, str] = UNSET,
    path: str,
) -> Optional[Union[Error, SandboxConnectResponse]]:
    """Mint a connect token for a sandbox file transfer

     Mint a short-lived, capability-scoped connect token that authorizes a
    single file upload or download against the sandbox, and return the
    sandbox-proxy endpoint to invoke with it. The caller streams the file
    bytes directly to (or from) that endpoint with the token as a bearer
    credential. `application/octet-stream` carries a single file and
    `application/x-tar` a directory archive, with compression carried
    separately by `Content-Encoding: gzip` in either direction; directory
    downloads return `application/x-tar` with `Content-Encoding: gzip`. The
    token is bound to this sandbox, operation, and path, and expires
    shortly after issuance.

    Args:
        sandbox_id (str):  Example: sbx-1cd4gcph1rs3idesc73a2b2mg.
        operation (ConnectSandboxFilesOperation):
        owner_id (Union[Unset, str]):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, SandboxConnectResponse]
    """

    return sync_detailed(
        sandbox_id=sandbox_id,
        operation=operation,
        client=client,
        owner_id=owner_id,
        path=path,
    ).parsed


async def asyncio_detailed(
    sandbox_id: str,
    operation: ConnectSandboxFilesOperation,
    *,
    client: Union[AuthenticatedClient, Client],
    owner_id: Union[Unset, str] = UNSET,
    path: str,
) -> Response[Union[Error, SandboxConnectResponse]]:
    """Mint a connect token for a sandbox file transfer

     Mint a short-lived, capability-scoped connect token that authorizes a
    single file upload or download against the sandbox, and return the
    sandbox-proxy endpoint to invoke with it. The caller streams the file
    bytes directly to (or from) that endpoint with the token as a bearer
    credential. `application/octet-stream` carries a single file and
    `application/x-tar` a directory archive, with compression carried
    separately by `Content-Encoding: gzip` in either direction; directory
    downloads return `application/x-tar` with `Content-Encoding: gzip`. The
    token is bound to this sandbox, operation, and path, and expires
    shortly after issuance.

    Args:
        sandbox_id (str):  Example: sbx-1cd4gcph1rs3idesc73a2b2mg.
        operation (ConnectSandboxFilesOperation):
        owner_id (Union[Unset, str]):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, SandboxConnectResponse]]
    """

    kwargs = _get_kwargs(
        sandbox_id=sandbox_id,
        operation=operation,
        owner_id=owner_id,
        path=path,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    sandbox_id: str,
    operation: ConnectSandboxFilesOperation,
    *,
    client: Union[AuthenticatedClient, Client],
    owner_id: Union[Unset, str] = UNSET,
    path: str,
) -> Optional[Union[Error, SandboxConnectResponse]]:
    """Mint a connect token for a sandbox file transfer

     Mint a short-lived, capability-scoped connect token that authorizes a
    single file upload or download against the sandbox, and return the
    sandbox-proxy endpoint to invoke with it. The caller streams the file
    bytes directly to (or from) that endpoint with the token as a bearer
    credential. `application/octet-stream` carries a single file and
    `application/x-tar` a directory archive, with compression carried
    separately by `Content-Encoding: gzip` in either direction; directory
    downloads return `application/x-tar` with `Content-Encoding: gzip`. The
    token is bound to this sandbox, operation, and path, and expires
    shortly after issuance.

    Args:
        sandbox_id (str):  Example: sbx-1cd4gcph1rs3idesc73a2b2mg.
        operation (ConnectSandboxFilesOperation):
        owner_id (Union[Unset, str]):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, SandboxConnectResponse]
    """

    return (
        await asyncio_detailed(
            sandbox_id=sandbox_id,
            operation=operation,
            client=client,
            owner_id=owner_id,
            path=path,
        )
    ).parsed
