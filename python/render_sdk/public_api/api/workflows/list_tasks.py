from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.task import Task
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
    owner_id: Union[Unset, list[str]] = UNSET,
    task_id: Union[Unset, list[str]] = UNSET,
    workflow_version_id: Union[Unset, list[str]] = UNSET,
    workflow_id: Union[Unset, list[str]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["cursor"] = cursor

    params["limit"] = limit

    json_owner_id: Union[Unset, list[str]] = UNSET
    if not isinstance(owner_id, Unset):
        json_owner_id = owner_id

    params["ownerId"] = json_owner_id

    json_task_id: Union[Unset, list[str]] = UNSET
    if not isinstance(task_id, Unset):
        json_task_id = task_id

    params["taskId"] = json_task_id

    json_workflow_version_id: Union[Unset, list[str]] = UNSET
    if not isinstance(workflow_version_id, Unset):
        json_workflow_version_id = workflow_version_id

    params["workflowVersionId"] = json_workflow_version_id

    json_workflow_id: Union[Unset, list[str]] = UNSET
    if not isinstance(workflow_id, Unset):
        json_workflow_id = workflow_id

    params["workflowId"] = json_workflow_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/tasks",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, list["Task"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Task.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

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


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, list["Task"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
    owner_id: Union[Unset, list[str]] = UNSET,
    task_id: Union[Unset, list[str]] = UNSET,
    workflow_version_id: Union[Unset, list[str]] = UNSET,
    workflow_id: Union[Unset, list[str]] = UNSET,
) -> Response[Union[Error, list["Task"]]]:
    """List tasks

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.
        owner_id (Union[Unset, list[str]]):
        task_id (Union[Unset, list[str]]):
        workflow_version_id (Union[Unset, list[str]]):
        workflow_id (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, list['Task']]]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        limit=limit,
        owner_id=owner_id,
        task_id=task_id,
        workflow_version_id=workflow_version_id,
        workflow_id=workflow_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
    owner_id: Union[Unset, list[str]] = UNSET,
    task_id: Union[Unset, list[str]] = UNSET,
    workflow_version_id: Union[Unset, list[str]] = UNSET,
    workflow_id: Union[Unset, list[str]] = UNSET,
) -> Optional[Union[Error, list["Task"]]]:
    """List tasks

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.
        owner_id (Union[Unset, list[str]]):
        task_id (Union[Unset, list[str]]):
        workflow_version_id (Union[Unset, list[str]]):
        workflow_id (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, list['Task']]
    """

    return sync_detailed(
        client=client,
        cursor=cursor,
        limit=limit,
        owner_id=owner_id,
        task_id=task_id,
        workflow_version_id=workflow_version_id,
        workflow_id=workflow_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
    owner_id: Union[Unset, list[str]] = UNSET,
    task_id: Union[Unset, list[str]] = UNSET,
    workflow_version_id: Union[Unset, list[str]] = UNSET,
    workflow_id: Union[Unset, list[str]] = UNSET,
) -> Response[Union[Error, list["Task"]]]:
    """List tasks

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.
        owner_id (Union[Unset, list[str]]):
        task_id (Union[Unset, list[str]]):
        workflow_version_id (Union[Unset, list[str]]):
        workflow_id (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, list['Task']]]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        limit=limit,
        owner_id=owner_id,
        task_id=task_id,
        workflow_version_id=workflow_version_id,
        workflow_id=workflow_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
    owner_id: Union[Unset, list[str]] = UNSET,
    task_id: Union[Unset, list[str]] = UNSET,
    workflow_version_id: Union[Unset, list[str]] = UNSET,
    workflow_id: Union[Unset, list[str]] = UNSET,
) -> Optional[Union[Error, list["Task"]]]:
    """List tasks

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.
        owner_id (Union[Unset, list[str]]):
        task_id (Union[Unset, list[str]]):
        workflow_version_id (Union[Unset, list[str]]):
        workflow_id (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, list['Task']]
    """

    return (
        await asyncio_detailed(
            client=client,
            cursor=cursor,
            limit=limit,
            owner_id=owner_id,
            task_id=task_id,
            workflow_version_id=workflow_version_id,
            workflow_id=workflow_id,
        )
    ).parsed
