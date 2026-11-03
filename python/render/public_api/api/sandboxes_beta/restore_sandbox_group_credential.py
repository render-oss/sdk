from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.sandbox_credential import SandboxCredential
from ...models.sandbox_credential_restore import SandboxCredentialRestore
from ...types import Response


def _get_kwargs(
    sandbox_group_id: str,
    credential_id: str,
    *,
    body: SandboxCredentialRestore,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/sandbox-groups/{sandbox_group_id}/credentials/{credential_id}/restore",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, SandboxCredential]]:
    if response.status_code == 200:
        response_200 = SandboxCredential.from_dict(response.json())

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
) -> Response[Union[Error, SandboxCredential]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    sandbox_group_id: str,
    credential_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: SandboxCredentialRestore,
) -> Response[Union[Error, SandboxCredential]]:
    """Restore sandbox credential configuration

     Admin-only. Creates a new current revision from the routing
    configuration, injection configuration, and secret value of a retained
    version. The new revision has an increasing version ID, the restoring
    identity and timestamp, the same fingerprint as the source, and
    restoredFromVersionId identifying the source. Each distinct
    configuration is stored once by fingerprint. The current and three most
    recently active prior configurations are retained. Evicting a
    configuration removes all version metadata referring to it. Values are
    never returned. A temporary synchronization conflict returns 429.

    Args:
        sandbox_group_id (str):  Example: sbg-cph1rs3idesc73a2b2mg.
        credential_id (str): Caller-supplied URL-safe name, unique within the sandbox group. The
            names
            `.` and `..` and the prefix `rnd-` are reserved. IDs are case-sensitive.
             Example: my-inference-key.
        body (SandboxCredentialRestore):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, SandboxCredential]]
    """

    kwargs = _get_kwargs(
        sandbox_group_id=sandbox_group_id,
        credential_id=credential_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    sandbox_group_id: str,
    credential_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: SandboxCredentialRestore,
) -> Optional[Union[Error, SandboxCredential]]:
    """Restore sandbox credential configuration

     Admin-only. Creates a new current revision from the routing
    configuration, injection configuration, and secret value of a retained
    version. The new revision has an increasing version ID, the restoring
    identity and timestamp, the same fingerprint as the source, and
    restoredFromVersionId identifying the source. Each distinct
    configuration is stored once by fingerprint. The current and three most
    recently active prior configurations are retained. Evicting a
    configuration removes all version metadata referring to it. Values are
    never returned. A temporary synchronization conflict returns 429.

    Args:
        sandbox_group_id (str):  Example: sbg-cph1rs3idesc73a2b2mg.
        credential_id (str): Caller-supplied URL-safe name, unique within the sandbox group. The
            names
            `.` and `..` and the prefix `rnd-` are reserved. IDs are case-sensitive.
             Example: my-inference-key.
        body (SandboxCredentialRestore):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, SandboxCredential]
    """

    return sync_detailed(
        sandbox_group_id=sandbox_group_id,
        credential_id=credential_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    sandbox_group_id: str,
    credential_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: SandboxCredentialRestore,
) -> Response[Union[Error, SandboxCredential]]:
    """Restore sandbox credential configuration

     Admin-only. Creates a new current revision from the routing
    configuration, injection configuration, and secret value of a retained
    version. The new revision has an increasing version ID, the restoring
    identity and timestamp, the same fingerprint as the source, and
    restoredFromVersionId identifying the source. Each distinct
    configuration is stored once by fingerprint. The current and three most
    recently active prior configurations are retained. Evicting a
    configuration removes all version metadata referring to it. Values are
    never returned. A temporary synchronization conflict returns 429.

    Args:
        sandbox_group_id (str):  Example: sbg-cph1rs3idesc73a2b2mg.
        credential_id (str): Caller-supplied URL-safe name, unique within the sandbox group. The
            names
            `.` and `..` and the prefix `rnd-` are reserved. IDs are case-sensitive.
             Example: my-inference-key.
        body (SandboxCredentialRestore):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, SandboxCredential]]
    """

    kwargs = _get_kwargs(
        sandbox_group_id=sandbox_group_id,
        credential_id=credential_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    sandbox_group_id: str,
    credential_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: SandboxCredentialRestore,
) -> Optional[Union[Error, SandboxCredential]]:
    """Restore sandbox credential configuration

     Admin-only. Creates a new current revision from the routing
    configuration, injection configuration, and secret value of a retained
    version. The new revision has an increasing version ID, the restoring
    identity and timestamp, the same fingerprint as the source, and
    restoredFromVersionId identifying the source. Each distinct
    configuration is stored once by fingerprint. The current and three most
    recently active prior configurations are retained. Evicting a
    configuration removes all version metadata referring to it. Values are
    never returned. A temporary synchronization conflict returns 429.

    Args:
        sandbox_group_id (str):  Example: sbg-cph1rs3idesc73a2b2mg.
        credential_id (str): Caller-supplied URL-safe name, unique within the sandbox group. The
            names
            `.` and `..` and the prefix `rnd-` are reserved. IDs are case-sensitive.
             Example: my-inference-key.
        body (SandboxCredentialRestore):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, SandboxCredential]
    """

    return (
        await asyncio_detailed(
            sandbox_group_id=sandbox_group_id,
            credential_id=credential_id,
            client=client,
            body=body,
        )
    ).parsed
