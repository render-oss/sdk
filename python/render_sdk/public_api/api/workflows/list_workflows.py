from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    name: Union[Unset, list[str]] = UNSET,
    owner_id: Union[Unset, list[str]] = UNSET,
    workflow_id: Union[Unset, list[str]] = UNSET,
    environment_id: Union[Unset, list[str]] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_name: Union[Unset, list[str]] = UNSET
    if not isinstance(name, Unset):
        json_name = name

    params["name"] = json_name

    json_owner_id: Union[Unset, list[str]] = UNSET
    if not isinstance(owner_id, Unset):
        json_owner_id = owner_id

    params["ownerId"] = json_owner_id

    json_workflow_id: Union[Unset, list[str]] = UNSET
    if not isinstance(workflow_id, Unset):
        json_workflow_id = workflow_id

    params["workflowID"] = json_workflow_id

    json_environment_id: Union[Unset, list[str]] = UNSET
    if not isinstance(environment_id, Unset):
        json_environment_id = environment_id

    params["environmentId"] = json_environment_id

    params["cursor"] = cursor

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/workflows",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Error]:
    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())

        return response_403

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
    owner_id: Union[Unset, list[str]] = UNSET,
    workflow_id: Union[Unset, list[str]] = UNSET,
    environment_id: Union[Unset, list[str]] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> Response[Error]:
    """List all workflows

    Args:
        name (Union[Unset, list[str]]):
        owner_id (Union[Unset, list[str]]):
        workflow_id (Union[Unset, list[str]]):
        environment_id (Union[Unset, list[str]]):
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
        owner_id=owner_id,
        workflow_id=workflow_id,
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
    owner_id: Union[Unset, list[str]] = UNSET,
    workflow_id: Union[Unset, list[str]] = UNSET,
    environment_id: Union[Unset, list[str]] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> Optional[Error]:
    """List all workflows

    Args:
        name (Union[Unset, list[str]]):
        owner_id (Union[Unset, list[str]]):
        workflow_id (Union[Unset, list[str]]):
        environment_id (Union[Unset, list[str]]):
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
        owner_id=owner_id,
        workflow_id=workflow_id,
        environment_id=environment_id,
        cursor=cursor,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    name: Union[Unset, list[str]] = UNSET,
    owner_id: Union[Unset, list[str]] = UNSET,
    workflow_id: Union[Unset, list[str]] = UNSET,
    environment_id: Union[Unset, list[str]] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> Response[Error]:
    """List all workflows

    Args:
        name (Union[Unset, list[str]]):
        owner_id (Union[Unset, list[str]]):
        workflow_id (Union[Unset, list[str]]):
        environment_id (Union[Unset, list[str]]):
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
        owner_id=owner_id,
        workflow_id=workflow_id,
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
    owner_id: Union[Unset, list[str]] = UNSET,
    workflow_id: Union[Unset, list[str]] = UNSET,
    environment_id: Union[Unset, list[str]] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> Optional[Error]:
    """List all workflows

    Args:
        name (Union[Unset, list[str]]):
        owner_id (Union[Unset, list[str]]):
        workflow_id (Union[Unset, list[str]]):
        environment_id (Union[Unset, list[str]]):
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
            owner_id=owner_id,
            workflow_id=workflow_id,
            environment_id=environment_id,
            cursor=cursor,
            limit=limit,
        )
    ).parsed
