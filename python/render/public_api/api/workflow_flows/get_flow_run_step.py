from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.flow_run_step_details import FlowRunStepDetails
from ...types import UNSET, Response, Unset


def _get_kwargs(
    flow_run_id: str,
    step_seq: int,
    *,
    step_key: str | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["stepKey"] = step_key

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/flow-runs/{flow_run_id}/steps/{step_seq}".format(
            flow_run_id=quote(str(flow_run_id), safe=""),
            step_seq=quote(str(step_seq), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Error | FlowRunStepDetails | None:
    if response.status_code == 200:
        response_200 = FlowRunStepDetails.from_dict(response.json())

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
) -> Response[Error | FlowRunStepDetails]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    flow_run_id: str,
    step_seq: int,
    *,
    client: AuthenticatedClient | Client,
    step_key: str | Unset = UNSET,
) -> Response[Error | FlowRunStepDetails]:
    """Retrieve flow run step

     Retrieve a single step of a flow run, including its input, result and error. A sequence number can
    cover more than one step, so pass the `stepKey` the step listing reported to address one of those.

    Args:
        flow_run_id (str):
        step_seq (int):
        step_key (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FlowRunStepDetails]
    """

    kwargs = _get_kwargs(
        flow_run_id=flow_run_id,
        step_seq=step_seq,
        step_key=step_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    flow_run_id: str,
    step_seq: int,
    *,
    client: AuthenticatedClient | Client,
    step_key: str | Unset = UNSET,
) -> Error | FlowRunStepDetails | None:
    """Retrieve flow run step

     Retrieve a single step of a flow run, including its input, result and error. A sequence number can
    cover more than one step, so pass the `stepKey` the step listing reported to address one of those.

    Args:
        flow_run_id (str):
        step_seq (int):
        step_key (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FlowRunStepDetails
    """

    return sync_detailed(
        flow_run_id=flow_run_id,
        step_seq=step_seq,
        client=client,
        step_key=step_key,
    ).parsed


async def asyncio_detailed(
    flow_run_id: str,
    step_seq: int,
    *,
    client: AuthenticatedClient | Client,
    step_key: str | Unset = UNSET,
) -> Response[Error | FlowRunStepDetails]:
    """Retrieve flow run step

     Retrieve a single step of a flow run, including its input, result and error. A sequence number can
    cover more than one step, so pass the `stepKey` the step listing reported to address one of those.

    Args:
        flow_run_id (str):
        step_seq (int):
        step_key (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FlowRunStepDetails]
    """

    kwargs = _get_kwargs(
        flow_run_id=flow_run_id,
        step_seq=step_seq,
        step_key=step_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    flow_run_id: str,
    step_seq: int,
    *,
    client: AuthenticatedClient | Client,
    step_key: str | Unset = UNSET,
) -> Error | FlowRunStepDetails | None:
    """Retrieve flow run step

     Retrieve a single step of a flow run, including its input, result and error. A sequence number can
    cover more than one step, so pass the `stepKey` the step listing reported to address one of those.

    Args:
        flow_run_id (str):
        step_seq (int):
        step_key (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FlowRunStepDetails
    """

    return (
        await asyncio_detailed(
            flow_run_id=flow_run_id,
            step_seq=step_seq,
            client=client,
            step_key=step_key,
        )
    ).parsed
