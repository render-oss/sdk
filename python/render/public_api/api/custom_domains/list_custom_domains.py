import datetime
from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.custom_domain_with_cursor import CustomDomainWithCursor
from ...models.error import Error
from ...models.list_custom_domains_domain_type import ListCustomDomainsDomainType
from ...models.list_custom_domains_verification_status import ListCustomDomainsVerificationStatus
from ...types import UNSET, Response, Unset


def _get_kwargs(
    service_id: str,
    *,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 20,
    name: list[str] | Unset = UNSET,
    domain_type: ListCustomDomainsDomainType | Unset = UNSET,
    verification_status: ListCustomDomainsVerificationStatus | Unset = UNSET,
    created_before: datetime.datetime | Unset = UNSET,
    created_after: datetime.datetime | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["cursor"] = cursor

    params["limit"] = limit

    json_name: list[str] | Unset = UNSET
    if not isinstance(name, Unset):
        json_name = name

    params["name"] = json_name

    json_domain_type: str | Unset = UNSET
    if not isinstance(domain_type, Unset):
        json_domain_type = domain_type.value

    params["domainType"] = json_domain_type

    json_verification_status: str | Unset = UNSET
    if not isinstance(verification_status, Unset):
        json_verification_status = verification_status.value

    params["verificationStatus"] = json_verification_status

    json_created_before: str | Unset = UNSET
    if not isinstance(created_before, Unset):
        json_created_before = created_before.isoformat()
    params["createdBefore"] = json_created_before

    json_created_after: str | Unset = UNSET
    if not isinstance(created_after, Unset):
        json_created_after = created_after.isoformat()
    params["createdAfter"] = json_created_after

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/services/{service_id}/custom-domains".format(
            service_id=quote(str(service_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Error | list[CustomDomainWithCursor] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = CustomDomainWithCursor.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[Error | list[CustomDomainWithCursor]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    service_id: str,
    *,
    client: AuthenticatedClient | Client,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 20,
    name: list[str] | Unset = UNSET,
    domain_type: ListCustomDomainsDomainType | Unset = UNSET,
    verification_status: ListCustomDomainsVerificationStatus | Unset = UNSET,
    created_before: datetime.datetime | Unset = UNSET,
    created_after: datetime.datetime | Unset = UNSET,
) -> Response[Error | list[CustomDomainWithCursor]]:
    """List custom domains

     List a particular service's custom domains that match the provided filters. If no filters are
    provided, all custom domains for the service are returned.

    Args:
        service_id (str):
        cursor (str | Unset):
        limit (int | Unset): Defaults to 20 Default: 20.
        name (list[str] | Unset):
        domain_type (ListCustomDomainsDomainType | Unset):
        verification_status (ListCustomDomainsVerificationStatus | Unset):
        created_before (datetime.datetime | Unset):
        created_after (datetime.datetime | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[CustomDomainWithCursor]]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        cursor=cursor,
        limit=limit,
        name=name,
        domain_type=domain_type,
        verification_status=verification_status,
        created_before=created_before,
        created_after=created_after,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    service_id: str,
    *,
    client: AuthenticatedClient | Client,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 20,
    name: list[str] | Unset = UNSET,
    domain_type: ListCustomDomainsDomainType | Unset = UNSET,
    verification_status: ListCustomDomainsVerificationStatus | Unset = UNSET,
    created_before: datetime.datetime | Unset = UNSET,
    created_after: datetime.datetime | Unset = UNSET,
) -> Error | list[CustomDomainWithCursor] | None:
    """List custom domains

     List a particular service's custom domains that match the provided filters. If no filters are
    provided, all custom domains for the service are returned.

    Args:
        service_id (str):
        cursor (str | Unset):
        limit (int | Unset): Defaults to 20 Default: 20.
        name (list[str] | Unset):
        domain_type (ListCustomDomainsDomainType | Unset):
        verification_status (ListCustomDomainsVerificationStatus | Unset):
        created_before (datetime.datetime | Unset):
        created_after (datetime.datetime | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[CustomDomainWithCursor]
    """

    return sync_detailed(
        service_id=service_id,
        client=client,
        cursor=cursor,
        limit=limit,
        name=name,
        domain_type=domain_type,
        verification_status=verification_status,
        created_before=created_before,
        created_after=created_after,
    ).parsed


async def asyncio_detailed(
    service_id: str,
    *,
    client: AuthenticatedClient | Client,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 20,
    name: list[str] | Unset = UNSET,
    domain_type: ListCustomDomainsDomainType | Unset = UNSET,
    verification_status: ListCustomDomainsVerificationStatus | Unset = UNSET,
    created_before: datetime.datetime | Unset = UNSET,
    created_after: datetime.datetime | Unset = UNSET,
) -> Response[Error | list[CustomDomainWithCursor]]:
    """List custom domains

     List a particular service's custom domains that match the provided filters. If no filters are
    provided, all custom domains for the service are returned.

    Args:
        service_id (str):
        cursor (str | Unset):
        limit (int | Unset): Defaults to 20 Default: 20.
        name (list[str] | Unset):
        domain_type (ListCustomDomainsDomainType | Unset):
        verification_status (ListCustomDomainsVerificationStatus | Unset):
        created_before (datetime.datetime | Unset):
        created_after (datetime.datetime | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[CustomDomainWithCursor]]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        cursor=cursor,
        limit=limit,
        name=name,
        domain_type=domain_type,
        verification_status=verification_status,
        created_before=created_before,
        created_after=created_after,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    service_id: str,
    *,
    client: AuthenticatedClient | Client,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 20,
    name: list[str] | Unset = UNSET,
    domain_type: ListCustomDomainsDomainType | Unset = UNSET,
    verification_status: ListCustomDomainsVerificationStatus | Unset = UNSET,
    created_before: datetime.datetime | Unset = UNSET,
    created_after: datetime.datetime | Unset = UNSET,
) -> Error | list[CustomDomainWithCursor] | None:
    """List custom domains

     List a particular service's custom domains that match the provided filters. If no filters are
    provided, all custom domains for the service are returned.

    Args:
        service_id (str):
        cursor (str | Unset):
        limit (int | Unset): Defaults to 20 Default: 20.
        name (list[str] | Unset):
        domain_type (ListCustomDomainsDomainType | Unset):
        verification_status (ListCustomDomainsVerificationStatus | Unset):
        created_before (datetime.datetime | Unset):
        created_after (datetime.datetime | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[CustomDomainWithCursor]
    """

    return (
        await asyncio_detailed(
            service_id=service_id,
            client=client,
            cursor=cursor,
            limit=limit,
            name=name,
            domain_type=domain_type,
            verification_status=verification_status,
            created_before=created_before,
            created_after=created_after,
        )
    ).parsed
