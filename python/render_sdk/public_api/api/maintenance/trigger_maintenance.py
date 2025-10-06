from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    maintenance_run_param: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/maintenance/{maintenance_run_param}/trigger",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Error]]:
    if response.status_code == 202:
        response_202 = cast(Any, None)
        return response_202

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
) -> Response[Union[Any, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    maintenance_run_param: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, Error]]:
    """Trigger maintenance run

     Trigger the scheduled maintenance run with the provided ID.

    Triggering maintenance is asynchronous. To check whether maintenance has started, use the [Retrieve
    maintenance run](https://api-docs.render.com/reference/retrieve-maintenance) endpoint.

    As maintenance progresses, the run's `state` will change from `scheduled` to other values, such as
    `in_progress` and `succeeded`.

    Args:
        maintenance_run_param (str):  Example: mrn-cph1rs3idesc73a2b2mg.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error]]
    """

    kwargs = _get_kwargs(
        maintenance_run_param=maintenance_run_param,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    maintenance_run_param: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, Error]]:
    """Trigger maintenance run

     Trigger the scheduled maintenance run with the provided ID.

    Triggering maintenance is asynchronous. To check whether maintenance has started, use the [Retrieve
    maintenance run](https://api-docs.render.com/reference/retrieve-maintenance) endpoint.

    As maintenance progresses, the run's `state` will change from `scheduled` to other values, such as
    `in_progress` and `succeeded`.

    Args:
        maintenance_run_param (str):  Example: mrn-cph1rs3idesc73a2b2mg.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error]
    """

    return sync_detailed(
        maintenance_run_param=maintenance_run_param,
        client=client,
    ).parsed


async def asyncio_detailed(
    maintenance_run_param: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, Error]]:
    """Trigger maintenance run

     Trigger the scheduled maintenance run with the provided ID.

    Triggering maintenance is asynchronous. To check whether maintenance has started, use the [Retrieve
    maintenance run](https://api-docs.render.com/reference/retrieve-maintenance) endpoint.

    As maintenance progresses, the run's `state` will change from `scheduled` to other values, such as
    `in_progress` and `succeeded`.

    Args:
        maintenance_run_param (str):  Example: mrn-cph1rs3idesc73a2b2mg.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error]]
    """

    kwargs = _get_kwargs(
        maintenance_run_param=maintenance_run_param,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    maintenance_run_param: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, Error]]:
    """Trigger maintenance run

     Trigger the scheduled maintenance run with the provided ID.

    Triggering maintenance is asynchronous. To check whether maintenance has started, use the [Retrieve
    maintenance run](https://api-docs.render.com/reference/retrieve-maintenance) endpoint.

    As maintenance progresses, the run's `state` will change from `scheduled` to other values, such as
    `in_progress` and `succeeded`.

    Args:
        maintenance_run_param (str):  Example: mrn-cph1rs3idesc73a2b2mg.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error]
    """

    return (
        await asyncio_detailed(
            maintenance_run_param=maintenance_run_param,
            client=client,
        )
    ).parsed
