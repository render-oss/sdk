import datetime
from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.stream_sandbox_logs_accept import StreamSandboxLogsAccept
from ...types import UNSET, Response, Unset


def _get_kwargs(
    sandbox_id: str,
    *,
    since: Union[Unset, datetime.datetime] = UNSET,
    follow: Union[Unset, bool] = True,
    exec_id: Union[Unset, str] = UNSET,
    accept: Union[Unset, StreamSandboxLogsAccept] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(accept, Unset):
        headers["Accept"] = str(accept)

    params: dict[str, Any] = {}

    json_since: Union[Unset, str] = UNSET
    if not isinstance(since, Unset):
        json_since = since.isoformat()
    params["since"] = json_since

    params["follow"] = follow

    params["execId"] = exec_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/sandboxes/{sandbox_id}/logs",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, str]]:
    if response.status_code == 200:
        response_200 = response.text
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
) -> Response[Union[Error, str]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    sandbox_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    since: Union[Unset, datetime.datetime] = UNSET,
    follow: Union[Unset, bool] = True,
    exec_id: Union[Unset, str] = UNSET,
    accept: Union[Unset, StreamSandboxLogsAccept] = UNSET,
) -> Response[Union[Error, str]]:
    """Stream sandbox logs and lifecycle events

     Stream sandbox output and lifecycle events as a server-sent event stream.
    Replays historical events from sandbox creation (or from `since`), then
    continues live. The stream closes after the `terminated` or `errored`
    lifecycle event.

    Args:
        sandbox_id (str):  Example: sbx-cph1rs3idesc73a2b2mg.
        since (Union[Unset, datetime.datetime]):
        follow (Union[Unset, bool]):  Default: True.
        exec_id (Union[Unset, str]):
        accept (Union[Unset, StreamSandboxLogsAccept]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, str]]
    """

    kwargs = _get_kwargs(
        sandbox_id=sandbox_id,
        since=since,
        follow=follow,
        exec_id=exec_id,
        accept=accept,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    sandbox_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    since: Union[Unset, datetime.datetime] = UNSET,
    follow: Union[Unset, bool] = True,
    exec_id: Union[Unset, str] = UNSET,
    accept: Union[Unset, StreamSandboxLogsAccept] = UNSET,
) -> Optional[Union[Error, str]]:
    """Stream sandbox logs and lifecycle events

     Stream sandbox output and lifecycle events as a server-sent event stream.
    Replays historical events from sandbox creation (or from `since`), then
    continues live. The stream closes after the `terminated` or `errored`
    lifecycle event.

    Args:
        sandbox_id (str):  Example: sbx-cph1rs3idesc73a2b2mg.
        since (Union[Unset, datetime.datetime]):
        follow (Union[Unset, bool]):  Default: True.
        exec_id (Union[Unset, str]):
        accept (Union[Unset, StreamSandboxLogsAccept]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, str]
    """

    return sync_detailed(
        sandbox_id=sandbox_id,
        client=client,
        since=since,
        follow=follow,
        exec_id=exec_id,
        accept=accept,
    ).parsed


async def asyncio_detailed(
    sandbox_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    since: Union[Unset, datetime.datetime] = UNSET,
    follow: Union[Unset, bool] = True,
    exec_id: Union[Unset, str] = UNSET,
    accept: Union[Unset, StreamSandboxLogsAccept] = UNSET,
) -> Response[Union[Error, str]]:
    """Stream sandbox logs and lifecycle events

     Stream sandbox output and lifecycle events as a server-sent event stream.
    Replays historical events from sandbox creation (or from `since`), then
    continues live. The stream closes after the `terminated` or `errored`
    lifecycle event.

    Args:
        sandbox_id (str):  Example: sbx-cph1rs3idesc73a2b2mg.
        since (Union[Unset, datetime.datetime]):
        follow (Union[Unset, bool]):  Default: True.
        exec_id (Union[Unset, str]):
        accept (Union[Unset, StreamSandboxLogsAccept]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, str]]
    """

    kwargs = _get_kwargs(
        sandbox_id=sandbox_id,
        since=since,
        follow=follow,
        exec_id=exec_id,
        accept=accept,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    sandbox_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    since: Union[Unset, datetime.datetime] = UNSET,
    follow: Union[Unset, bool] = True,
    exec_id: Union[Unset, str] = UNSET,
    accept: Union[Unset, StreamSandboxLogsAccept] = UNSET,
) -> Optional[Union[Error, str]]:
    """Stream sandbox logs and lifecycle events

     Stream sandbox output and lifecycle events as a server-sent event stream.
    Replays historical events from sandbox creation (or from `since`), then
    continues live. The stream closes after the `terminated` or `errored`
    lifecycle event.

    Args:
        sandbox_id (str):  Example: sbx-cph1rs3idesc73a2b2mg.
        since (Union[Unset, datetime.datetime]):
        follow (Union[Unset, bool]):  Default: True.
        exec_id (Union[Unset, str]):
        accept (Union[Unset, StreamSandboxLogsAccept]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, str]
    """

    return (
        await asyncio_detailed(
            sandbox_id=sandbox_id,
            client=client,
            since=since,
            follow=follow,
            exec_id=exec_id,
            accept=accept,
        )
    ).parsed
