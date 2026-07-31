from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.log_stream_setting import LogStreamSetting
from ...models.resource_log_stream_setting import ResourceLogStreamSetting
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    owner_id: Union[Unset, list[str]] = UNSET,
    log_stream_id: Union[Unset, list[str]] = UNSET,
    resource_id: Union[Unset, list[str]] = UNSET,
    setting: Union[Unset, list[LogStreamSetting]] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_owner_id: Union[Unset, list[str]] = UNSET
    if not isinstance(owner_id, Unset):
        json_owner_id = owner_id

    params["ownerId"] = json_owner_id

    json_log_stream_id: Union[Unset, list[str]] = UNSET
    if not isinstance(log_stream_id, Unset):
        json_log_stream_id = log_stream_id

    params["logStreamId"] = json_log_stream_id

    json_resource_id: Union[Unset, list[str]] = UNSET
    if not isinstance(resource_id, Unset):
        json_resource_id = resource_id

    params["resourceId"] = json_resource_id

    json_setting: Union[Unset, list[str]] = UNSET
    if not isinstance(setting, Unset):
        json_setting = []
        for setting_item_data in setting:
            setting_item = setting_item_data.value
            json_setting.append(setting_item)

    params["setting"] = json_setting

    params["cursor"] = cursor

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/logs/streams/resource",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Error, list["ResourceLogStreamSetting"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ResourceLogStreamSetting.from_dict(response_200_item_data)

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
) -> Response[Union[Error, list["ResourceLogStreamSetting"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    owner_id: Union[Unset, list[str]] = UNSET,
    log_stream_id: Union[Unset, list[str]] = UNSET,
    resource_id: Union[Unset, list[str]] = UNSET,
    setting: Union[Unset, list[LogStreamSetting]] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> Response[Union[Error, list["ResourceLogStreamSetting"]]]:
    """List log stream overrides

     Lists log stream overrides for the provided workspace that match the provided filters. These
    overrides take precedence over the workspace's default log stream.

    Args:
        owner_id (Union[Unset, list[str]]):
        log_stream_id (Union[Unset, list[str]]):
        resource_id (Union[Unset, list[str]]):
        setting (Union[Unset, list[LogStreamSetting]]):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, list['ResourceLogStreamSetting']]]
    """

    kwargs = _get_kwargs(
        owner_id=owner_id,
        log_stream_id=log_stream_id,
        resource_id=resource_id,
        setting=setting,
        cursor=cursor,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    owner_id: Union[Unset, list[str]] = UNSET,
    log_stream_id: Union[Unset, list[str]] = UNSET,
    resource_id: Union[Unset, list[str]] = UNSET,
    setting: Union[Unset, list[LogStreamSetting]] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> Optional[Union[Error, list["ResourceLogStreamSetting"]]]:
    """List log stream overrides

     Lists log stream overrides for the provided workspace that match the provided filters. These
    overrides take precedence over the workspace's default log stream.

    Args:
        owner_id (Union[Unset, list[str]]):
        log_stream_id (Union[Unset, list[str]]):
        resource_id (Union[Unset, list[str]]):
        setting (Union[Unset, list[LogStreamSetting]]):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, list['ResourceLogStreamSetting']]
    """

    return sync_detailed(
        client=client,
        owner_id=owner_id,
        log_stream_id=log_stream_id,
        resource_id=resource_id,
        setting=setting,
        cursor=cursor,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    owner_id: Union[Unset, list[str]] = UNSET,
    log_stream_id: Union[Unset, list[str]] = UNSET,
    resource_id: Union[Unset, list[str]] = UNSET,
    setting: Union[Unset, list[LogStreamSetting]] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> Response[Union[Error, list["ResourceLogStreamSetting"]]]:
    """List log stream overrides

     Lists log stream overrides for the provided workspace that match the provided filters. These
    overrides take precedence over the workspace's default log stream.

    Args:
        owner_id (Union[Unset, list[str]]):
        log_stream_id (Union[Unset, list[str]]):
        resource_id (Union[Unset, list[str]]):
        setting (Union[Unset, list[LogStreamSetting]]):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, list['ResourceLogStreamSetting']]]
    """

    kwargs = _get_kwargs(
        owner_id=owner_id,
        log_stream_id=log_stream_id,
        resource_id=resource_id,
        setting=setting,
        cursor=cursor,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    owner_id: Union[Unset, list[str]] = UNSET,
    log_stream_id: Union[Unset, list[str]] = UNSET,
    resource_id: Union[Unset, list[str]] = UNSET,
    setting: Union[Unset, list[LogStreamSetting]] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 20,
) -> Optional[Union[Error, list["ResourceLogStreamSetting"]]]:
    """List log stream overrides

     Lists log stream overrides for the provided workspace that match the provided filters. These
    overrides take precedence over the workspace's default log stream.

    Args:
        owner_id (Union[Unset, list[str]]):
        log_stream_id (Union[Unset, list[str]]):
        resource_id (Union[Unset, list[str]]):
        setting (Union[Unset, list[LogStreamSetting]]):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]): Defaults to 20 Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, list['ResourceLogStreamSetting']]
    """

    return (
        await asyncio_detailed(
            client=client,
            owner_id=owner_id,
            log_stream_id=log_stream_id,
            resource_id=resource_id,
            setting=setting,
            cursor=cursor,
            limit=limit,
        )
    ).parsed
