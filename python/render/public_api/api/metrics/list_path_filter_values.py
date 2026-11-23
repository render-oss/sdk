import datetime
from http import HTTPStatus
from typing import Any, cast

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    start_time: datetime.datetime | Unset = UNSET,
    end_time: datetime.datetime | Unset = UNSET,
    resolution_seconds: float | Unset = 60.0,
    resource: str | Unset = UNSET,
    service: str | Unset = UNSET,
    project: str | Unset = UNSET,
    environment: str | Unset = UNSET,
    host: str | Unset = UNSET,
    status_code: str | Unset = UNSET,
    path: str | Unset = UNSET,
    region: str | Unset = UNSET,
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

    params["service"] = service

    params["project"] = project

    params["environment"] = environment

    params["host"] = host

    params["statusCode"] = status_code

    params["path"] = path

    params["region"] = region

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/metrics/filters/path",
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

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())

        return response_500

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
    start_time: datetime.datetime | Unset = UNSET,
    end_time: datetime.datetime | Unset = UNSET,
    resolution_seconds: float | Unset = 60.0,
    resource: str | Unset = UNSET,
    service: str | Unset = UNSET,
    project: str | Unset = UNSET,
    environment: str | Unset = UNSET,
    host: str | Unset = UNSET,
    status_code: str | Unset = UNSET,
    path: str | Unset = UNSET,
    region: str | Unset = UNSET,
) -> Response[Error | list[str]]:
    """List queryable paths

     The path suggestions are based on the most recent 5000 log lines as filtered by the provided filters

    Args:
        start_time (datetime.datetime | Unset):  Example: 2021-06-17T08:15:30Z.
        end_time (datetime.datetime | Unset):  Example: 2021-06-17T08:30:30Z.
        resolution_seconds (float | Unset):  Default: 60.0. Example: 60.
        resource (str | Unset):  Example: srv-xxxxx.
        service (str | Unset):  Example: srv-xxxxx.
        project (str | Unset):  Example: prj-xxxxx.
        environment (str | Unset):  Example: evm-xxxxx.
        host (str | Unset):  Example: example.com.
        status_code (str | Unset):  Example: 200.
        path (str | Unset):  Example: /graphql.
        region (str | Unset):  Example: oregon.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[str]]
    """

    kwargs = _get_kwargs(
        start_time=start_time,
        end_time=end_time,
        resolution_seconds=resolution_seconds,
        resource=resource,
        service=service,
        project=project,
        environment=environment,
        host=host,
        status_code=status_code,
        path=path,
        region=region,
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
    service: str | Unset = UNSET,
    project: str | Unset = UNSET,
    environment: str | Unset = UNSET,
    host: str | Unset = UNSET,
    status_code: str | Unset = UNSET,
    path: str | Unset = UNSET,
    region: str | Unset = UNSET,
) -> Error | list[str] | None:
    """List queryable paths

     The path suggestions are based on the most recent 5000 log lines as filtered by the provided filters

    Args:
        start_time (datetime.datetime | Unset):  Example: 2021-06-17T08:15:30Z.
        end_time (datetime.datetime | Unset):  Example: 2021-06-17T08:30:30Z.
        resolution_seconds (float | Unset):  Default: 60.0. Example: 60.
        resource (str | Unset):  Example: srv-xxxxx.
        service (str | Unset):  Example: srv-xxxxx.
        project (str | Unset):  Example: prj-xxxxx.
        environment (str | Unset):  Example: evm-xxxxx.
        host (str | Unset):  Example: example.com.
        status_code (str | Unset):  Example: 200.
        path (str | Unset):  Example: /graphql.
        region (str | Unset):  Example: oregon.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[str]
    """

    return sync_detailed(
        client=client,
        start_time=start_time,
        end_time=end_time,
        resolution_seconds=resolution_seconds,
        resource=resource,
        service=service,
        project=project,
        environment=environment,
        host=host,
        status_code=status_code,
        path=path,
        region=region,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    start_time: datetime.datetime | Unset = UNSET,
    end_time: datetime.datetime | Unset = UNSET,
    resolution_seconds: float | Unset = 60.0,
    resource: str | Unset = UNSET,
    service: str | Unset = UNSET,
    project: str | Unset = UNSET,
    environment: str | Unset = UNSET,
    host: str | Unset = UNSET,
    status_code: str | Unset = UNSET,
    path: str | Unset = UNSET,
    region: str | Unset = UNSET,
) -> Response[Error | list[str]]:
    """List queryable paths

     The path suggestions are based on the most recent 5000 log lines as filtered by the provided filters

    Args:
        start_time (datetime.datetime | Unset):  Example: 2021-06-17T08:15:30Z.
        end_time (datetime.datetime | Unset):  Example: 2021-06-17T08:30:30Z.
        resolution_seconds (float | Unset):  Default: 60.0. Example: 60.
        resource (str | Unset):  Example: srv-xxxxx.
        service (str | Unset):  Example: srv-xxxxx.
        project (str | Unset):  Example: prj-xxxxx.
        environment (str | Unset):  Example: evm-xxxxx.
        host (str | Unset):  Example: example.com.
        status_code (str | Unset):  Example: 200.
        path (str | Unset):  Example: /graphql.
        region (str | Unset):  Example: oregon.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[str]]
    """

    kwargs = _get_kwargs(
        start_time=start_time,
        end_time=end_time,
        resolution_seconds=resolution_seconds,
        resource=resource,
        service=service,
        project=project,
        environment=environment,
        host=host,
        status_code=status_code,
        path=path,
        region=region,
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
    service: str | Unset = UNSET,
    project: str | Unset = UNSET,
    environment: str | Unset = UNSET,
    host: str | Unset = UNSET,
    status_code: str | Unset = UNSET,
    path: str | Unset = UNSET,
    region: str | Unset = UNSET,
) -> Error | list[str] | None:
    """List queryable paths

     The path suggestions are based on the most recent 5000 log lines as filtered by the provided filters

    Args:
        start_time (datetime.datetime | Unset):  Example: 2021-06-17T08:15:30Z.
        end_time (datetime.datetime | Unset):  Example: 2021-06-17T08:30:30Z.
        resolution_seconds (float | Unset):  Default: 60.0. Example: 60.
        resource (str | Unset):  Example: srv-xxxxx.
        service (str | Unset):  Example: srv-xxxxx.
        project (str | Unset):  Example: prj-xxxxx.
        environment (str | Unset):  Example: evm-xxxxx.
        host (str | Unset):  Example: example.com.
        status_code (str | Unset):  Example: 200.
        path (str | Unset):  Example: /graphql.
        region (str | Unset):  Example: oregon.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[str]
    """

    return (
        await asyncio_detailed(
            client=client,
            start_time=start_time,
            end_time=end_time,
            resolution_seconds=resolution_seconds,
            resource=resource,
            service=service,
            project=project,
            environment=environment,
            host=host,
            status_code=status_code,
            path=path,
            region=region,
        )
    ).parsed
