from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.registry_credential import RegistryCredential
from ...models.update_registry_credential_body import UpdateRegistryCredentialBody
from ...types import Response


def _get_kwargs(
    registry_credential_id: str,
    *,
    body: UpdateRegistryCredentialBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": f"/registrycredentials/{registry_credential_id}",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, RegistryCredential]]:
    if response.status_code == 200:
        response_200 = RegistryCredential.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 402:
        response_402 = Error.from_dict(response.json())

        return response_402

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404

    if response.status_code == 406:
        response_406 = Error.from_dict(response.json())

        return response_406

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        return response_409

    if response.status_code == 410:
        response_410 = Error.from_dict(response.json())

        return response_410

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
) -> Response[Union[Error, RegistryCredential]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    registry_credential_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateRegistryCredentialBody,
) -> Response[Union[Error, RegistryCredential]]:
    """Update registry credential

     Update the registry credential with the provided ID. Services that use this credential must be
    redeployed to use updated values.

    Args:
        registry_credential_id (str):
        body (UpdateRegistryCredentialBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, RegistryCredential]]
    """

    kwargs = _get_kwargs(
        registry_credential_id=registry_credential_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    registry_credential_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateRegistryCredentialBody,
) -> Optional[Union[Error, RegistryCredential]]:
    """Update registry credential

     Update the registry credential with the provided ID. Services that use this credential must be
    redeployed to use updated values.

    Args:
        registry_credential_id (str):
        body (UpdateRegistryCredentialBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, RegistryCredential]
    """

    return sync_detailed(
        registry_credential_id=registry_credential_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    registry_credential_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateRegistryCredentialBody,
) -> Response[Union[Error, RegistryCredential]]:
    """Update registry credential

     Update the registry credential with the provided ID. Services that use this credential must be
    redeployed to use updated values.

    Args:
        registry_credential_id (str):
        body (UpdateRegistryCredentialBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, RegistryCredential]]
    """

    kwargs = _get_kwargs(
        registry_credential_id=registry_credential_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    registry_credential_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateRegistryCredentialBody,
) -> Optional[Union[Error, RegistryCredential]]:
    """Update registry credential

     Update the registry credential with the provided ID. Services that use this credential must be
    redeployed to use updated values.

    Args:
        registry_credential_id (str):
        body (UpdateRegistryCredentialBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, RegistryCredential]
    """

    return (
        await asyncio_detailed(
            registry_credential_id=registry_credential_id,
            client=client,
            body=body,
        )
    ).parsed
