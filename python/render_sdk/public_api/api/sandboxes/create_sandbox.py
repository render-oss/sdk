from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_sandbox_accept import CreateSandboxAccept
from ...models.error import Error
from ...models.sandbox_post import SandboxPOST
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: SandboxPOST,
    idempotency_key: Union[Unset, UUID] = UNSET,
    accept: Union[Unset, CreateSandboxAccept] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    if not isinstance(accept, Unset):
        headers["Accept"] = str(accept)

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/sandboxes",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, str]]:
    if response.status_code == 200:
        response_200 = response.text
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
) -> Response[Union[Error, str]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: SandboxPOST,
    idempotency_key: Union[Unset, UUID] = UNSET,
    accept: Union[Unset, CreateSandboxAccept] = UNSET,
) -> Response[Union[Error, str]]:
    """Create sandbox

     Create a sandbox. Responds with a server-sent event stream that stays open for the
    sandbox's lifetime. The stream emits `status` events on every state transition and
    `warning` advisories before termination. The stream closes when the sandbox reaches
    `terminated` or `errored`.

    Supply an `Idempotency-Key` header (UUID v4 recommended) to safely retry on network
    error. A duplicate key within the retry window returns the existing sandbox's SSE
    stream, replaying events from the current state.

    Args:
        idempotency_key (Union[Unset, UUID]):
        accept (Union[Unset, CreateSandboxAccept]):
        body (SandboxPOST):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, str]]
    """

    kwargs = _get_kwargs(
        body=body,
        idempotency_key=idempotency_key,
        accept=accept,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: SandboxPOST,
    idempotency_key: Union[Unset, UUID] = UNSET,
    accept: Union[Unset, CreateSandboxAccept] = UNSET,
) -> Optional[Union[Error, str]]:
    """Create sandbox

     Create a sandbox. Responds with a server-sent event stream that stays open for the
    sandbox's lifetime. The stream emits `status` events on every state transition and
    `warning` advisories before termination. The stream closes when the sandbox reaches
    `terminated` or `errored`.

    Supply an `Idempotency-Key` header (UUID v4 recommended) to safely retry on network
    error. A duplicate key within the retry window returns the existing sandbox's SSE
    stream, replaying events from the current state.

    Args:
        idempotency_key (Union[Unset, UUID]):
        accept (Union[Unset, CreateSandboxAccept]):
        body (SandboxPOST):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, str]
    """

    return sync_detailed(
        client=client,
        body=body,
        idempotency_key=idempotency_key,
        accept=accept,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: SandboxPOST,
    idempotency_key: Union[Unset, UUID] = UNSET,
    accept: Union[Unset, CreateSandboxAccept] = UNSET,
) -> Response[Union[Error, str]]:
    """Create sandbox

     Create a sandbox. Responds with a server-sent event stream that stays open for the
    sandbox's lifetime. The stream emits `status` events on every state transition and
    `warning` advisories before termination. The stream closes when the sandbox reaches
    `terminated` or `errored`.

    Supply an `Idempotency-Key` header (UUID v4 recommended) to safely retry on network
    error. A duplicate key within the retry window returns the existing sandbox's SSE
    stream, replaying events from the current state.

    Args:
        idempotency_key (Union[Unset, UUID]):
        accept (Union[Unset, CreateSandboxAccept]):
        body (SandboxPOST):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, str]]
    """

    kwargs = _get_kwargs(
        body=body,
        idempotency_key=idempotency_key,
        accept=accept,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: SandboxPOST,
    idempotency_key: Union[Unset, UUID] = UNSET,
    accept: Union[Unset, CreateSandboxAccept] = UNSET,
) -> Optional[Union[Error, str]]:
    """Create sandbox

     Create a sandbox. Responds with a server-sent event stream that stays open for the
    sandbox's lifetime. The stream emits `status` events on every state transition and
    `warning` advisories before termination. The stream closes when the sandbox reaches
    `terminated` or `errored`.

    Supply an `Idempotency-Key` header (UUID v4 recommended) to safely retry on network
    error. A duplicate key within the retry window returns the existing sandbox's SSE
    stream, replaying events from the current state.

    Args:
        idempotency_key (Union[Unset, UUID]):
        accept (Union[Unset, CreateSandboxAccept]):
        body (SandboxPOST):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, str]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            idempotency_key=idempotency_key,
            accept=accept,
        )
    ).parsed
