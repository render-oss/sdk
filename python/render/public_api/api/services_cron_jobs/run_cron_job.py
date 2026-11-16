from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.cron_job_run import CronJobRun
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    cron_job_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/cron-jobs/{cron_job_id}/runs".format(
            cron_job_id=quote(str(cron_job_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx2.Response) -> CronJobRun | Error | None:
    if response.status_code == 200:
        response_200 = CronJobRun.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 406:
        response_406 = Error.from_dict(response.json())

        return response_406

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx2.Response) -> Response[CronJobRun | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    cron_job_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[CronJobRun | Error]:
    """Trigger cron job run

     Trigger a run for a cron job and cancel any active runs.

    Args:
        cron_job_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CronJobRun | Error]
    """

    kwargs = _get_kwargs(
        cron_job_id=cron_job_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    cron_job_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> CronJobRun | Error | None:
    """Trigger cron job run

     Trigger a run for a cron job and cancel any active runs.

    Args:
        cron_job_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CronJobRun | Error
    """

    return sync_detailed(
        cron_job_id=cron_job_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    cron_job_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[CronJobRun | Error]:
    """Trigger cron job run

     Trigger a run for a cron job and cancel any active runs.

    Args:
        cron_job_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CronJobRun | Error]
    """

    kwargs = _get_kwargs(
        cron_job_id=cron_job_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    cron_job_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> CronJobRun | Error | None:
    """Trigger cron job run

     Trigger a run for a cron job and cancel any active runs.

    Args:
        cron_job_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CronJobRun | Error
    """

    return (
        await asyncio_detailed(
            cron_job_id=cron_job_id,
            client=client,
        )
    ).parsed
