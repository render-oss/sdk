from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.webhook import Webhook
from ...models.webhook_patch_input import WebhookPATCHInput
from ...types import Response


def _get_kwargs(
    webhook_id: str,
    *,
    body: WebhookPATCHInput,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": f"/webhooks/{webhook_id}",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, Webhook]]:
    if response.status_code == 200:
        response_200 = Webhook.from_dict(response.json())

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
) -> Response[Union[Error, Webhook]]:
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
    body: WebhookPATCHInput,
) -> Response[Union[Error, Webhook]]:
    """Update a webhook

     Update the webhook with the provided ID.

    Args:
        webhook_id (str):  Example: whk-d04m9b1r0fns73ckp94f.
        body (WebhookPATCHInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, Webhook]]
    """

    kwargs = _get_kwargs(
        webhook_id=webhook_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    webhook_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: WebhookPATCHInput,
) -> Optional[Union[Error, Webhook]]:
    """Update a webhook

     Update the webhook with the provided ID.

    Args:
        webhook_id (str):  Example: whk-d04m9b1r0fns73ckp94f.
        body (WebhookPATCHInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, Webhook]
    """

    return sync_detailed(
        webhook_id=webhook_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    webhook_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: WebhookPATCHInput,
) -> Response[Union[Error, Webhook]]:
    """Update a webhook

     Update the webhook with the provided ID.

    Args:
        webhook_id (str):  Example: whk-d04m9b1r0fns73ckp94f.
        body (WebhookPATCHInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, Webhook]]
    """

    kwargs = _get_kwargs(
        webhook_id=webhook_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    webhook_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: WebhookPATCHInput,
) -> Optional[Union[Error, Webhook]]:
    """Update a webhook

     Update the webhook with the provided ID.

    Args:
        webhook_id (str):  Example: whk-d04m9b1r0fns73ckp94f.
        body (WebhookPATCHInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, Webhook]
    """

    return (
        await asyncio_detailed(
            webhook_id=webhook_id,
            client=client,
            body=body,
        )
    ).parsed
