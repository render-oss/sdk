import datetime
from http import HTTPStatus
from typing import Any

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.registry_credential import RegistryCredential
from ...models.registry_credential_registry import RegistryCredentialRegistry
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    name: list[str] | Unset = UNSET,
    username: list[str] | Unset = UNSET,
    type_: list[RegistryCredentialRegistry] | Unset = UNSET,
    created_before: datetime.datetime | Unset = UNSET,
    created_after: datetime.datetime | Unset = UNSET,
    updated_before: datetime.datetime | Unset = UNSET,
    updated_after: datetime.datetime | Unset = UNSET,
    owner_id: list[str] | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 20,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_name: list[str] | Unset = UNSET
    if not isinstance(name, Unset):
        json_name = name

    params["name"] = json_name

    json_username: list[str] | Unset = UNSET
    if not isinstance(username, Unset):
        json_username = username

    params["username"] = json_username

    json_type_: list[str] | Unset = UNSET
    if not isinstance(type_, Unset):
        json_type_ = []
        for type_item_data in type_:
            type_item = type_item_data.value
            json_type_.append(type_item)

    params["type"] = json_type_

    json_created_before: str | Unset = UNSET
    if not isinstance(created_before, Unset):
        json_created_before = created_before.isoformat()
    params["createdBefore"] = json_created_before

    json_created_after: str | Unset = UNSET
    if not isinstance(created_after, Unset):
        json_created_after = created_after.isoformat()
    params["createdAfter"] = json_created_after

    json_updated_before: str | Unset = UNSET
    if not isinstance(updated_before, Unset):
        json_updated_before = updated_before.isoformat()
    params["updatedBefore"] = json_updated_before

    json_updated_after: str | Unset = UNSET
    if not isinstance(updated_after, Unset):
        json_updated_after = updated_after.isoformat()
    params["updatedAfter"] = json_updated_after

    json_owner_id: list[str] | Unset = UNSET
    if not isinstance(owner_id, Unset):
        json_owner_id = owner_id

    params["ownerId"] = json_owner_id

    params["cursor"] = cursor

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/registrycredentials",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Error | list[RegistryCredential] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = RegistryCredential.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 406:
        response_406 = Error.from_dict(response.json())

        return response_406

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
) -> Response[Error | list[RegistryCredential]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    name: list[str] | Unset = UNSET,
    username: list[str] | Unset = UNSET,
    type_: list[RegistryCredentialRegistry] | Unset = UNSET,
    created_before: datetime.datetime | Unset = UNSET,
    created_after: datetime.datetime | Unset = UNSET,
    updated_before: datetime.datetime | Unset = UNSET,
    updated_after: datetime.datetime | Unset = UNSET,
    owner_id: list[str] | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 20,
) -> Response[Error | list[RegistryCredential]]:
    """List registry credentials

     List registry credentials matching the provided filters. If no filters are provided, returns all
    registry credentials you have permissions to view.

    Args:
        name (list[str] | Unset):
        username (list[str] | Unset):
        type_ (list[RegistryCredentialRegistry] | Unset):
        created_before (datetime.datetime | Unset):
        created_after (datetime.datetime | Unset):
        updated_before (datetime.datetime | Unset):
        updated_after (datetime.datetime | Unset):
        owner_id (list[str] | Unset):
        cursor (str | Unset):
        limit (int | Unset): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[RegistryCredential]]
    """

    kwargs = _get_kwargs(
        name=name,
        username=username,
        type_=type_,
        created_before=created_before,
        created_after=created_after,
        updated_before=updated_before,
        updated_after=updated_after,
        owner_id=owner_id,
        cursor=cursor,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    name: list[str] | Unset = UNSET,
    username: list[str] | Unset = UNSET,
    type_: list[RegistryCredentialRegistry] | Unset = UNSET,
    created_before: datetime.datetime | Unset = UNSET,
    created_after: datetime.datetime | Unset = UNSET,
    updated_before: datetime.datetime | Unset = UNSET,
    updated_after: datetime.datetime | Unset = UNSET,
    owner_id: list[str] | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 20,
) -> Error | list[RegistryCredential] | None:
    """List registry credentials

     List registry credentials matching the provided filters. If no filters are provided, returns all
    registry credentials you have permissions to view.

    Args:
        name (list[str] | Unset):
        username (list[str] | Unset):
        type_ (list[RegistryCredentialRegistry] | Unset):
        created_before (datetime.datetime | Unset):
        created_after (datetime.datetime | Unset):
        updated_before (datetime.datetime | Unset):
        updated_after (datetime.datetime | Unset):
        owner_id (list[str] | Unset):
        cursor (str | Unset):
        limit (int | Unset): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[RegistryCredential]
    """

    return sync_detailed(
        client=client,
        name=name,
        username=username,
        type_=type_,
        created_before=created_before,
        created_after=created_after,
        updated_before=updated_before,
        updated_after=updated_after,
        owner_id=owner_id,
        cursor=cursor,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    name: list[str] | Unset = UNSET,
    username: list[str] | Unset = UNSET,
    type_: list[RegistryCredentialRegistry] | Unset = UNSET,
    created_before: datetime.datetime | Unset = UNSET,
    created_after: datetime.datetime | Unset = UNSET,
    updated_before: datetime.datetime | Unset = UNSET,
    updated_after: datetime.datetime | Unset = UNSET,
    owner_id: list[str] | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 20,
) -> Response[Error | list[RegistryCredential]]:
    """List registry credentials

     List registry credentials matching the provided filters. If no filters are provided, returns all
    registry credentials you have permissions to view.

    Args:
        name (list[str] | Unset):
        username (list[str] | Unset):
        type_ (list[RegistryCredentialRegistry] | Unset):
        created_before (datetime.datetime | Unset):
        created_after (datetime.datetime | Unset):
        updated_before (datetime.datetime | Unset):
        updated_after (datetime.datetime | Unset):
        owner_id (list[str] | Unset):
        cursor (str | Unset):
        limit (int | Unset): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[RegistryCredential]]
    """

    kwargs = _get_kwargs(
        name=name,
        username=username,
        type_=type_,
        created_before=created_before,
        created_after=created_after,
        updated_before=updated_before,
        updated_after=updated_after,
        owner_id=owner_id,
        cursor=cursor,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    name: list[str] | Unset = UNSET,
    username: list[str] | Unset = UNSET,
    type_: list[RegistryCredentialRegistry] | Unset = UNSET,
    created_before: datetime.datetime | Unset = UNSET,
    created_after: datetime.datetime | Unset = UNSET,
    updated_before: datetime.datetime | Unset = UNSET,
    updated_after: datetime.datetime | Unset = UNSET,
    owner_id: list[str] | Unset = UNSET,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 20,
) -> Error | list[RegistryCredential] | None:
    """List registry credentials

     List registry credentials matching the provided filters. If no filters are provided, returns all
    registry credentials you have permissions to view.

    Args:
        name (list[str] | Unset):
        username (list[str] | Unset):
        type_ (list[RegistryCredentialRegistry] | Unset):
        created_before (datetime.datetime | Unset):
        created_after (datetime.datetime | Unset):
        updated_before (datetime.datetime | Unset):
        updated_after (datetime.datetime | Unset):
        owner_id (list[str] | Unset):
        cursor (str | Unset):
        limit (int | Unset): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[RegistryCredential]
    """

    return (
        await asyncio_detailed(
            client=client,
            name=name,
            username=username,
            type_=type_,
            created_before=created_before,
            created_after=created_after,
            updated_before=updated_before,
            updated_after=updated_after,
            owner_id=owner_id,
            cursor=cursor,
            limit=limit,
        )
    ).parsed
