from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.sandbox_credential import SandboxCredential
from ...models.sandbox_credential_create import SandboxCredentialCreate
from ...types import Response


def _get_kwargs(
    sandbox_group_id: str,
    *,
    body: SandboxCredentialCreate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/sandbox-groups/{sandbox_group_id}/credentials".format(
            sandbox_group_id=quote(str(sandbox_group_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Error | SandboxCredential | None:
    if response.status_code == 201:
        response_201 = SandboxCredential.from_dict(response.json())

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
) -> Response[Error | SandboxCredential]:
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
    body: SandboxCredentialCreate,
) -> Response[Error | SandboxCredential]:
    """Create sandbox group credential

     Configure a credential for injection into matching outbound HTTPS requests from sandboxes in this
    group. Requires an admin. You assign the credential ID.

    Each group supports up to 25 credentials. Current credential settings and secret values have a
    combined serialized size limit of 200 KiB (204800 bytes). Render retains the current configuration
    and three distinct prior configurations per credential, with a total storage limit of 1 MiB
    including version metadata.

    The response confirms the configuration was saved. It does not confirm that credential injection is
    active for a particular sandbox.

    Args:
        sandbox_group_id (str): The ID of the sandbox group. Example: sbg-cph1rs3idesc73a2b2mg.
        body (SandboxCredentialCreate): The credential configuration to create, including request
            matching and injection settings.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SandboxCredential]
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
    body: SandboxCredentialCreate,
) -> Error | SandboxCredential | None:
    """Create sandbox group credential

     Configure a credential for injection into matching outbound HTTPS requests from sandboxes in this
    group. Requires an admin. You assign the credential ID.

    Each group supports up to 25 credentials. Current credential settings and secret values have a
    combined serialized size limit of 200 KiB (204800 bytes). Render retains the current configuration
    and three distinct prior configurations per credential, with a total storage limit of 1 MiB
    including version metadata.

    The response confirms the configuration was saved. It does not confirm that credential injection is
    active for a particular sandbox.

    Args:
        sandbox_group_id (str): The ID of the sandbox group. Example: sbg-cph1rs3idesc73a2b2mg.
        body (SandboxCredentialCreate): The credential configuration to create, including request
            matching and injection settings.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SandboxCredential
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
    body: SandboxCredentialCreate,
) -> Response[Error | SandboxCredential]:
    """Create sandbox group credential

     Configure a credential for injection into matching outbound HTTPS requests from sandboxes in this
    group. Requires an admin. You assign the credential ID.

    Each group supports up to 25 credentials. Current credential settings and secret values have a
    combined serialized size limit of 200 KiB (204800 bytes). Render retains the current configuration
    and three distinct prior configurations per credential, with a total storage limit of 1 MiB
    including version metadata.

    The response confirms the configuration was saved. It does not confirm that credential injection is
    active for a particular sandbox.

    Args:
        sandbox_group_id (str): The ID of the sandbox group. Example: sbg-cph1rs3idesc73a2b2mg.
        body (SandboxCredentialCreate): The credential configuration to create, including request
            matching and injection settings.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SandboxCredential]
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
    body: SandboxCredentialCreate,
) -> Error | SandboxCredential | None:
    """Create sandbox group credential

     Configure a credential for injection into matching outbound HTTPS requests from sandboxes in this
    group. Requires an admin. You assign the credential ID.

    Each group supports up to 25 credentials. Current credential settings and secret values have a
    combined serialized size limit of 200 KiB (204800 bytes). Render retains the current configuration
    and three distinct prior configurations per credential, with a total storage limit of 1 MiB
    including version metadata.

    The response confirms the configuration was saved. It does not confirm that credential injection is
    active for a particular sandbox.

    Args:
        sandbox_group_id (str): The ID of the sandbox group. Example: sbg-cph1rs3idesc73a2b2mg.
        body (SandboxCredentialCreate): The credential configuration to create, including request
            matching and injection settings.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SandboxCredential
    """

    return (
        await asyncio_detailed(
            sandbox_group_id=sandbox_group_id,
            client=client,
            body=body,
        )
    ).parsed
