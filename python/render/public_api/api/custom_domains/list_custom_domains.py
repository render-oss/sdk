import datetime
from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

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
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
    name: Union[Unset, list[str]] = UNSET,
    domain_type: Union[Unset, ListCustomDomainsDomainType] = UNSET,
    verification_status: Union[Unset, ListCustomDomainsVerificationStatus] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    created_after: Union[Unset, datetime.datetime] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["cursor"] = cursor

    params["limit"] = limit

    json_name: Union[Unset, list[str]] = UNSET
    if not isinstance(name, Unset):
        json_name = name

    params["name"] = json_name

    json_domain_type: Union[Unset, str] = UNSET
    if not isinstance(domain_type, Unset):
        json_domain_type = domain_type.value

    params["domainType"] = json_domain_type

    json_verification_status: Union[Unset, str] = UNSET
    if not isinstance(verification_status, Unset):
        json_verification_status = verification_status.value

    params["verificationStatus"] = json_verification_status

    json_created_before: Union[Unset, str] = UNSET
    if not isinstance(created_before, Unset):
        json_created_before = created_before.isoformat()
    params["createdBefore"] = json_created_before

    json_created_after: Union[Unset, str] = UNSET
    if not isinstance(created_after, Unset):
        json_created_after = created_after.isoformat()
    params["createdAfter"] = json_created_after

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/services/{service_id}/custom-domains",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, list["CustomDomainWithCursor"]]]:
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
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Error, list["CustomDomainWithCursor"]]]:
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
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
    name: Union[Unset, list[str]] = UNSET,
    domain_type: Union[Unset, ListCustomDomainsDomainType] = UNSET,
    verification_status: Union[Unset, ListCustomDomainsVerificationStatus] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    created_after: Union[Unset, datetime.datetime] = UNSET,
) -> Response[Union[Error, list["CustomDomainWithCursor"]]]:
    """List custom domains

     List a particular service's custom domains that match the provided filters. If no filters are
    provided, all custom domains for the service are returned.

    Args:
        service_id (str):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.
        name (Union[Unset, list[str]]):
        domain_type (Union[Unset, ListCustomDomainsDomainType]):
        verification_status (Union[Unset, ListCustomDomainsVerificationStatus]):
        created_before (Union[Unset, datetime.datetime]):
        created_after (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, list['CustomDomainWithCursor']]]
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
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
    name: Union[Unset, list[str]] = UNSET,
    domain_type: Union[Unset, ListCustomDomainsDomainType] = UNSET,
    verification_status: Union[Unset, ListCustomDomainsVerificationStatus] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    created_after: Union[Unset, datetime.datetime] = UNSET,
) -> Optional[Union[Error, list["CustomDomainWithCursor"]]]:
    """List custom domains

     List a particular service's custom domains that match the provided filters. If no filters are
    provided, all custom domains for the service are returned.

    Args:
        service_id (str):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.
        name (Union[Unset, list[str]]):
        domain_type (Union[Unset, ListCustomDomainsDomainType]):
        verification_status (Union[Unset, ListCustomDomainsVerificationStatus]):
        created_before (Union[Unset, datetime.datetime]):
        created_after (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, list['CustomDomainWithCursor']]
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
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
    name: Union[Unset, list[str]] = UNSET,
    domain_type: Union[Unset, ListCustomDomainsDomainType] = UNSET,
    verification_status: Union[Unset, ListCustomDomainsVerificationStatus] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    created_after: Union[Unset, datetime.datetime] = UNSET,
) -> Response[Union[Error, list["CustomDomainWithCursor"]]]:
    """List custom domains

     List a particular service's custom domains that match the provided filters. If no filters are
    provided, all custom domains for the service are returned.

    Args:
        service_id (str):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.
        name (Union[Unset, list[str]]):
        domain_type (Union[Unset, ListCustomDomainsDomainType]):
        verification_status (Union[Unset, ListCustomDomainsVerificationStatus]):
        created_before (Union[Unset, datetime.datetime]):
        created_after (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, list['CustomDomainWithCursor']]]
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
    client: Union[AuthenticatedClient, Client],
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
    name: Union[Unset, list[str]] = UNSET,
    domain_type: Union[Unset, ListCustomDomainsDomainType] = UNSET,
    verification_status: Union[Unset, ListCustomDomainsVerificationStatus] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    created_after: Union[Unset, datetime.datetime] = UNSET,
) -> Optional[Union[Error, list["CustomDomainWithCursor"]]]:
    """List custom domains

     List a particular service's custom domains that match the provided filters. If no filters are
    provided, all custom domains for the service are returned.

    Args:
        service_id (str):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.
        name (Union[Unset, list[str]]):
        domain_type (Union[Unset, ListCustomDomainsDomainType]):
        verification_status (Union[Unset, ListCustomDomainsVerificationStatus]):
        created_before (Union[Unset, datetime.datetime]):
        created_after (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, list['CustomDomainWithCursor']]
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
