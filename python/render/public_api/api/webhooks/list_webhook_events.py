import datetime
from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.webhook_event_with_cursor import WebhookEventWithCursor
from ...types import UNSET, Response, Unset


def _get_kwargs(
    webhook_id: str,
    *,
    sent_before: Union[Unset, datetime.datetime] = UNSET,
    sent_after: Union[Unset, datetime.datetime] = UNSET,
    limit: Union[Unset, int] = 20,
    cursor: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_sent_before: Union[Unset, str] = UNSET
    if not isinstance(sent_before, Unset):
        json_sent_before = sent_before.isoformat()
    params["sentBefore"] = json_sent_before

    json_sent_after: Union[Unset, str] = UNSET
    if not isinstance(sent_after, Unset):
        json_sent_after = sent_after.isoformat()
    params["sentAfter"] = json_sent_after

    params["limit"] = limit

    params["cursor"] = cursor

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/webhooks/{webhook_id}/events",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, list["WebhookEventWithCursor"]]]:
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
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, list["WebhookEventWithCursor"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    webhook_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    sent_before: Union[Unset, datetime.datetime] = UNSET,
    sent_after: Union[Unset, datetime.datetime] = UNSET,
    limit: Union[Unset, int] = 20,
    cursor: Union[Unset, str] = UNSET,
) -> Response[Union[Error, list["WebhookEventWithCursor"]]]:
    """List webhook events

     Retrieve a list of events that have been sent to this webhook, with optional filtering by timestamp.

    Args:
        webhook_id (str):  Example: whk-d04m9b1r0fns73ckp94f.
        sent_before (Union[Unset, datetime.datetime]):
        sent_after (Union[Unset, datetime.datetime]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, list['WebhookEventWithCursor']]]
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
    client: Union[AuthenticatedClient, Client],
    sent_before: Union[Unset, datetime.datetime] = UNSET,
    sent_after: Union[Unset, datetime.datetime] = UNSET,
    limit: Union[Unset, int] = 20,
    cursor: Union[Unset, str] = UNSET,
) -> Optional[Union[Error, list["WebhookEventWithCursor"]]]:
    """List webhook events

     Retrieve a list of events that have been sent to this webhook, with optional filtering by timestamp.

    Args:
        webhook_id (str):  Example: whk-d04m9b1r0fns73ckp94f.
        sent_before (Union[Unset, datetime.datetime]):
        sent_after (Union[Unset, datetime.datetime]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, list['WebhookEventWithCursor']]
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
    client: Union[AuthenticatedClient, Client],
    sent_before: Union[Unset, datetime.datetime] = UNSET,
    sent_after: Union[Unset, datetime.datetime] = UNSET,
    limit: Union[Unset, int] = 20,
    cursor: Union[Unset, str] = UNSET,
) -> Response[Union[Error, list["WebhookEventWithCursor"]]]:
    """List webhook events

     Retrieve a list of events that have been sent to this webhook, with optional filtering by timestamp.

    Args:
        webhook_id (str):  Example: whk-d04m9b1r0fns73ckp94f.
        sent_before (Union[Unset, datetime.datetime]):
        sent_after (Union[Unset, datetime.datetime]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, list['WebhookEventWithCursor']]]
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
    client: Union[AuthenticatedClient, Client],
    sent_before: Union[Unset, datetime.datetime] = UNSET,
    sent_after: Union[Unset, datetime.datetime] = UNSET,
    limit: Union[Unset, int] = 20,
    cursor: Union[Unset, str] = UNSET,
) -> Optional[Union[Error, list["WebhookEventWithCursor"]]]:
    """List webhook events

     Retrieve a list of events that have been sent to this webhook, with optional filtering by timestamp.

    Args:
        webhook_id (str):  Example: whk-d04m9b1r0fns73ckp94f.
        sent_before (Union[Unset, datetime.datetime]):
        sent_after (Union[Unset, datetime.datetime]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, list['WebhookEventWithCursor']]
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
