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

     Restore a retained credential version, including its routing settings, injection settings, and
    secret value, as a new current version. Requires an admin.

    The new version has a higher ID, records who restored it and when, and identifies the source in
    `restoredFromVersionId`. Its fingerprint matches the source version. Render retains the current
    configuration and the three distinct prior configurations most recently active. Removing an older
    configuration also removes all versions that refer to it.

    The response confirms the configuration was saved. It does not confirm that credential injection is
    active for a particular sandbox.

    These endpoints do not return secret values.

    Args:
        sandbox_group_id (str): The ID of the sandbox group. Example: sbg-cph1rs3idesc73a2b2mg.
        credential_id (str): The case-sensitive ID you assign to the credential, unique within its
            sandbox group. Use only letters, numbers, periods, underscores, tildes, and hyphens. The
            names `.` and `..` and IDs starting with `rnd-` are reserved.
             Example: my-inference-key.
        body (SandboxCredentialRestore): The retained credential version to restore.

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

     Restore a retained credential version, including its routing settings, injection settings, and
    secret value, as a new current version. Requires an admin.

    The new version has a higher ID, records who restored it and when, and identifies the source in
    `restoredFromVersionId`. Its fingerprint matches the source version. Render retains the current
    configuration and the three distinct prior configurations most recently active. Removing an older
    configuration also removes all versions that refer to it.

    The response confirms the configuration was saved. It does not confirm that credential injection is
    active for a particular sandbox.

    These endpoints do not return secret values.

    Args:
        sandbox_group_id (str): The ID of the sandbox group. Example: sbg-cph1rs3idesc73a2b2mg.
        credential_id (str): The case-sensitive ID you assign to the credential, unique within its
            sandbox group. Use only letters, numbers, periods, underscores, tildes, and hyphens. The
            names `.` and `..` and IDs starting with `rnd-` are reserved.
             Example: my-inference-key.
        body (SandboxCredentialRestore): The retained credential version to restore.

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

     Restore a retained credential version, including its routing settings, injection settings, and
    secret value, as a new current version. Requires an admin.

    The new version has a higher ID, records who restored it and when, and identifies the source in
    `restoredFromVersionId`. Its fingerprint matches the source version. Render retains the current
    configuration and the three distinct prior configurations most recently active. Removing an older
    configuration also removes all versions that refer to it.

    The response confirms the configuration was saved. It does not confirm that credential injection is
    active for a particular sandbox.

    These endpoints do not return secret values.

    Args:
        sandbox_group_id (str): The ID of the sandbox group. Example: sbg-cph1rs3idesc73a2b2mg.
        credential_id (str): The case-sensitive ID you assign to the credential, unique within its
            sandbox group. Use only letters, numbers, periods, underscores, tildes, and hyphens. The
            names `.` and `..` and IDs starting with `rnd-` are reserved.
             Example: my-inference-key.
        body (SandboxCredentialRestore): The retained credential version to restore.

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

     Restore a retained credential version, including its routing settings, injection settings, and
    secret value, as a new current version. Requires an admin.

    The new version has a higher ID, records who restored it and when, and identifies the source in
    `restoredFromVersionId`. Its fingerprint matches the source version. Render retains the current
    configuration and the three distinct prior configurations most recently active. Removing an older
    configuration also removes all versions that refer to it.

    The response confirms the configuration was saved. It does not confirm that credential injection is
    active for a particular sandbox.

    These endpoints do not return secret values.

    Args:
        sandbox_group_id (str): The ID of the sandbox group. Example: sbg-cph1rs3idesc73a2b2mg.
        credential_id (str): The case-sensitive ID you assign to the credential, unique within its
            sandbox group. Use only letters, numbers, periods, underscores, tildes, and hyphens. The
            names `.` and `..` and IDs starting with `rnd-` are reserved.
             Example: my-inference-key.
        body (SandboxCredentialRestore): The retained credential version to restore.

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
