from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.deploy import Deploy
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    service_id: str,
    deploy_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/services/{service_id}/deploys/{deploy_id}/cancel",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Deploy, Error]]:
    if response.status_code == 200:
        response_200 = Deploy.from_dict(response.json())

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
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Deploy, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    service_id: str,
    deploy_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Deploy, Error]]:
    """Cancel deploy

     Cancel an in-progress deploy for a service.

    Not supported for cron jobs.

    Args:
        service_id (str):
        deploy_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Deploy, Error]]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        deploy_id=deploy_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    service_id: str,
    deploy_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Deploy, Error]]:
    """Cancel deploy

     Cancel an in-progress deploy for a service.

    Not supported for cron jobs.

    Args:
        service_id (str):
        deploy_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Deploy, Error]
    """

    return sync_detailed(
        service_id=service_id,
        deploy_id=deploy_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    service_id: str,
    deploy_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Deploy, Error]]:
    """Cancel deploy

     Cancel an in-progress deploy for a service.

    Not supported for cron jobs.

    Args:
        service_id (str):
        deploy_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Deploy, Error]]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        deploy_id=deploy_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    service_id: str,
    deploy_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Deploy, Error]]:
    """Cancel deploy

     Cancel an in-progress deploy for a service.

    Not supported for cron jobs.

    Args:
        service_id (str):
        deploy_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Deploy, Error]
    """

    return (
        await asyncio_detailed(
            service_id=service_id,
            deploy_id=deploy_id,
            client=client,
        )
    ).parsed
