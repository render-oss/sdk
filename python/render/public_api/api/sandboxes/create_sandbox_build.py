from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.sandbox_build import SandboxBuild
from ...models.sandbox_build_post import SandboxBuildPOST
from ...types import Response


def _get_kwargs(
    sandbox_group_id: str,
    *,
    body: SandboxBuildPOST,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/sandbox-groups/{sandbox_group_id}/builds".format(
            sandbox_group_id=quote(str(sandbox_group_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx2.Response) -> Error | SandboxBuild | None:
    if response.status_code == 201:
        response_201 = SandboxBuild.from_dict(response.json())

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
) -> Response[Error | SandboxBuild]:
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
    body: SandboxBuildPOST,
) -> Response[Error | SandboxBuild]:
    """Create sandbox build

     Start converting an OCI container image into an image that sandboxes can use. New builds run
    asynchronously. Retrieve the build until its status is `succeeded` or `failed`. After it succeeds,
    provide its ID as `buildId` when creating a sandbox.

    If the group already has a pending, running, or succeeded build for the same name and image digest,
    Render returns that build. Retrying a failed build starts a new build.

    Args:
        sandbox_group_id (str): The ID of the sandbox group. Example: sbg-cph1rs3idesc73a2b2mg.
        body (SandboxBuildPOST): The source container image and settings for the sandbox build.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SandboxBuild]
    """

    kwargs = _get_kwargs(
        sandbox_group_id=sandbox_group_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    sandbox_group_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: SandboxBuildPOST,
) -> Error | SandboxBuild | None:
    """Create sandbox build

     Start converting an OCI container image into an image that sandboxes can use. New builds run
    asynchronously. Retrieve the build until its status is `succeeded` or `failed`. After it succeeds,
    provide its ID as `buildId` when creating a sandbox.

    If the group already has a pending, running, or succeeded build for the same name and image digest,
    Render returns that build. Retrying a failed build starts a new build.

    Args:
        sandbox_group_id (str): The ID of the sandbox group. Example: sbg-cph1rs3idesc73a2b2mg.
        body (SandboxBuildPOST): The source container image and settings for the sandbox build.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SandboxBuild
    """

    return sync_detailed(
        sandbox_group_id=sandbox_group_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    sandbox_group_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: SandboxBuildPOST,
) -> Response[Error | SandboxBuild]:
    """Create sandbox build

     Start converting an OCI container image into an image that sandboxes can use. New builds run
    asynchronously. Retrieve the build until its status is `succeeded` or `failed`. After it succeeds,
    provide its ID as `buildId` when creating a sandbox.

    If the group already has a pending, running, or succeeded build for the same name and image digest,
    Render returns that build. Retrying a failed build starts a new build.

    Args:
        sandbox_group_id (str): The ID of the sandbox group. Example: sbg-cph1rs3idesc73a2b2mg.
        body (SandboxBuildPOST): The source container image and settings for the sandbox build.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SandboxBuild]
    """

    kwargs = _get_kwargs(
        sandbox_group_id=sandbox_group_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    sandbox_group_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: SandboxBuildPOST,
) -> Error | SandboxBuild | None:
    """Create sandbox build

     Start converting an OCI container image into an image that sandboxes can use. New builds run
    asynchronously. Retrieve the build until its status is `succeeded` or `failed`. After it succeeds,
    provide its ID as `buildId` when creating a sandbox.

    If the group already has a pending, running, or succeeded build for the same name and image digest,
    Render returns that build. Retrying a failed build starts a new build.

    Args:
        sandbox_group_id (str): The ID of the sandbox group. Example: sbg-cph1rs3idesc73a2b2mg.
        body (SandboxBuildPOST): The source container image and settings for the sandbox build.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SandboxBuild
    """

    return (
        await asyncio_detailed(
            sandbox_group_id=sandbox_group_id,
            client=client,
            body=body,
        )
    ).parsed
