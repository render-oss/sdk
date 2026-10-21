from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.sandbox_credential import SandboxCredential
from ...models.sandbox_credential_update import SandboxCredentialUpdate
from ...types import Response


def _get_kwargs(
    sandbox_group_id: str,
    credential_id: str,
    *,
    body: SandboxCredentialUpdate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": f"/sandbox-groups/{sandbox_group_id}/credentials/{credential_id}",
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
    body: SandboxCredentialUpdate,
) -> Response[Union[Error, SandboxCredential]]:
    """Update sandbox group credential

     Admins may update configuration. Developers may update injection, method/path
    filters, and enabled state; destination or value changes require an admin.
    Assigning a value creates a new version; omitting it preserves the value.
    Other omitted fields are preserved; empty methods or paths arrays clear their
    filters. The group's serialized current credentials must
    remain within 200 KiB (204800 bytes). A successful response means desired
    state was saved; runtime reconciliation may still be pending.

    Args:
        sandbox_group_id (str):  Example: sbg-cph1rs3idesc73a2b2mg.
        credential_id (str): Caller-supplied URL-safe name, unique within the sandbox group. The
            names
            `.` and `..` and the prefix `rnd-` are reserved. IDs are case-sensitive.
             Example: my-inference-key.
        body (SandboxCredentialUpdate): Omitted fields retain their existing values. Empty methods
            or paths arrays
            clear those filters. Developers may update injection, methods, paths, and
            enabled state. Changing the destination requires an admin and otherwise
            returns 403. Overwriting a value requires an admin; omitting it has no effect.
            Changes to routing, injection, or enabled state create a new configuration version.
            Overwriting the value also creates a version, even when the value is unchanged.
            The credential ID is immutable.

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
    body: SandboxCredentialUpdate,
) -> Optional[Union[Error, SandboxCredential]]:
    """Update sandbox group credential

     Admins may update configuration. Developers may update injection, method/path
    filters, and enabled state; destination or value changes require an admin.
    Assigning a value creates a new version; omitting it preserves the value.
    Other omitted fields are preserved; empty methods or paths arrays clear their
    filters. The group's serialized current credentials must
    remain within 200 KiB (204800 bytes). A successful response means desired
    state was saved; runtime reconciliation may still be pending.

    Args:
        sandbox_group_id (str):  Example: sbg-cph1rs3idesc73a2b2mg.
        credential_id (str): Caller-supplied URL-safe name, unique within the sandbox group. The
            names
            `.` and `..` and the prefix `rnd-` are reserved. IDs are case-sensitive.
             Example: my-inference-key.
        body (SandboxCredentialUpdate): Omitted fields retain their existing values. Empty methods
            or paths arrays
            clear those filters. Developers may update injection, methods, paths, and
            enabled state. Changing the destination requires an admin and otherwise
            returns 403. Overwriting a value requires an admin; omitting it has no effect.
            Changes to routing, injection, or enabled state create a new configuration version.
            Overwriting the value also creates a version, even when the value is unchanged.
            The credential ID is immutable.

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
    body: SandboxCredentialUpdate,
) -> Response[Union[Error, SandboxCredential]]:
    """Update sandbox group credential

     Admins may update configuration. Developers may update injection, method/path
    filters, and enabled state; destination or value changes require an admin.
    Assigning a value creates a new version; omitting it preserves the value.
    Other omitted fields are preserved; empty methods or paths arrays clear their
    filters. The group's serialized current credentials must
    remain within 200 KiB (204800 bytes). A successful response means desired
    state was saved; runtime reconciliation may still be pending.

    Args:
        sandbox_group_id (str):  Example: sbg-cph1rs3idesc73a2b2mg.
        credential_id (str): Caller-supplied URL-safe name, unique within the sandbox group. The
            names
            `.` and `..` and the prefix `rnd-` are reserved. IDs are case-sensitive.
             Example: my-inference-key.
        body (SandboxCredentialUpdate): Omitted fields retain their existing values. Empty methods
            or paths arrays
            clear those filters. Developers may update injection, methods, paths, and
            enabled state. Changing the destination requires an admin and otherwise
            returns 403. Overwriting a value requires an admin; omitting it has no effect.
            Changes to routing, injection, or enabled state create a new configuration version.
            Overwriting the value also creates a version, even when the value is unchanged.
            The credential ID is immutable.

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
    body: SandboxCredentialUpdate,
) -> Optional[Union[Error, SandboxCredential]]:
    """Update sandbox group credential

     Admins may update configuration. Developers may update injection, method/path
    filters, and enabled state; destination or value changes require an admin.
    Assigning a value creates a new version; omitting it preserves the value.
    Other omitted fields are preserved; empty methods or paths arrays clear their
    filters. The group's serialized current credentials must
    remain within 200 KiB (204800 bytes). A successful response means desired
    state was saved; runtime reconciliation may still be pending.

    Args:
        sandbox_group_id (str):  Example: sbg-cph1rs3idesc73a2b2mg.
        credential_id (str): Caller-supplied URL-safe name, unique within the sandbox group. The
            names
            `.` and `..` and the prefix `rnd-` are reserved. IDs are case-sensitive.
             Example: my-inference-key.
        body (SandboxCredentialUpdate): Omitted fields retain their existing values. Empty methods
            or paths arrays
            clear those filters. Developers may update injection, methods, paths, and
            enabled state. Changing the destination requires an admin and otherwise
            returns 403. Overwriting a value requires an admin; omitting it has no effect.
            Changes to routing, injection, or enabled state create a new configuration version.
            Overwriting the value also creates a version, even when the value is unchanged.
            The credential ID is immutable.

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
