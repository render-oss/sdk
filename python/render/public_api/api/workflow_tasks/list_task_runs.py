from http import HTTPStatus
from typing import Any

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.task_run_with_cursor import TaskRunWithCursor
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 20,
    task_slug: list[str] | Unset = UNSET,
    root_task_run_id: list[str] | Unset = UNSET,
    owner_id: list[str] | Unset = UNSET,
    workflow_version_id: list[str] | Unset = UNSET,
    workflow_id: list[str] | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["cursor"] = cursor

    params["limit"] = limit

    json_task_slug: list[str] | Unset = UNSET
    if not isinstance(task_slug, Unset):
        json_task_slug = task_slug

    params["taskSlug"] = json_task_slug

    json_root_task_run_id: list[str] | Unset = UNSET
    if not isinstance(root_task_run_id, Unset):
        json_root_task_run_id = root_task_run_id

    params["rootTaskRunId"] = json_root_task_run_id

    json_owner_id: list[str] | Unset = UNSET
    if not isinstance(owner_id, Unset):
        json_owner_id = owner_id

    params["ownerId"] = json_owner_id

    json_workflow_version_id: list[str] | Unset = UNSET
    if not isinstance(workflow_version_id, Unset):
        json_workflow_version_id = workflow_version_id

    params["workflowVersionId"] = json_workflow_version_id

    json_workflow_id: list[str] | Unset = UNSET
    if not isinstance(workflow_id, Unset):
        json_workflow_id = workflow_id

    params["workflowId"] = json_workflow_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/task-runs",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Error | list[TaskRunWithCursor] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = TaskRunWithCursor.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[Error | list[TaskRunWithCursor]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 20,
    task_slug: list[str] | Unset = UNSET,
    root_task_run_id: list[str] | Unset = UNSET,
    owner_id: list[str] | Unset = UNSET,
    workflow_version_id: list[str] | Unset = UNSET,
    workflow_id: list[str] | Unset = UNSET,
) -> Response[Error | list[TaskRunWithCursor]]:
    """List task runs

     List task runs that match the provided filters. If no filters are provided, all task runs accessible
    by the authenticated user are returned.

    Args:
        cursor (str | Unset):
        limit (int | Unset): Defaults to 20 Default: 20.
        task_slug (list[str] | Unset):
        root_task_run_id (list[str] | Unset):
        owner_id (list[str] | Unset):
        workflow_version_id (list[str] | Unset):
        workflow_id (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[TaskRunWithCursor]]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        limit=limit,
        task_slug=task_slug,
        root_task_run_id=root_task_run_id,
        owner_id=owner_id,
        workflow_version_id=workflow_version_id,
        workflow_id=workflow_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 20,
    task_slug: list[str] | Unset = UNSET,
    root_task_run_id: list[str] | Unset = UNSET,
    owner_id: list[str] | Unset = UNSET,
    workflow_version_id: list[str] | Unset = UNSET,
    workflow_id: list[str] | Unset = UNSET,
) -> Error | list[TaskRunWithCursor] | None:
    """List task runs

     List task runs that match the provided filters. If no filters are provided, all task runs accessible
    by the authenticated user are returned.

    Args:
        cursor (str | Unset):
        limit (int | Unset): Defaults to 20 Default: 20.
        task_slug (list[str] | Unset):
        root_task_run_id (list[str] | Unset):
        owner_id (list[str] | Unset):
        workflow_version_id (list[str] | Unset):
        workflow_id (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[TaskRunWithCursor]
    """

    return sync_detailed(
        client=client,
        cursor=cursor,
        limit=limit,
        task_slug=task_slug,
        root_task_run_id=root_task_run_id,
        owner_id=owner_id,
        workflow_version_id=workflow_version_id,
        workflow_id=workflow_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 20,
    task_slug: list[str] | Unset = UNSET,
    root_task_run_id: list[str] | Unset = UNSET,
    owner_id: list[str] | Unset = UNSET,
    workflow_version_id: list[str] | Unset = UNSET,
    workflow_id: list[str] | Unset = UNSET,
) -> Response[Error | list[TaskRunWithCursor]]:
    """List task runs

     List task runs that match the provided filters. If no filters are provided, all task runs accessible
    by the authenticated user are returned.

    Args:
        cursor (str | Unset):
        limit (int | Unset): Defaults to 20 Default: 20.
        task_slug (list[str] | Unset):
        root_task_run_id (list[str] | Unset):
        owner_id (list[str] | Unset):
        workflow_version_id (list[str] | Unset):
        workflow_id (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[TaskRunWithCursor]]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        limit=limit,
        task_slug=task_slug,
        root_task_run_id=root_task_run_id,
        owner_id=owner_id,
        workflow_version_id=workflow_version_id,
        workflow_id=workflow_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 20,
    task_slug: list[str] | Unset = UNSET,
    root_task_run_id: list[str] | Unset = UNSET,
    owner_id: list[str] | Unset = UNSET,
    workflow_version_id: list[str] | Unset = UNSET,
    workflow_id: list[str] | Unset = UNSET,
) -> Error | list[TaskRunWithCursor] | None:
    """List task runs

     List task runs that match the provided filters. If no filters are provided, all task runs accessible
    by the authenticated user are returned.

    Args:
        cursor (str | Unset):
        limit (int | Unset): Defaults to 20 Default: 20.
        task_slug (list[str] | Unset):
        root_task_run_id (list[str] | Unset):
        owner_id (list[str] | Unset):
        workflow_version_id (list[str] | Unset):
        workflow_id (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[TaskRunWithCursor]
    """

    return (
        await asyncio_detailed(
            client=client,
            cursor=cursor,
            limit=limit,
            task_slug=task_slug,
            root_task_run_id=root_task_run_id,
            owner_id=owner_id,
            workflow_version_id=workflow_version_id,
            workflow_id=workflow_id,
        )
    ).parsed
