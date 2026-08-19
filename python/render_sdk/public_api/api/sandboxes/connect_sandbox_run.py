from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.connect_sandbox_run_operation import ConnectSandboxRunOperation
from ...models.error import Error
from ...models.sandbox_connect_request import SandboxConnectRequest
from ...models.sandbox_connect_response import SandboxConnectResponse
from ...types import UNSET, Response


def _get_kwargs(
    sandbox_id: str,
    operation: ConnectSandboxRunOperation,
    *,
    body: SandboxConnectRequest,
    owner_id: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["ownerId"] = owner_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/sandboxes/{sandbox_id}/runs/{operation}/token",
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
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
    operation: ConnectSandboxRunOperation,
    *,
    client: Union[AuthenticatedClient, Client],
    body: SandboxConnectRequest,
    owner_id: str,
) -> Response[Union[Error, SandboxConnectResponse]]:
    """Create a connect token for a sandbox run

     Mint a short-lived, capability-scoped connect token that authorizes a
    single run operation against the specified sandbox. The response contains
    the sandbox URI where the caller sends the command with the token as a bearer credential.

    Args:
        sandbox_id (str):  Example: sbx-1cd4gcph1rs3idesc73a2b2mg.
        operation (ConnectSandboxRunOperation):
        owner_id (str):
        body (SandboxConnectRequest): Optional body when minting a run connect token. `command` is
            stored on
            the exec timeline (truncated to 4KB); the full command is still sent
            to the sandbox proxy when executing.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, SandboxConnectResponse]]
    """

    kwargs = _get_kwargs(
        sandbox_id=sandbox_id,
        operation=operation,
        body=body,
        owner_id=owner_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    sandbox_id: str,
    operation: ConnectSandboxRunOperation,
    *,
    client: Union[AuthenticatedClient, Client],
    body: SandboxConnectRequest,
    owner_id: str,
) -> Optional[Union[Error, SandboxConnectResponse]]:
    """Create a connect token for a sandbox run

     Mint a short-lived, capability-scoped connect token that authorizes a
    single run operation against the specified sandbox. The response contains
    the sandbox URI where the caller sends the command with the token as a bearer credential.

    Args:
        sandbox_id (str):  Example: sbx-1cd4gcph1rs3idesc73a2b2mg.
        operation (ConnectSandboxRunOperation):
        owner_id (str):
        body (SandboxConnectRequest): Optional body when minting a run connect token. `command` is
            stored on
            the exec timeline (truncated to 4KB); the full command is still sent
            to the sandbox proxy when executing.

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
        body=body,
        owner_id=owner_id,
    ).parsed


async def asyncio_detailed(
    sandbox_id: str,
    operation: ConnectSandboxRunOperation,
    *,
    client: Union[AuthenticatedClient, Client],
    body: SandboxConnectRequest,
    owner_id: str,
) -> Response[Union[Error, SandboxConnectResponse]]:
    """Create a connect token for a sandbox run

     Mint a short-lived, capability-scoped connect token that authorizes a
    single run operation against the specified sandbox. The response contains
    the sandbox URI where the caller sends the command with the token as a bearer credential.

    Args:
        sandbox_id (str):  Example: sbx-1cd4gcph1rs3idesc73a2b2mg.
        operation (ConnectSandboxRunOperation):
        owner_id (str):
        body (SandboxConnectRequest): Optional body when minting a run connect token. `command` is
            stored on
            the exec timeline (truncated to 4KB); the full command is still sent
            to the sandbox proxy when executing.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, SandboxConnectResponse]]
    """

    kwargs = _get_kwargs(
        sandbox_id=sandbox_id,
        operation=operation,
        body=body,
        owner_id=owner_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    sandbox_id: str,
    operation: ConnectSandboxRunOperation,
    *,
    client: Union[AuthenticatedClient, Client],
    body: SandboxConnectRequest,
    owner_id: str,
) -> Optional[Union[Error, SandboxConnectResponse]]:
    """Create a connect token for a sandbox run

     Mint a short-lived, capability-scoped connect token that authorizes a
    single run operation against the specified sandbox. The response contains
    the sandbox URI where the caller sends the command with the token as a bearer credential.

    Args:
        sandbox_id (str):  Example: sbx-1cd4gcph1rs3idesc73a2b2mg.
        operation (ConnectSandboxRunOperation):
        owner_id (str):
        body (SandboxConnectRequest): Optional body when minting a run connect token. `command` is
            stored on
            the exec timeline (truncated to 4KB); the full command is still sent
            to the sandbox proxy when executing.

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
            body=body,
            owner_id=owner_id,
        )
    ).parsed
