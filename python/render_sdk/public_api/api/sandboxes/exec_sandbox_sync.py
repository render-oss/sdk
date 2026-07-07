from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.exec_sandbox_sync_accept import ExecSandboxSyncAccept
from ...models.sandbox_exec_sync_request import SandboxExecSyncRequest
from ...models.sandbox_exec_sync_response import SandboxExecSyncResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    sandbox_id: str,
    *,
    body: SandboxExecSyncRequest,
    owner_id: str,
    accept: Union[Unset, ExecSandboxSyncAccept] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(accept, Unset):
        headers["Accept"] = str(accept)

    params: dict[str, Any] = {}

    params["ownerId"] = owner_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/sandboxes/{sandbox_id}/exec",
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, SandboxExecSyncResponse]]:
    if response.status_code == 200:
        response_200 = SandboxExecSyncResponse.from_dict(response.json())

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
) -> Response[Union[Error, SandboxExecSyncResponse]]:
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
    body: SandboxExecSyncRequest,
    owner_id: str,
    accept: Union[Unset, ExecSandboxSyncAccept] = UNSET,
) -> Response[Union[Error, SandboxExecSyncResponse]]:
    """Execute command in sandbox synchronously

     Run a single command in a running sandbox. By default, blocks until the
    command exits and returns stdout, stderr, and exit code in one JSON
    response.

    To receive stdout and stderr as they are produced, set
    `Accept: text/event-stream`. Streaming responses use finite
    server-sent events and end with either an `exit` event or an `error`
    event.

    Args:
        sandbox_id (str):  Example: sbx-cph1rs3idesc73a2b2mg.
        owner_id (str):
        accept (Union[Unset, ExecSandboxSyncAccept]):
        body (SandboxExecSyncRequest): Body of the synchronous exec endpoint.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, SandboxExecSyncResponse]]
    """

    kwargs = _get_kwargs(
        sandbox_id=sandbox_id,
        body=body,
        owner_id=owner_id,
        accept=accept,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    sandbox_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: SandboxExecSyncRequest,
    owner_id: str,
    accept: Union[Unset, ExecSandboxSyncAccept] = UNSET,
) -> Optional[Union[Error, SandboxExecSyncResponse]]:
    """Execute command in sandbox synchronously

     Run a single command in a running sandbox. By default, blocks until the
    command exits and returns stdout, stderr, and exit code in one JSON
    response.

    To receive stdout and stderr as they are produced, set
    `Accept: text/event-stream`. Streaming responses use finite
    server-sent events and end with either an `exit` event or an `error`
    event.

    Args:
        sandbox_id (str):  Example: sbx-cph1rs3idesc73a2b2mg.
        owner_id (str):
        accept (Union[Unset, ExecSandboxSyncAccept]):
        body (SandboxExecSyncRequest): Body of the synchronous exec endpoint.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, SandboxExecSyncResponse]
    """

    return sync_detailed(
        sandbox_id=sandbox_id,
        client=client,
        body=body,
        owner_id=owner_id,
        accept=accept,
    ).parsed


async def asyncio_detailed(
    sandbox_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: SandboxExecSyncRequest,
    owner_id: str,
    accept: Union[Unset, ExecSandboxSyncAccept] = UNSET,
) -> Response[Union[Error, SandboxExecSyncResponse]]:
    """Execute command in sandbox synchronously

     Run a single command in a running sandbox. By default, blocks until the
    command exits and returns stdout, stderr, and exit code in one JSON
    response.

    To receive stdout and stderr as they are produced, set
    `Accept: text/event-stream`. Streaming responses use finite
    server-sent events and end with either an `exit` event or an `error`
    event.

    Args:
        sandbox_id (str):  Example: sbx-cph1rs3idesc73a2b2mg.
        owner_id (str):
        accept (Union[Unset, ExecSandboxSyncAccept]):
        body (SandboxExecSyncRequest): Body of the synchronous exec endpoint.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, SandboxExecSyncResponse]]
    """

    kwargs = _get_kwargs(
        sandbox_id=sandbox_id,
        body=body,
        owner_id=owner_id,
        accept=accept,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    sandbox_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: SandboxExecSyncRequest,
    owner_id: str,
    accept: Union[Unset, ExecSandboxSyncAccept] = UNSET,
) -> Optional[Union[Error, SandboxExecSyncResponse]]:
    """Execute command in sandbox synchronously

     Run a single command in a running sandbox. By default, blocks until the
    command exits and returns stdout, stderr, and exit code in one JSON
    response.

    To receive stdout and stderr as they are produced, set
    `Accept: text/event-stream`. Streaming responses use finite
    server-sent events and end with either an `exit` event or an `error`
    event.

    Args:
        sandbox_id (str):  Example: sbx-cph1rs3idesc73a2b2mg.
        owner_id (str):
        accept (Union[Unset, ExecSandboxSyncAccept]):
        body (SandboxExecSyncRequest): Body of the synchronous exec endpoint.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, SandboxExecSyncResponse]
    """

    return (
        await asyncio_detailed(
            sandbox_id=sandbox_id,
            client=client,
            body=body,
            owner_id=owner_id,
            accept=accept,
        )
    ).parsed
