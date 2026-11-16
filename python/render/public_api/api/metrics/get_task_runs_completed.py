import datetime
from http import HTTPStatus
from typing import Any

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.get_task_runs_completed_aggregate_by import GetTaskRunsCompletedAggregateBy
from ...models.get_task_runs_completed_state import GetTaskRunsCompletedState
from ...models.time_series import TimeSeries
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    start_time: datetime.datetime | Unset = UNSET,
    end_time: datetime.datetime | Unset = UNSET,
    resolution_seconds: float | Unset = 60.0,
    resource: str | Unset = UNSET,
    state: GetTaskRunsCompletedState | Unset = UNSET,
    aggregate_by: GetTaskRunsCompletedAggregateBy | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_start_time: str | Unset = UNSET
    if not isinstance(start_time, Unset):
        json_start_time = start_time.isoformat()
    params["startTime"] = json_start_time

    json_end_time: str | Unset = UNSET
    if not isinstance(end_time, Unset):
        json_end_time = end_time.isoformat()
    params["endTime"] = json_end_time

    params["resolutionSeconds"] = resolution_seconds

    params["resource"] = resource

    json_state: str | Unset = UNSET
    if not isinstance(state, Unset):
        json_state = state.value

    params["state"] = json_state

    json_aggregate_by: str | Unset = UNSET
    if not isinstance(aggregate_by, Unset):
        json_aggregate_by = aggregate_by.value

    params["aggregateBy"] = json_aggregate_by

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/metrics/task-runs-completed",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Error | list[TimeSeries] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemastime_series_collection_item_data in _response_200:
            componentsschemastime_series_collection_item = TimeSeries.from_dict(
                componentsschemastime_series_collection_item_data
            )

            response_200.append(componentsschemastime_series_collection_item)

        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Response[Error | list[TimeSeries]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    start_time: datetime.datetime | Unset = UNSET,
    end_time: datetime.datetime | Unset = UNSET,
    resolution_seconds: float | Unset = 60.0,
    resource: str | Unset = UNSET,
    state: GetTaskRunsCompletedState | Unset = UNSET,
    aggregate_by: GetTaskRunsCompletedAggregateBy | Unset = UNSET,
) -> Response[Error | list[TimeSeries]]:
    """Get task runs completed count

     Get the total number of task runs completed for one or more tasks. Optionally filter by state
    (succeeded/failed) or aggregate by state.

    Args:
        start_time (datetime.datetime | Unset):  Example: 2021-06-17T08:15:30Z.
        end_time (datetime.datetime | Unset):  Example: 2021-06-17T08:30:30Z.
        resolution_seconds (float | Unset):  Default: 60.0. Example: 60.
        resource (str | Unset):  Example: tsk-xxxxx.
        state (GetTaskRunsCompletedState | Unset):
        aggregate_by (GetTaskRunsCompletedAggregateBy | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[TimeSeries]]
    """

    kwargs = _get_kwargs(
        start_time=start_time,
        end_time=end_time,
        resolution_seconds=resolution_seconds,
        resource=resource,
        state=state,
        aggregate_by=aggregate_by,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    start_time: datetime.datetime | Unset = UNSET,
    end_time: datetime.datetime | Unset = UNSET,
    resolution_seconds: float | Unset = 60.0,
    resource: str | Unset = UNSET,
    state: GetTaskRunsCompletedState | Unset = UNSET,
    aggregate_by: GetTaskRunsCompletedAggregateBy | Unset = UNSET,
) -> Error | list[TimeSeries] | None:
    """Get task runs completed count

     Get the total number of task runs completed for one or more tasks. Optionally filter by state
    (succeeded/failed) or aggregate by state.

    Args:
        start_time (datetime.datetime | Unset):  Example: 2021-06-17T08:15:30Z.
        end_time (datetime.datetime | Unset):  Example: 2021-06-17T08:30:30Z.
        resolution_seconds (float | Unset):  Default: 60.0. Example: 60.
        resource (str | Unset):  Example: tsk-xxxxx.
        state (GetTaskRunsCompletedState | Unset):
        aggregate_by (GetTaskRunsCompletedAggregateBy | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[TimeSeries]
    """

    return sync_detailed(
        client=client,
        start_time=start_time,
        end_time=end_time,
        resolution_seconds=resolution_seconds,
        resource=resource,
        state=state,
        aggregate_by=aggregate_by,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    start_time: datetime.datetime | Unset = UNSET,
    end_time: datetime.datetime | Unset = UNSET,
    resolution_seconds: float | Unset = 60.0,
    resource: str | Unset = UNSET,
    state: GetTaskRunsCompletedState | Unset = UNSET,
    aggregate_by: GetTaskRunsCompletedAggregateBy | Unset = UNSET,
) -> Response[Error | list[TimeSeries]]:
    """Get task runs completed count

     Get the total number of task runs completed for one or more tasks. Optionally filter by state
    (succeeded/failed) or aggregate by state.

    Args:
        start_time (datetime.datetime | Unset):  Example: 2021-06-17T08:15:30Z.
        end_time (datetime.datetime | Unset):  Example: 2021-06-17T08:30:30Z.
        resolution_seconds (float | Unset):  Default: 60.0. Example: 60.
        resource (str | Unset):  Example: tsk-xxxxx.
        state (GetTaskRunsCompletedState | Unset):
        aggregate_by (GetTaskRunsCompletedAggregateBy | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[TimeSeries]]
    """

    kwargs = _get_kwargs(
        start_time=start_time,
        end_time=end_time,
        resolution_seconds=resolution_seconds,
        resource=resource,
        state=state,
        aggregate_by=aggregate_by,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    start_time: datetime.datetime | Unset = UNSET,
    end_time: datetime.datetime | Unset = UNSET,
    resolution_seconds: float | Unset = 60.0,
    resource: str | Unset = UNSET,
    state: GetTaskRunsCompletedState | Unset = UNSET,
    aggregate_by: GetTaskRunsCompletedAggregateBy | Unset = UNSET,
) -> Error | list[TimeSeries] | None:
    """Get task runs completed count

     Get the total number of task runs completed for one or more tasks. Optionally filter by state
    (succeeded/failed) or aggregate by state.

    Args:
        start_time (datetime.datetime | Unset):  Example: 2021-06-17T08:15:30Z.
        end_time (datetime.datetime | Unset):  Example: 2021-06-17T08:30:30Z.
        resolution_seconds (float | Unset):  Default: 60.0. Example: 60.
        resource (str | Unset):  Example: tsk-xxxxx.
        state (GetTaskRunsCompletedState | Unset):
        aggregate_by (GetTaskRunsCompletedAggregateBy | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[TimeSeries]
    """

    return (
        await asyncio_detailed(
            client=client,
            start_time=start_time,
            end_time=end_time,
            resolution_seconds=resolution_seconds,
            resource=resource,
            state=state,
            aggregate_by=aggregate_by,
        )
    ).parsed
