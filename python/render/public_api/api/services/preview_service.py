from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.preview_input import PreviewInput
from ...types import Response


def _get_kwargs(
    service_id: str,
    *,
    body: PreviewInput,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/services/{service_id}/preview",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Error]:
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


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    service_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: PreviewInput,
) -> Response[Error]:
    """Create service preview (image-backed)

     Create a preview instance for an image-backed service. The preview uses the settings of the base
    service (referenced by `serviceId`), except settings overridden via provided parameters.

    View all active previews from your service's Previews tab in the Render Dashboard.

    Note that you can't create previews for Git-backed services using the Render API.

    Args:
        service_id (str):
        body (PreviewInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    service_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: PreviewInput,
) -> Optional[Error]:
    """Create service preview (image-backed)

     Create a preview instance for an image-backed service. The preview uses the settings of the base
    service (referenced by `serviceId`), except settings overridden via provided parameters.

    View all active previews from your service's Previews tab in the Render Dashboard.

    Note that you can't create previews for Git-backed services using the Render API.

    Args:
        service_id (str):
        body (PreviewInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error
    """

    return sync_detailed(
        service_id=service_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    service_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: PreviewInput,
) -> Response[Error]:
    """Create service preview (image-backed)

     Create a preview instance for an image-backed service. The preview uses the settings of the base
    service (referenced by `serviceId`), except settings overridden via provided parameters.

    View all active previews from your service's Previews tab in the Render Dashboard.

    Note that you can't create previews for Git-backed services using the Render API.

    Args:
        service_id (str):
        body (PreviewInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    service_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: PreviewInput,
) -> Optional[Error]:
    """Create service preview (image-backed)

     Create a preview instance for an image-backed service. The preview uses the settings of the base
    service (referenced by `serviceId`), except settings overridden via provided parameters.

    View all active previews from your service's Previews tab in the Render Dashboard.

    Note that you can't create previews for Git-backed services using the Render API.

    Args:
        service_id (str):
        body (PreviewInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error
    """

    return (
        await asyncio_detailed(
            service_id=service_id,
            client=client,
            body=body,
        )
    ).parsed
