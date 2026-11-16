import datetime
from http import HTTPStatus
from typing import Any, cast

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.list_logs_values_label import ListLogsValuesLabel
from ...models.log_direction import LogDirection
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    owner_id: str,
    label: ListLogsValuesLabel,
    start_time: datetime.datetime | Unset = UNSET,
    end_time: datetime.datetime | Unset = UNSET,
    direction: LogDirection | Unset = UNSET,
    resource: list[str],
    instance: list[str] | Unset = UNSET,
    host: list[str] | Unset = UNSET,
    status_code: list[str] | Unset = UNSET,
    method: list[str] | Unset = UNSET,
    task: list[str] | Unset = UNSET,
    task_run: list[str] | Unset = UNSET,
    sandbox: list[str] | Unset = UNSET,
    build: list[str] | Unset = UNSET,
    level: list[str] | Unset = UNSET,
    type_: list[str] | Unset = UNSET,
    text: list[str] | Unset = UNSET,
    path: list[str] | Unset = UNSET,
    limit: int | Unset = 20,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["ownerId"] = owner_id

    json_label = label.value
    params["label"] = json_label

    json_start_time: str | Unset = UNSET
    if not isinstance(start_time, Unset):
        json_start_time = start_time.isoformat()
    params["startTime"] = json_start_time

    json_end_time: str | Unset = UNSET
    if not isinstance(end_time, Unset):
        json_end_time = end_time.isoformat()
    params["endTime"] = json_end_time

    json_direction: str | Unset = UNSET
    if not isinstance(direction, Unset):
        json_direction = direction.value

    params["direction"] = json_direction

    json_resource = resource

    params["resource"] = json_resource

    json_instance: list[str] | Unset = UNSET
    if not isinstance(instance, Unset):
        json_instance = instance

    params["instance"] = json_instance

    json_host: list[str] | Unset = UNSET
    if not isinstance(host, Unset):
        json_host = host

    params["host"] = json_host

    json_status_code: list[str] | Unset = UNSET
    if not isinstance(status_code, Unset):
        json_status_code = status_code

    params["statusCode"] = json_status_code

    json_method: list[str] | Unset = UNSET
    if not isinstance(method, Unset):
        json_method = method

    params["method"] = json_method

    json_task: list[str] | Unset = UNSET
    if not isinstance(task, Unset):
        json_task = task

    params["task"] = json_task

    json_task_run: list[str] | Unset = UNSET
    if not isinstance(task_run, Unset):
        json_task_run = task_run

    params["taskRun"] = json_task_run

    json_sandbox: list[str] | Unset = UNSET
    if not isinstance(sandbox, Unset):
        json_sandbox = sandbox

    params["sandbox"] = json_sandbox

    json_build: list[str] | Unset = UNSET
    if not isinstance(build, Unset):
        json_build = build

    params["build"] = json_build

    json_level: list[str] | Unset = UNSET
    if not isinstance(level, Unset):
        json_level = level

    params["level"] = json_level

    json_type_: list[str] | Unset = UNSET
    if not isinstance(type_, Unset):
        json_type_ = type_

    params["type"] = json_type_

    json_text: list[str] | Unset = UNSET
    if not isinstance(text, Unset):
        json_text = text

    params["text"] = json_text

    json_path: list[str] | Unset = UNSET
    if not isinstance(path, Unset):
        json_path = path

    params["path"] = json_path

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/logs/values",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx2.Response) -> Error | list[str] | None:
    if response.status_code == 200:
        response_200 = cast(list[str], response.json())

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

    if response.status_code == 406:
        response_406 = Error.from_dict(response.json())

        return response_406

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx2.Response) -> Response[Error | list[str]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    owner_id: str,
    label: ListLogsValuesLabel,
    start_time: datetime.datetime | Unset = UNSET,
    end_time: datetime.datetime | Unset = UNSET,
    direction: LogDirection | Unset = UNSET,
    resource: list[str],
    instance: list[str] | Unset = UNSET,
    host: list[str] | Unset = UNSET,
    status_code: list[str] | Unset = UNSET,
    method: list[str] | Unset = UNSET,
    task: list[str] | Unset = UNSET,
    task_run: list[str] | Unset = UNSET,
    sandbox: list[str] | Unset = UNSET,
    build: list[str] | Unset = UNSET,
    level: list[str] | Unset = UNSET,
    type_: list[str] | Unset = UNSET,
    text: list[str] | Unset = UNSET,
    path: list[str] | Unset = UNSET,
    limit: int | Unset = 20,
) -> Response[Error | list[str]]:
    """List log label values

     List all values for a given log label in the logs matching the provided filters.

    Args:
        owner_id (str):
        label (ListLogsValuesLabel):
        start_time (datetime.datetime | Unset):  Example: 2021-06-17T08:15:30Z.
        end_time (datetime.datetime | Unset):  Example: 2021-06-17T08:30:30Z.
        direction (LogDirection | Unset):
        resource (list[str]):
        instance (list[str] | Unset):
        host (list[str] | Unset):
        status_code (list[str] | Unset):
        method (list[str] | Unset):
        task (list[str] | Unset):
        task_run (list[str] | Unset):
        sandbox (list[str] | Unset):
        build (list[str] | Unset):
        level (list[str] | Unset):
        type_ (list[str] | Unset):
        text (list[str] | Unset):
        path (list[str] | Unset):
        limit (int | Unset): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[str]]
    """

    kwargs = _get_kwargs(
        owner_id=owner_id,
        label=label,
        start_time=start_time,
        end_time=end_time,
        direction=direction,
        resource=resource,
        instance=instance,
        host=host,
        status_code=status_code,
        method=method,
        task=task,
        task_run=task_run,
        sandbox=sandbox,
        build=build,
        level=level,
        type_=type_,
        text=text,
        path=path,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    owner_id: str,
    label: ListLogsValuesLabel,
    start_time: datetime.datetime | Unset = UNSET,
    end_time: datetime.datetime | Unset = UNSET,
    direction: LogDirection | Unset = UNSET,
    resource: list[str],
    instance: list[str] | Unset = UNSET,
    host: list[str] | Unset = UNSET,
    status_code: list[str] | Unset = UNSET,
    method: list[str] | Unset = UNSET,
    task: list[str] | Unset = UNSET,
    task_run: list[str] | Unset = UNSET,
    sandbox: list[str] | Unset = UNSET,
    build: list[str] | Unset = UNSET,
    level: list[str] | Unset = UNSET,
    type_: list[str] | Unset = UNSET,
    text: list[str] | Unset = UNSET,
    path: list[str] | Unset = UNSET,
    limit: int | Unset = 20,
) -> Error | list[str] | None:
    """List log label values

     List all values for a given log label in the logs matching the provided filters.

    Args:
        owner_id (str):
        label (ListLogsValuesLabel):
        start_time (datetime.datetime | Unset):  Example: 2021-06-17T08:15:30Z.
        end_time (datetime.datetime | Unset):  Example: 2021-06-17T08:30:30Z.
        direction (LogDirection | Unset):
        resource (list[str]):
        instance (list[str] | Unset):
        host (list[str] | Unset):
        status_code (list[str] | Unset):
        method (list[str] | Unset):
        task (list[str] | Unset):
        task_run (list[str] | Unset):
        sandbox (list[str] | Unset):
        build (list[str] | Unset):
        level (list[str] | Unset):
        type_ (list[str] | Unset):
        text (list[str] | Unset):
        path (list[str] | Unset):
        limit (int | Unset): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[str]
    """

    return sync_detailed(
        client=client,
        owner_id=owner_id,
        label=label,
        start_time=start_time,
        end_time=end_time,
        direction=direction,
        resource=resource,
        instance=instance,
        host=host,
        status_code=status_code,
        method=method,
        task=task,
        task_run=task_run,
        sandbox=sandbox,
        build=build,
        level=level,
        type_=type_,
        text=text,
        path=path,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    owner_id: str,
    label: ListLogsValuesLabel,
    start_time: datetime.datetime | Unset = UNSET,
    end_time: datetime.datetime | Unset = UNSET,
    direction: LogDirection | Unset = UNSET,
    resource: list[str],
    instance: list[str] | Unset = UNSET,
    host: list[str] | Unset = UNSET,
    status_code: list[str] | Unset = UNSET,
    method: list[str] | Unset = UNSET,
    task: list[str] | Unset = UNSET,
    task_run: list[str] | Unset = UNSET,
    sandbox: list[str] | Unset = UNSET,
    build: list[str] | Unset = UNSET,
    level: list[str] | Unset = UNSET,
    type_: list[str] | Unset = UNSET,
    text: list[str] | Unset = UNSET,
    path: list[str] | Unset = UNSET,
    limit: int | Unset = 20,
) -> Response[Error | list[str]]:
    """List log label values

     List all values for a given log label in the logs matching the provided filters.

    Args:
        owner_id (str):
        label (ListLogsValuesLabel):
        start_time (datetime.datetime | Unset):  Example: 2021-06-17T08:15:30Z.
        end_time (datetime.datetime | Unset):  Example: 2021-06-17T08:30:30Z.
        direction (LogDirection | Unset):
        resource (list[str]):
        instance (list[str] | Unset):
        host (list[str] | Unset):
        status_code (list[str] | Unset):
        method (list[str] | Unset):
        task (list[str] | Unset):
        task_run (list[str] | Unset):
        sandbox (list[str] | Unset):
        build (list[str] | Unset):
        level (list[str] | Unset):
        type_ (list[str] | Unset):
        text (list[str] | Unset):
        path (list[str] | Unset):
        limit (int | Unset): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[str]]
    """

    kwargs = _get_kwargs(
        owner_id=owner_id,
        label=label,
        start_time=start_time,
        end_time=end_time,
        direction=direction,
        resource=resource,
        instance=instance,
        host=host,
        status_code=status_code,
        method=method,
        task=task,
        task_run=task_run,
        sandbox=sandbox,
        build=build,
        level=level,
        type_=type_,
        text=text,
        path=path,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    owner_id: str,
    label: ListLogsValuesLabel,
    start_time: datetime.datetime | Unset = UNSET,
    end_time: datetime.datetime | Unset = UNSET,
    direction: LogDirection | Unset = UNSET,
    resource: list[str],
    instance: list[str] | Unset = UNSET,
    host: list[str] | Unset = UNSET,
    status_code: list[str] | Unset = UNSET,
    method: list[str] | Unset = UNSET,
    task: list[str] | Unset = UNSET,
    task_run: list[str] | Unset = UNSET,
    sandbox: list[str] | Unset = UNSET,
    build: list[str] | Unset = UNSET,
    level: list[str] | Unset = UNSET,
    type_: list[str] | Unset = UNSET,
    text: list[str] | Unset = UNSET,
    path: list[str] | Unset = UNSET,
    limit: int | Unset = 20,
) -> Error | list[str] | None:
    """List log label values

     List all values for a given log label in the logs matching the provided filters.

    Args:
        owner_id (str):
        label (ListLogsValuesLabel):
        start_time (datetime.datetime | Unset):  Example: 2021-06-17T08:15:30Z.
        end_time (datetime.datetime | Unset):  Example: 2021-06-17T08:30:30Z.
        direction (LogDirection | Unset):
        resource (list[str]):
        instance (list[str] | Unset):
        host (list[str] | Unset):
        status_code (list[str] | Unset):
        method (list[str] | Unset):
        task (list[str] | Unset):
        task_run (list[str] | Unset):
        sandbox (list[str] | Unset):
        build (list[str] | Unset):
        level (list[str] | Unset):
        type_ (list[str] | Unset):
        text (list[str] | Unset):
        path (list[str] | Unset):
        limit (int | Unset): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[str]
    """

    return (
        await asyncio_detailed(
            client=client,
            owner_id=owner_id,
            label=label,
            start_time=start_time,
            end_time=end_time,
            direction=direction,
            resource=resource,
            instance=instance,
            host=host,
            status_code=status_code,
            method=method,
            task=task,
            task_run=task_run,
            sandbox=sandbox,
            build=build,
            level=level,
            type_=type_,
            text=text,
            path=path,
            limit=limit,
        )
    ).parsed
