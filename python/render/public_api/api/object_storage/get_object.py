from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.get_object_output import GetObjectOutput
from ...models.region import Region
from ...types import Response


def _get_kwargs(
    owner_id: str,
    region: Region,
    key: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/objects/{owner_id}/{region}/{key}".format(
            owner_id=quote(str(owner_id), safe=""),
            region=quote(str(region), safe=""),
            key=quote(str(key), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Error | GetObjectOutput | None:
    if response.status_code == 200:
        response_200 = GetObjectOutput.from_dict(response.json())

        return response_200

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
) -> Response[Error | GetObjectOutput]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    owner_id: str,
    region: Region,
    key: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Error | GetObjectOutput]:
    """Get presigned URL to download an object

     Returns a presigned URL for downloading the object at the specified key.
    The object must begin being downloaded within the URL's expiration time.

    Args:
        owner_id (str):
        region (Region): Defaults to "oregon"
        key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GetObjectOutput]
    """

    kwargs = _get_kwargs(
        owner_id=owner_id,
        region=region,
        key=key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    owner_id: str,
    region: Region,
    key: str,
    *,
    client: AuthenticatedClient | Client,
) -> Error | GetObjectOutput | None:
    """Get presigned URL to download an object

     Returns a presigned URL for downloading the object at the specified key.
    The object must begin being downloaded within the URL's expiration time.

    Args:
        owner_id (str):
        region (Region): Defaults to "oregon"
        key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GetObjectOutput
    """

    return sync_detailed(
        owner_id=owner_id,
        region=region,
        key=key,
        client=client,
    ).parsed


async def asyncio_detailed(
    owner_id: str,
    region: Region,
    key: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Error | GetObjectOutput]:
    """Get presigned URL to download an object

     Returns a presigned URL for downloading the object at the specified key.
    The object must begin being downloaded within the URL's expiration time.

    Args:
        owner_id (str):
        region (Region): Defaults to "oregon"
        key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GetObjectOutput]
    """

    kwargs = _get_kwargs(
        owner_id=owner_id,
        region=region,
        key=key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    owner_id: str,
    region: Region,
    key: str,
    *,
    client: AuthenticatedClient | Client,
) -> Error | GetObjectOutput | None:
    """Get presigned URL to download an object

     Returns a presigned URL for downloading the object at the specified key.
    The object must begin being downloaded within the URL's expiration time.

    Args:
        owner_id (str):
        region (Region): Defaults to "oregon"
        key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GetObjectOutput
    """

    return (
        await asyncio_detailed(
            owner_id=owner_id,
            region=region,
            key=key,
            client=client,
        )
    ).parsed
