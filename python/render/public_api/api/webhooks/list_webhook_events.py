import datetime
from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.webhook_event_with_cursor import WebhookEventWithCursor
from ...types import UNSET, Response, Unset


def _get_kwargs(
    webhook_id: str,
    *,
    sent_before: datetime.datetime | Unset = UNSET,
    sent_after: datetime.datetime | Unset = UNSET,
    limit: int | Unset = 20,
    cursor: str | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_sent_before: str | Unset = UNSET
    if not isinstance(sent_before, Unset):
        json_sent_before = sent_before.isoformat()
    params["sentBefore"] = json_sent_before

    json_sent_after: str | Unset = UNSET
    if not isinstance(sent_after, Unset):
        json_sent_after = sent_after.isoformat()
    params["sentAfter"] = json_sent_after

    params["limit"] = limit

    params["cursor"] = cursor

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/webhooks/{webhook_id}/events".format(
            webhook_id=quote(str(webhook_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Error | list[WebhookEventWithCursor] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = WebhookEventWithCursor.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

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
) -> Response[Error | list[WebhookEventWithCursor]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    webhook_id: str,
    *,
    client: AuthenticatedClient | Client,
    sent_before: datetime.datetime | Unset = UNSET,
    sent_after: datetime.datetime | Unset = UNSET,
    limit: int | Unset = 20,
    cursor: str | Unset = UNSET,
) -> Response[Error | list[WebhookEventWithCursor]]:
    """List webhook events

     Retrieve a list of events that have been sent to this webhook, with optional filtering by timestamp.

    Args:
        webhook_id (str):  Example: whk-d04m9b1r0fns73ckp94f.
        sent_before (datetime.datetime | Unset):
        sent_after (datetime.datetime | Unset):
        limit (int | Unset): Defaults to 20 Default: 20.
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[WebhookEventWithCursor]]
    """

    kwargs = _get_kwargs(
        webhook_id=webhook_id,
        sent_before=sent_before,
        sent_after=sent_after,
        limit=limit,
        cursor=cursor,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    webhook_id: str,
    *,
    client: AuthenticatedClient | Client,
    sent_before: datetime.datetime | Unset = UNSET,
    sent_after: datetime.datetime | Unset = UNSET,
    limit: int | Unset = 20,
    cursor: str | Unset = UNSET,
) -> Error | list[WebhookEventWithCursor] | None:
    """List webhook events

     Retrieve a list of events that have been sent to this webhook, with optional filtering by timestamp.

    Args:
        webhook_id (str):  Example: whk-d04m9b1r0fns73ckp94f.
        sent_before (datetime.datetime | Unset):
        sent_after (datetime.datetime | Unset):
        limit (int | Unset): Defaults to 20 Default: 20.
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[WebhookEventWithCursor]
    """

    return sync_detailed(
        webhook_id=webhook_id,
        client=client,
        sent_before=sent_before,
        sent_after=sent_after,
        limit=limit,
        cursor=cursor,
    ).parsed


async def asyncio_detailed(
    webhook_id: str,
    *,
    client: AuthenticatedClient | Client,
    sent_before: datetime.datetime | Unset = UNSET,
    sent_after: datetime.datetime | Unset = UNSET,
    limit: int | Unset = 20,
    cursor: str | Unset = UNSET,
) -> Response[Error | list[WebhookEventWithCursor]]:
    """List webhook events

     Retrieve a list of events that have been sent to this webhook, with optional filtering by timestamp.

    Args:
        webhook_id (str):  Example: whk-d04m9b1r0fns73ckp94f.
        sent_before (datetime.datetime | Unset):
        sent_after (datetime.datetime | Unset):
        limit (int | Unset): Defaults to 20 Default: 20.
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[WebhookEventWithCursor]]
    """

    kwargs = _get_kwargs(
        webhook_id=webhook_id,
        sent_before=sent_before,
        sent_after=sent_after,
        limit=limit,
        cursor=cursor,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    webhook_id: str,
    *,
    client: AuthenticatedClient | Client,
    sent_before: datetime.datetime | Unset = UNSET,
    sent_after: datetime.datetime | Unset = UNSET,
    limit: int | Unset = 20,
    cursor: str | Unset = UNSET,
) -> Error | list[WebhookEventWithCursor] | None:
    """List webhook events

     Retrieve a list of events that have been sent to this webhook, with optional filtering by timestamp.

    Args:
        webhook_id (str):  Example: whk-d04m9b1r0fns73ckp94f.
        sent_before (datetime.datetime | Unset):
        sent_after (datetime.datetime | Unset):
        limit (int | Unset): Defaults to 20 Default: 20.
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[WebhookEventWithCursor]
    """

    return (
        await asyncio_detailed(
            webhook_id=webhook_id,
            client=client,
            sent_before=sent_before,
            sent_after=sent_after,
            limit=limit,
            cursor=cursor,
        )
    ).parsed
