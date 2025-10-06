import datetime
from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.environment_with_cursor import EnvironmentWithCursor
from ...models.error import Error
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    name: Union[Unset, list[str]] = UNSET,
    project_id: list[str],
    created_before: Union[Unset, datetime.datetime] = UNSET,
    created_after: Union[Unset, datetime.datetime] = UNSET,
    updated_before: Union[Unset, datetime.datetime] = UNSET,
    updated_after: Union[Unset, datetime.datetime] = UNSET,
    owner_id: Union[Unset, list[str]] = UNSET,
    environment_id: Union[Unset, list[str]] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_name: Union[Unset, list[str]] = UNSET
    if not isinstance(name, Unset):
        json_name = name

    params["name"] = json_name

    json_project_id = project_id

    params["projectId"] = json_project_id

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

    json_environment_id: Union[Unset, list[str]] = UNSET
    if not isinstance(environment_id, Unset):
        json_environment_id = environment_id

    params["environmentId"] = json_environment_id

    params["cursor"] = cursor

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/environments",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, list["EnvironmentWithCursor"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = EnvironmentWithCursor.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404

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
) -> Response[Union[Error, list["EnvironmentWithCursor"]]]:
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
    project_id: list[str],
    created_before: Union[Unset, datetime.datetime] = UNSET,
    created_after: Union[Unset, datetime.datetime] = UNSET,
    updated_before: Union[Unset, datetime.datetime] = UNSET,
    updated_after: Union[Unset, datetime.datetime] = UNSET,
    owner_id: Union[Unset, list[str]] = UNSET,
    environment_id: Union[Unset, list[str]] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> Response[Union[Error, list["EnvironmentWithCursor"]]]:
    """List environments

     List a particular project's environments matching the provided filters. If no filters are provided,
    all environments are returned.

    Args:
        name (Union[Unset, list[str]]):
        project_id (list[str]):
        created_before (Union[Unset, datetime.datetime]):
        created_after (Union[Unset, datetime.datetime]):
        updated_before (Union[Unset, datetime.datetime]):
        updated_after (Union[Unset, datetime.datetime]):
        owner_id (Union[Unset, list[str]]):
        environment_id (Union[Unset, list[str]]):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, list['EnvironmentWithCursor']]]
    """

    kwargs = _get_kwargs(
        name=name,
        project_id=project_id,
        created_before=created_before,
        created_after=created_after,
        updated_before=updated_before,
        updated_after=updated_after,
        owner_id=owner_id,
        environment_id=environment_id,
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
    project_id: list[str],
    created_before: Union[Unset, datetime.datetime] = UNSET,
    created_after: Union[Unset, datetime.datetime] = UNSET,
    updated_before: Union[Unset, datetime.datetime] = UNSET,
    updated_after: Union[Unset, datetime.datetime] = UNSET,
    owner_id: Union[Unset, list[str]] = UNSET,
    environment_id: Union[Unset, list[str]] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> Optional[Union[Error, list["EnvironmentWithCursor"]]]:
    """List environments

     List a particular project's environments matching the provided filters. If no filters are provided,
    all environments are returned.

    Args:
        name (Union[Unset, list[str]]):
        project_id (list[str]):
        created_before (Union[Unset, datetime.datetime]):
        created_after (Union[Unset, datetime.datetime]):
        updated_before (Union[Unset, datetime.datetime]):
        updated_after (Union[Unset, datetime.datetime]):
        owner_id (Union[Unset, list[str]]):
        environment_id (Union[Unset, list[str]]):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, list['EnvironmentWithCursor']]
    """

    return sync_detailed(
        client=client,
        name=name,
        project_id=project_id,
        created_before=created_before,
        created_after=created_after,
        updated_before=updated_before,
        updated_after=updated_after,
        owner_id=owner_id,
        environment_id=environment_id,
        cursor=cursor,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    name: Union[Unset, list[str]] = UNSET,
    project_id: list[str],
    created_before: Union[Unset, datetime.datetime] = UNSET,
    created_after: Union[Unset, datetime.datetime] = UNSET,
    updated_before: Union[Unset, datetime.datetime] = UNSET,
    updated_after: Union[Unset, datetime.datetime] = UNSET,
    owner_id: Union[Unset, list[str]] = UNSET,
    environment_id: Union[Unset, list[str]] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> Response[Union[Error, list["EnvironmentWithCursor"]]]:
    """List environments

     List a particular project's environments matching the provided filters. If no filters are provided,
    all environments are returned.

    Args:
        name (Union[Unset, list[str]]):
        project_id (list[str]):
        created_before (Union[Unset, datetime.datetime]):
        created_after (Union[Unset, datetime.datetime]):
        updated_before (Union[Unset, datetime.datetime]):
        updated_after (Union[Unset, datetime.datetime]):
        owner_id (Union[Unset, list[str]]):
        environment_id (Union[Unset, list[str]]):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, list['EnvironmentWithCursor']]]
    """

    kwargs = _get_kwargs(
        name=name,
        project_id=project_id,
        created_before=created_before,
        created_after=created_after,
        updated_before=updated_before,
        updated_after=updated_after,
        owner_id=owner_id,
        environment_id=environment_id,
        cursor=cursor,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    name: Union[Unset, list[str]] = UNSET,
    project_id: list[str],
    created_before: Union[Unset, datetime.datetime] = UNSET,
    created_after: Union[Unset, datetime.datetime] = UNSET,
    updated_before: Union[Unset, datetime.datetime] = UNSET,
    updated_after: Union[Unset, datetime.datetime] = UNSET,
    owner_id: Union[Unset, list[str]] = UNSET,
    environment_id: Union[Unset, list[str]] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> Optional[Union[Error, list["EnvironmentWithCursor"]]]:
    """List environments

     List a particular project's environments matching the provided filters. If no filters are provided,
    all environments are returned.

    Args:
        name (Union[Unset, list[str]]):
        project_id (list[str]):
        created_before (Union[Unset, datetime.datetime]):
        created_after (Union[Unset, datetime.datetime]):
        updated_before (Union[Unset, datetime.datetime]):
        updated_after (Union[Unset, datetime.datetime]):
        owner_id (Union[Unset, list[str]]):
        environment_id (Union[Unset, list[str]]):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, list['EnvironmentWithCursor']]
    """

    return (
        await asyncio_detailed(
            client=client,
            name=name,
            project_id=project_id,
            created_before=created_before,
            created_after=created_after,
            updated_before=updated_before,
            updated_after=updated_after,
            owner_id=owner_id,
            environment_id=environment_id,
            cursor=cursor,
            limit=limit,
        )
    ).parsed
