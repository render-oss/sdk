import datetime
from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.list_services_suspended_item import ListServicesSuspendedItem
from ...models.region import Region
from ...models.service_runtime import ServiceRuntime
from ...models.service_type import ServiceType
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    name: Union[Unset, list[str]] = UNSET,
    type_: Union[Unset, list[ServiceType]] = UNSET,
    environment_id: Union[Unset, list[str]] = UNSET,
    env: Union[Unset, list[ServiceRuntime]] = UNSET,
    region: Union[Unset, list[Region]] = UNSET,
    suspended: Union[Unset, list[ListServicesSuspendedItem]] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    created_after: Union[Unset, datetime.datetime] = UNSET,
    updated_before: Union[Unset, datetime.datetime] = UNSET,
    updated_after: Union[Unset, datetime.datetime] = UNSET,
    owner_id: Union[Unset, list[str]] = UNSET,
    include_previews: Union[Unset, bool] = True,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_name: Union[Unset, list[str]] = UNSET
    if not isinstance(name, Unset):
        json_name = name

    params["name"] = json_name

    json_type_: Union[Unset, list[str]] = UNSET
    if not isinstance(type_, Unset):
        json_type_ = []
        for type_item_data in type_:
            type_item = type_item_data.value
            json_type_.append(type_item)

    params["type"] = json_type_

    json_environment_id: Union[Unset, list[str]] = UNSET
    if not isinstance(environment_id, Unset):
        json_environment_id = environment_id

    params["environmentId"] = json_environment_id

    json_env: Union[Unset, list[str]] = UNSET
    if not isinstance(env, Unset):
        json_env = []
        for env_item_data in env:
            env_item = env_item_data.value
            json_env.append(env_item)

    params["env"] = json_env

    json_region: Union[Unset, list[str]] = UNSET
    if not isinstance(region, Unset):
        json_region = []
        for region_item_data in region:
            region_item = region_item_data.value
            json_region.append(region_item)

    params["region"] = json_region

    json_suspended: Union[Unset, list[str]] = UNSET
    if not isinstance(suspended, Unset):
        json_suspended = []
        for suspended_item_data in suspended:
            suspended_item = suspended_item_data.value
            json_suspended.append(suspended_item)

    params["suspended"] = json_suspended

    json_created_before: Union[Unset, str] = UNSET
    if not isinstance(created_before, Unset):
        json_created_before = created_before.isoformat()
    params["createdBefore"] = json_created_before

    json_created_after: Union[Unset, str] = UNSET
    if not isinstance(created_after, Unset):
        json_created_after = created_after.isoformat()
    params["createdAfter"] = json_created_after

    json_updated_before: Union[Unset, str] = UNSET
    if not isinstance(updated_before, Unset):
        json_updated_before = updated_before.isoformat()
    params["updatedBefore"] = json_updated_before

    json_updated_after: Union[Unset, str] = UNSET
    if not isinstance(updated_after, Unset):
        json_updated_after = updated_after.isoformat()
    params["updatedAfter"] = json_updated_after

    json_owner_id: Union[Unset, list[str]] = UNSET
    if not isinstance(owner_id, Unset):
        json_owner_id = owner_id

    params["ownerId"] = json_owner_id

    params["includePreviews"] = include_previews

    params["cursor"] = cursor

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/services",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Error]:
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


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    name: Union[Unset, list[str]] = UNSET,
    type_: Union[Unset, list[ServiceType]] = UNSET,
    environment_id: Union[Unset, list[str]] = UNSET,
    env: Union[Unset, list[ServiceRuntime]] = UNSET,
    region: Union[Unset, list[Region]] = UNSET,
    suspended: Union[Unset, list[ListServicesSuspendedItem]] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    created_after: Union[Unset, datetime.datetime] = UNSET,
    updated_before: Union[Unset, datetime.datetime] = UNSET,
    updated_after: Union[Unset, datetime.datetime] = UNSET,
    owner_id: Union[Unset, list[str]] = UNSET,
    include_previews: Union[Unset, bool] = True,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> Response[Error]:
    """List services

     List services matching the provided filters. If no filters are provided, returns all services you
    have permissions to view.

    Args:
        name (Union[Unset, list[str]]):
        type_ (Union[Unset, list[ServiceType]]):
        environment_id (Union[Unset, list[str]]):
        env (Union[Unset, list[ServiceRuntime]]):
        region (Union[Unset, list[Region]]):
        suspended (Union[Unset, list[ListServicesSuspendedItem]]):
        created_before (Union[Unset, datetime.datetime]):
        created_after (Union[Unset, datetime.datetime]):
        updated_before (Union[Unset, datetime.datetime]):
        updated_after (Union[Unset, datetime.datetime]):
        owner_id (Union[Unset, list[str]]):
        include_previews (Union[Unset, bool]):  Default: True.
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error]
    """

    kwargs = _get_kwargs(
        name=name,
        type_=type_,
        environment_id=environment_id,
        env=env,
        region=region,
        suspended=suspended,
        created_before=created_before,
        created_after=created_after,
        updated_before=updated_before,
        updated_after=updated_after,
        owner_id=owner_id,
        include_previews=include_previews,
        cursor=cursor,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    name: Union[Unset, list[str]] = UNSET,
    type_: Union[Unset, list[ServiceType]] = UNSET,
    environment_id: Union[Unset, list[str]] = UNSET,
    env: Union[Unset, list[ServiceRuntime]] = UNSET,
    region: Union[Unset, list[Region]] = UNSET,
    suspended: Union[Unset, list[ListServicesSuspendedItem]] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    created_after: Union[Unset, datetime.datetime] = UNSET,
    updated_before: Union[Unset, datetime.datetime] = UNSET,
    updated_after: Union[Unset, datetime.datetime] = UNSET,
    owner_id: Union[Unset, list[str]] = UNSET,
    include_previews: Union[Unset, bool] = True,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> Optional[Error]:
    """List services

     List services matching the provided filters. If no filters are provided, returns all services you
    have permissions to view.

    Args:
        name (Union[Unset, list[str]]):
        type_ (Union[Unset, list[ServiceType]]):
        environment_id (Union[Unset, list[str]]):
        env (Union[Unset, list[ServiceRuntime]]):
        region (Union[Unset, list[Region]]):
        suspended (Union[Unset, list[ListServicesSuspendedItem]]):
        created_before (Union[Unset, datetime.datetime]):
        created_after (Union[Unset, datetime.datetime]):
        updated_before (Union[Unset, datetime.datetime]):
        updated_after (Union[Unset, datetime.datetime]):
        owner_id (Union[Unset, list[str]]):
        include_previews (Union[Unset, bool]):  Default: True.
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error
    """

    return sync_detailed(
        client=client,
        name=name,
        type_=type_,
        environment_id=environment_id,
        env=env,
        region=region,
        suspended=suspended,
        created_before=created_before,
        created_after=created_after,
        updated_before=updated_before,
        updated_after=updated_after,
        owner_id=owner_id,
        include_previews=include_previews,
        cursor=cursor,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    name: Union[Unset, list[str]] = UNSET,
    type_: Union[Unset, list[ServiceType]] = UNSET,
    environment_id: Union[Unset, list[str]] = UNSET,
    env: Union[Unset, list[ServiceRuntime]] = UNSET,
    region: Union[Unset, list[Region]] = UNSET,
    suspended: Union[Unset, list[ListServicesSuspendedItem]] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    created_after: Union[Unset, datetime.datetime] = UNSET,
    updated_before: Union[Unset, datetime.datetime] = UNSET,
    updated_after: Union[Unset, datetime.datetime] = UNSET,
    owner_id: Union[Unset, list[str]] = UNSET,
    include_previews: Union[Unset, bool] = True,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> Response[Error]:
    """List services

     List services matching the provided filters. If no filters are provided, returns all services you
    have permissions to view.

    Args:
        name (Union[Unset, list[str]]):
        type_ (Union[Unset, list[ServiceType]]):
        environment_id (Union[Unset, list[str]]):
        env (Union[Unset, list[ServiceRuntime]]):
        region (Union[Unset, list[Region]]):
        suspended (Union[Unset, list[ListServicesSuspendedItem]]):
        created_before (Union[Unset, datetime.datetime]):
        created_after (Union[Unset, datetime.datetime]):
        updated_before (Union[Unset, datetime.datetime]):
        updated_after (Union[Unset, datetime.datetime]):
        owner_id (Union[Unset, list[str]]):
        include_previews (Union[Unset, bool]):  Default: True.
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error]
    """

    kwargs = _get_kwargs(
        name=name,
        type_=type_,
        environment_id=environment_id,
        env=env,
        region=region,
        suspended=suspended,
        created_before=created_before,
        created_after=created_after,
        updated_before=updated_before,
        updated_after=updated_after,
        owner_id=owner_id,
        include_previews=include_previews,
        cursor=cursor,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    name: Union[Unset, list[str]] = UNSET,
    type_: Union[Unset, list[ServiceType]] = UNSET,
    environment_id: Union[Unset, list[str]] = UNSET,
    env: Union[Unset, list[ServiceRuntime]] = UNSET,
    region: Union[Unset, list[Region]] = UNSET,
    suspended: Union[Unset, list[ListServicesSuspendedItem]] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    created_after: Union[Unset, datetime.datetime] = UNSET,
    updated_before: Union[Unset, datetime.datetime] = UNSET,
    updated_after: Union[Unset, datetime.datetime] = UNSET,
    owner_id: Union[Unset, list[str]] = UNSET,
    include_previews: Union[Unset, bool] = True,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> Optional[Error]:
    """List services

     List services matching the provided filters. If no filters are provided, returns all services you
    have permissions to view.

    Args:
        name (Union[Unset, list[str]]):
        type_ (Union[Unset, list[ServiceType]]):
        environment_id (Union[Unset, list[str]]):
        env (Union[Unset, list[ServiceRuntime]]):
        region (Union[Unset, list[Region]]):
        suspended (Union[Unset, list[ListServicesSuspendedItem]]):
        created_before (Union[Unset, datetime.datetime]):
        created_after (Union[Unset, datetime.datetime]):
        updated_before (Union[Unset, datetime.datetime]):
        updated_after (Union[Unset, datetime.datetime]):
        owner_id (Union[Unset, list[str]]):
        include_previews (Union[Unset, bool]):  Default: True.
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error
    """

    return (
        await asyncio_detailed(
            client=client,
            name=name,
            type_=type_,
            environment_id=environment_id,
            env=env,
            region=region,
            suspended=suspended,
            created_before=created_before,
            created_after=created_after,
            updated_before=updated_before,
            updated_after=updated_after,
            owner_id=owner_id,
            include_previews=include_previews,
            cursor=cursor,
            limit=limit,
        )
    ).parsed
