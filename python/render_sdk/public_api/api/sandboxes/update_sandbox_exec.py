from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.sandbox_exec_update_request import SandboxExecUpdateRequest
from ...models.sandbox_exec_update_response import SandboxExecUpdateResponse
from ...types import UNSET, Response


def _get_kwargs(
    sandbox_id: str,
    exec_id: str,
    *,
    body: SandboxExecUpdateRequest,
    owner_id: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["ownerId"] = owner_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/sandboxes/{sandbox_id}/execs/{exec_id}/status",
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, SandboxExecUpdateResponse]]:
    if response.status_code == 200:
        response_200 = SandboxExecUpdateResponse.from_dict(response.json())

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
) -> Response[Union[Error, SandboxExecUpdateResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    sandbox_id: str,
    exec_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: SandboxExecUpdateRequest,
    owner_id: str,
) -> Response[Union[Error, SandboxExecUpdateResponse]]:
    """Update sandbox execution

     Record the client-observed exit code for a previously minted sandbox
    execution. Call after the proxy run completes (sync response or closing
    SSE frame). Command text is recorded at token mint time, not here.

    Args:
        sandbox_id (str):  Example: sbx-1cd4gcph1rs3idesc73a2b2mg.
        exec_id (str):
        owner_id (str):
        body (SandboxExecUpdateRequest): Client-reported completion of a sandbox execution.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, SandboxExecUpdateResponse]]
    """

    kwargs = _get_kwargs(
        sandbox_id=sandbox_id,
        exec_id=exec_id,
        body=body,
        owner_id=owner_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    sandbox_id: str,
    exec_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: SandboxExecUpdateRequest,
    owner_id: str,
) -> Optional[Union[Error, SandboxExecUpdateResponse]]:
    """Update sandbox execution

     Record the client-observed exit code for a previously minted sandbox
    execution. Call after the proxy run completes (sync response or closing
    SSE frame). Command text is recorded at token mint time, not here.

    Args:
        sandbox_id (str):  Example: sbx-1cd4gcph1rs3idesc73a2b2mg.
        exec_id (str):
        owner_id (str):
        body (SandboxExecUpdateRequest): Client-reported completion of a sandbox execution.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, SandboxExecUpdateResponse]
    """

    return sync_detailed(
        sandbox_id=sandbox_id,
        exec_id=exec_id,
        client=client,
        body=body,
        owner_id=owner_id,
    ).parsed


async def asyncio_detailed(
    sandbox_id: str,
    exec_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: SandboxExecUpdateRequest,
    owner_id: str,
) -> Response[Union[Error, SandboxExecUpdateResponse]]:
    """Update sandbox execution

     Record the client-observed exit code for a previously minted sandbox
    execution. Call after the proxy run completes (sync response or closing
    SSE frame). Command text is recorded at token mint time, not here.

    Args:
        sandbox_id (str):  Example: sbx-1cd4gcph1rs3idesc73a2b2mg.
        exec_id (str):
        owner_id (str):
        body (SandboxExecUpdateRequest): Client-reported completion of a sandbox execution.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, SandboxExecUpdateResponse]]
    """

    kwargs = _get_kwargs(
        sandbox_id=sandbox_id,
        exec_id=exec_id,
        body=body,
        owner_id=owner_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    sandbox_id: str,
    exec_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: SandboxExecUpdateRequest,
    owner_id: str,
) -> Optional[Union[Error, SandboxExecUpdateResponse]]:
    """Update sandbox execution

     Record the client-observed exit code for a previously minted sandbox
    execution. Call after the proxy run completes (sync response or closing
    SSE frame). Command text is recorded at token mint time, not here.

    Args:
        sandbox_id (str):  Example: sbx-1cd4gcph1rs3idesc73a2b2mg.
        exec_id (str):
        owner_id (str):
        body (SandboxExecUpdateRequest): Client-reported completion of a sandbox execution.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, SandboxExecUpdateResponse]
    """

    return (
        await asyncio_detailed(
            sandbox_id=sandbox_id,
            exec_id=exec_id,
            client=client,
            body=body,
            owner_id=owner_id,
        )
    ).parsed
