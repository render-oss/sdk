from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.deploy import Deploy
from ...models.error import Error
from ...models.rollback_deploy_body import RollbackDeployBody
from ...types import Response


def _get_kwargs(
    service_id: str,
    *,
    body: RollbackDeployBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/services/{service_id}/rollback".format(
            service_id=quote(str(service_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx2.Response) -> Deploy | Error | None:
    if response.status_code == 201:
        response_201 = Deploy.from_dict(response.json())

        return response_201

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx2.Response) -> Response[Deploy | Error]:
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
    body: RollbackDeployBody,
) -> Response[Deploy | Error]:
    """Roll back deploy

     Trigger a rollback to a previous deploy of the specified service.

    Triggering a rollback with this endpoint does not disable autodeploys for the service. This means an
    autodeploy might restore changes you had intentionally rolled back.

    You can toggle autodeploys for your service with the [Update service](https://api-
    docs.render.com/reference/update-service) endpoint or in the Render Dashboard.

    Args:
        service_id (str):
        body (RollbackDeployBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Deploy | Error]
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
    client: AuthenticatedClient | Client,
    body: RollbackDeployBody,
) -> Deploy | Error | None:
    """Roll back deploy

     Trigger a rollback to a previous deploy of the specified service.

    Triggering a rollback with this endpoint does not disable autodeploys for the service. This means an
    autodeploy might restore changes you had intentionally rolled back.

    You can toggle autodeploys for your service with the [Update service](https://api-
    docs.render.com/reference/update-service) endpoint or in the Render Dashboard.

    Args:
        service_id (str):
        body (RollbackDeployBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Deploy | Error
    """

    return sync_detailed(
        service_id=service_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    service_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: RollbackDeployBody,
) -> Response[Deploy | Error]:
    """Roll back deploy

     Trigger a rollback to a previous deploy of the specified service.

    Triggering a rollback with this endpoint does not disable autodeploys for the service. This means an
    autodeploy might restore changes you had intentionally rolled back.

    You can toggle autodeploys for your service with the [Update service](https://api-
    docs.render.com/reference/update-service) endpoint or in the Render Dashboard.

    Args:
        service_id (str):
        body (RollbackDeployBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Deploy | Error]
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
    client: AuthenticatedClient | Client,
    body: RollbackDeployBody,
) -> Deploy | Error | None:
    """Roll back deploy

     Trigger a rollback to a previous deploy of the specified service.

    Triggering a rollback with this endpoint does not disable autodeploys for the service. This means an
    autodeploy might restore changes you had intentionally rolled back.

    You can toggle autodeploys for your service with the [Update service](https://api-
    docs.render.com/reference/update-service) endpoint or in the Render Dashboard.

    Args:
        service_id (str):
        body (RollbackDeployBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Deploy | Error
    """

    return (
        await asyncio_detailed(
            service_id=service_id,
            client=client,
            body=body,
        )
    ).parsed
