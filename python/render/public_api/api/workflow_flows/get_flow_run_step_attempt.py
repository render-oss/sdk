from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.flow_run_step_attempt_details import FlowRunStepAttemptDetails
from ...types import UNSET, Response, Unset


def _get_kwargs(
    flow_run_id: str,
    step_seq: int,
    attempt: int,
    *,
    step_key: str | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["stepKey"] = step_key

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/flow-runs/{flow_run_id}/steps/{step_seq}/attempts/{attempt}".format(
            flow_run_id=quote(str(flow_run_id), safe=""),
            step_seq=quote(str(step_seq), safe=""),
            attempt=quote(str(attempt), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Error | FlowRunStepAttemptDetails | None:
    if response.status_code == 200:
        response_200 = FlowRunStepAttemptDetails.from_dict(response.json())

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
) -> Response[Error | FlowRunStepAttemptDetails]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    flow_run_id: str,
    step_seq: int,
    attempt: int,
    *,
    client: AuthenticatedClient | Client,
    step_key: str | Unset = UNSET,
) -> Response[Error | FlowRunStepAttemptDetails]:
    """Retrieve recorded failed step attempt

    Args:
        flow_run_id (str):
        step_seq (int):
        attempt (int):
        step_key (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FlowRunStepAttemptDetails]
    """

    kwargs = _get_kwargs(
        flow_run_id=flow_run_id,
        step_seq=step_seq,
        attempt=attempt,
        step_key=step_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    flow_run_id: str,
    step_seq: int,
    attempt: int,
    *,
    client: AuthenticatedClient | Client,
    step_key: str | Unset = UNSET,
) -> Error | FlowRunStepAttemptDetails | None:
    """Retrieve recorded failed step attempt

    Args:
        flow_run_id (str):
        step_seq (int):
        attempt (int):
        step_key (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FlowRunStepAttemptDetails
    """

    return sync_detailed(
        flow_run_id=flow_run_id,
        step_seq=step_seq,
        attempt=attempt,
        client=client,
        step_key=step_key,
    ).parsed


async def asyncio_detailed(
    flow_run_id: str,
    step_seq: int,
    attempt: int,
    *,
    client: AuthenticatedClient | Client,
    step_key: str | Unset = UNSET,
) -> Response[Error | FlowRunStepAttemptDetails]:
    """Retrieve recorded failed step attempt

    Args:
        flow_run_id (str):
        step_seq (int):
        attempt (int):
        step_key (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FlowRunStepAttemptDetails]
    """

    kwargs = _get_kwargs(
        flow_run_id=flow_run_id,
        step_seq=step_seq,
        attempt=attempt,
        step_key=step_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    flow_run_id: str,
    step_seq: int,
    attempt: int,
    *,
    client: AuthenticatedClient | Client,
    step_key: str | Unset = UNSET,
) -> Error | FlowRunStepAttemptDetails | None:
    """Retrieve recorded failed step attempt

    Args:
        flow_run_id (str):
        step_seq (int):
        attempt (int):
        step_key (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FlowRunStepAttemptDetails
    """

    return (
        await asyncio_detailed(
            flow_run_id=flow_run_id,
            step_seq=step_seq,
            attempt=attempt,
            client=client,
            step_key=step_key,
        )
    ).parsed
