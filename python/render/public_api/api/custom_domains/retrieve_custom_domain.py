from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.custom_domain import CustomDomain
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    service_id: str,
    custom_domain_name_or_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/services/{service_id}/custom-domains/{custom_domain_name_or_id}".format(
            service_id=quote(str(service_id), safe=""),
            custom_domain_name_or_id=quote(str(custom_domain_name_or_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx2.Response) -> CustomDomain | Error | None:
    if response.status_code == 200:
        response_200 = CustomDomain.from_dict(response.json())

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

    if response.status_code == 406:
        response_406 = Error.from_dict(response.json())

        return response_406

    if response.status_code == 410:
        response_410 = Error.from_dict(response.json())

        return response_410

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
) -> Response[CustomDomain | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    service_id: str,
    custom_domain_name_or_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[CustomDomain | Error]:
    """Retrieve custom domain

     Retrieve a particular custom domain for a particular service.

    Args:
        service_id (str):
        custom_domain_name_or_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CustomDomain | Error]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        custom_domain_name_or_id=custom_domain_name_or_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    service_id: str,
    custom_domain_name_or_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> CustomDomain | Error | None:
    """Retrieve custom domain

     Retrieve a particular custom domain for a particular service.

    Args:
        service_id (str):
        custom_domain_name_or_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CustomDomain | Error
    """

    return sync_detailed(
        service_id=service_id,
        custom_domain_name_or_id=custom_domain_name_or_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    service_id: str,
    custom_domain_name_or_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[CustomDomain | Error]:
    """Retrieve custom domain

     Retrieve a particular custom domain for a particular service.

    Args:
        service_id (str):
        custom_domain_name_or_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CustomDomain | Error]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        custom_domain_name_or_id=custom_domain_name_or_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    service_id: str,
    custom_domain_name_or_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> CustomDomain | Error | None:
    """Retrieve custom domain

     Retrieve a particular custom domain for a particular service.

    Args:
        service_id (str):
        custom_domain_name_or_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CustomDomain | Error
    """

    return (
        await asyncio_detailed(
            service_id=service_id,
            custom_domain_name_or_id=custom_domain_name_or_id,
            client=client,
        )
    ).parsed
