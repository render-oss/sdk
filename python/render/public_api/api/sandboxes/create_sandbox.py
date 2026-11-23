from http import HTTPStatus
from typing import Any

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.sandbox_detail_response import SandboxDetailResponse
from ...models.sandbox_post import SandboxPOST
from ...types import Response


def _get_kwargs(
    *,
    body: SandboxPOST,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/sandboxes",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Error | SandboxDetailResponse | None:
    if response.status_code == 201:
        response_201 = SandboxDetailResponse.from_dict(response.json())

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
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Response[Error | SandboxDetailResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: SandboxPOST,
) -> Response[Error | SandboxDetailResponse]:
    """Create sandbox

     Create a sandbox and return its initial state. The sandbox might still be starting when the response
    is returned. To use a saved snapshot or custom image, provide `snapshotId`, `snapshotName`,
    `buildId`, or `buildName`.

    Args:
        body (SandboxPOST): The sandbox to create, including its compute plan, network policy, and
            optional source build or snapshot.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SandboxDetailResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: SandboxPOST,
) -> Error | SandboxDetailResponse | None:
    """Create sandbox

     Create a sandbox and return its initial state. The sandbox might still be starting when the response
    is returned. To use a saved snapshot or custom image, provide `snapshotId`, `snapshotName`,
    `buildId`, or `buildName`.

    Args:
        body (SandboxPOST): The sandbox to create, including its compute plan, network policy, and
            optional source build or snapshot.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SandboxDetailResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: SandboxPOST,
) -> Response[Error | SandboxDetailResponse]:
    """Create sandbox

     Create a sandbox and return its initial state. The sandbox might still be starting when the response
    is returned. To use a saved snapshot or custom image, provide `snapshotId`, `snapshotName`,
    `buildId`, or `buildName`.

    Args:
        body (SandboxPOST): The sandbox to create, including its compute plan, network policy, and
            optional source build or snapshot.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SandboxDetailResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: SandboxPOST,
) -> Error | SandboxDetailResponse | None:
    """Create sandbox

     Create a sandbox and return its initial state. The sandbox might still be starting when the response
    is returned. To use a saved snapshot or custom image, provide `snapshotId`, `snapshotName`,
    `buildId`, or `buildName`.

    Args:
        body (SandboxPOST): The sandbox to create, including its compute plan, network policy, and
            optional source build or snapshot.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SandboxDetailResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
