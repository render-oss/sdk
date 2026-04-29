"""Tests for KeyValueApi."""

import datetime
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from render_sdk.client.errors import ClientError, ServerError
from render_sdk.experimental.key_value.api import KeyValueApi
from render_sdk.experimental.key_value.types import KeyValueInstance
from render_sdk.public_api.models.database_status import DatabaseStatus
from render_sdk.public_api.models.key_value import KeyValue
from render_sdk.public_api.models.key_value_connection_info import (
    KeyValueConnectionInfo,
)
from render_sdk.public_api.models.key_value_detail import KeyValueDetail
from render_sdk.public_api.models.key_value_options import KeyValueOptions
from render_sdk.public_api.models.key_value_patch_input import KeyValuePATCHInput
from render_sdk.public_api.models.key_value_plan import KeyValuePlan
from render_sdk.public_api.models.key_value_post_input import KeyValuePOSTInput
from render_sdk.public_api.models.key_value_with_cursor import KeyValueWithCursor
from render_sdk.public_api.models.owner import Owner
from render_sdk.public_api.models.owner_type import OwnerType
from render_sdk.public_api.models.region import Region

_NOW = datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc)


def make_key_value_detail(
    id_: str = "red-abc",
    status: DatabaseStatus = DatabaseStatus.AVAILABLE,
    plan: KeyValuePlan = KeyValuePlan.FREE,
) -> KeyValueDetail:
    owner = Owner(
        id="tea-abc", name="Test", email="test@example.com", type_=OwnerType.TEAM
    )
    return KeyValueDetail(
        id=id_,
        created_at=_NOW,
        updated_at=_NOW,
        status=status,
        region=Region.OREGON,
        plan=plan,
        name="test-kv",
        owner=owner,
        options=KeyValueOptions(),
        ip_allow_list=[],
        version="7.2",
    )


def make_key_value(id_: str = "red-abc") -> KeyValue:
    owner = Owner(
        id="tea-abc", name="Test", email="test@example.com", type_=OwnerType.TEAM
    )
    return KeyValue(
        id=id_,
        created_at=_NOW,
        updated_at=_NOW,
        status=DatabaseStatus.AVAILABLE,
        region=Region.OREGON,
        plan=KeyValuePlan.FREE,
        name="test-kv",
        owner=owner,
        options=KeyValueOptions(),
        ip_allow_list=[],
        version="7.2",
        dashboard_url="https://dashboard.render.com/kv/red-abc",
    )


def ok(parsed):
    return SimpleNamespace(status_code=200, parsed=parsed)


def err(status_code):
    return SimpleNamespace(status_code=status_code, parsed=None)


@pytest.fixture
def api():
    return KeyValueApi(MagicMock())


class TestFindById:
    @pytest.mark.asyncio
    async def test_handles_api_token_error(self, api, mocker):
        mocker.patch(
            "render_sdk.experimental.key_value.api.retrieve_key_value.asyncio_detailed",
            new_callable=AsyncMock,
            return_value=err(401),
        )
        with pytest.raises(ClientError, match="API Token is not authorized"):
            await api.find_by_id("red-abc")

    @pytest.mark.asyncio
    async def test_handles_not_found_error(self, api, mocker):
        mocker.patch(
            "render_sdk.experimental.key_value.api.retrieve_key_value.asyncio_detailed",
            new_callable=AsyncMock,
            return_value=err(404),
        )
        with pytest.raises(ClientError, match="Unable to locate a Key Value with ID"):
            await api.find_by_id("red-abc")

    @pytest.mark.asyncio
    async def test_handles_unknown_client_error(self, api, mocker):
        mocker.patch(
            "render_sdk.experimental.key_value.api.retrieve_key_value.asyncio_detailed",
            new_callable=AsyncMock,
            return_value=err(429),
        )
        with pytest.raises(ClientError):
            await api.find_by_id("red-abc")

    @pytest.mark.asyncio
    async def test_handles_server_error(self, api, mocker):
        mocker.patch(
            "render_sdk.experimental.key_value.api.retrieve_key_value.asyncio_detailed",
            new_callable=AsyncMock,
            return_value=err(500),
        )
        with pytest.raises(ServerError):
            await api.find_by_id("red-abc")

    @pytest.mark.asyncio
    async def test_returns_instance_on_success(self, api, mocker):
        detail = make_key_value_detail()
        mocker.patch(
            "render_sdk.experimental.key_value.api.retrieve_key_value.asyncio_detailed",
            new_callable=AsyncMock,
            return_value=ok(detail),
        )
        result = await api.find_by_id("red-abc")
        assert isinstance(result, KeyValueInstance)
        assert result.id == detail.id
        assert result.status == detail.status
        assert result.plan == detail.plan


class TestFindByName:
    @pytest.mark.asyncio
    async def test_handles_api_token_error(self, api, mocker):
        mocker.patch(
            "render_sdk.experimental.key_value.api.list_key_value.asyncio_detailed",
            new_callable=AsyncMock,
            return_value=err(401),
        )
        with pytest.raises(ClientError, match="API Token is not authorized"):
            await api.find_by_name("test-redis", "tea-abc")

    @pytest.mark.asyncio
    async def test_handles_unknown_client_error(self, api, mocker):
        mocker.patch(
            "render_sdk.experimental.key_value.api.list_key_value.asyncio_detailed",
            new_callable=AsyncMock,
            return_value=err(429),
        )
        with pytest.raises(ClientError):
            await api.find_by_name("test-redis", "tea-abc")

    @pytest.mark.asyncio
    async def test_handles_server_error(self, api, mocker):
        mocker.patch(
            "render_sdk.experimental.key_value.api.list_key_value.asyncio_detailed",
            new_callable=AsyncMock,
            return_value=err(500),
        )
        with pytest.raises(ServerError):
            await api.find_by_name("test-redis", "tea-abc")

    @pytest.mark.asyncio
    async def test_returns_none_when_no_results(self, api, mocker):
        mocker.patch(
            "render_sdk.experimental.key_value.api.list_key_value.asyncio_detailed",
            new_callable=AsyncMock,
            return_value=ok([]),
        )
        result = await api.find_by_name("test-redis", "tea-abc")
        assert result is None

    @pytest.mark.asyncio
    async def test_returns_instance_on_success(self, api, mocker):
        kv = make_key_value()
        mocker.patch(
            "render_sdk.experimental.key_value.api.list_key_value.asyncio_detailed",
            new_callable=AsyncMock,
            return_value=ok([KeyValueWithCursor(key_value=kv, cursor="abc")]),
        )
        result = await api.find_by_name("test-redis", "tea-abc")
        assert isinstance(result, KeyValueInstance)
        assert result.id == kv.id
        assert result.status == kv.status
        assert result.plan == kv.plan


class TestGetConnectionInfo:
    @pytest.mark.asyncio
    async def test_handles_api_token_error(self, api, mocker):
        mocker.patch(
            "render_sdk.experimental.key_value.api.retrieve_key_value_connection_info.asyncio_detailed",
            new_callable=AsyncMock,
            return_value=err(401),
        )
        with pytest.raises(ClientError, match="API Token is not authorized"):
            await api.get_connection_info("red-abc")

    @pytest.mark.asyncio
    async def test_handles_unknown_client_error(self, api, mocker):
        mocker.patch(
            "render_sdk.experimental.key_value.api.retrieve_key_value_connection_info.asyncio_detailed",
            new_callable=AsyncMock,
            return_value=err(429),
        )
        with pytest.raises(ClientError):
            await api.get_connection_info("red-abc")

    @pytest.mark.asyncio
    async def test_handles_server_error(self, api, mocker):
        mocker.patch(
            "render_sdk.experimental.key_value.api.retrieve_key_value_connection_info.asyncio_detailed",
            new_callable=AsyncMock,
            return_value=err(500),
        )
        with pytest.raises(ServerError):
            await api.get_connection_info("red-abc")

    @pytest.mark.asyncio
    async def test_returns_internal_url_when_on_render(self, api, mocker, monkeypatch):
        internal = "redis://red-abc:6239"
        external = "rediss://abc:xyz@red-abc.ext:6239"
        mocker.patch(
            "render_sdk.experimental.key_value.api.retrieve_key_value_connection_info.asyncio_detailed",
            new_callable=AsyncMock,
            return_value=ok(
                KeyValueConnectionInfo(
                    internal_connection_string=internal,
                    external_connection_string=external,
                    cli_command="redis-cli",
                )
            ),
        )
        monkeypatch.setenv("RENDER", "true")
        result = await api.get_connection_info("red-abc")
        assert result == internal

    @pytest.mark.asyncio
    async def test_returns_external_url_when_not_on_render(
        self, api, mocker, monkeypatch
    ):
        internal = "redis://red-abc:6239"
        external = "rediss://abc:xyz@red-abc.ext:6239"
        mocker.patch(
            "render_sdk.experimental.key_value.api.retrieve_key_value_connection_info.asyncio_detailed",
            new_callable=AsyncMock,
            return_value=ok(
                KeyValueConnectionInfo(
                    internal_connection_string=internal,
                    external_connection_string=external,
                    cli_command="redis-cli",
                )
            ),
        )
        monkeypatch.delenv("RENDER", raising=False)
        result = await api.get_connection_info("red-abc")
        assert result == external


class TestCreateInstance:
    @pytest.mark.asyncio
    async def test_handles_api_token_error(self, api, mocker):
        mocker.patch(
            "render_sdk.experimental.key_value.api.create_key_value.asyncio_detailed",
            new_callable=AsyncMock,
            return_value=err(401),
        )
        body = KeyValuePOSTInput(
            name="test-redis", owner_id="tea-abc", plan=KeyValuePlan.FREE
        )
        with pytest.raises(ClientError, match="API Token is not authorized"):
            await api.create_instance(body)

    @pytest.mark.asyncio
    async def test_handles_unknown_client_error(self, api, mocker):
        mocker.patch(
            "render_sdk.experimental.key_value.api.create_key_value.asyncio_detailed",
            new_callable=AsyncMock,
            return_value=err(429),
        )
        body = KeyValuePOSTInput(
            name="test-redis", owner_id="tea-abc", plan=KeyValuePlan.FREE
        )
        with pytest.raises(ClientError):
            await api.create_instance(body)

    @pytest.mark.asyncio
    async def test_handles_server_error(self, api, mocker):
        mocker.patch(
            "render_sdk.experimental.key_value.api.create_key_value.asyncio_detailed",
            new_callable=AsyncMock,
            return_value=err(500),
        )
        body = KeyValuePOSTInput(
            name="test-redis", owner_id="tea-abc", plan=KeyValuePlan.FREE
        )
        with pytest.raises(ServerError):
            await api.create_instance(body)

    @pytest.mark.asyncio
    async def test_returns_instance_on_success(self, api, mocker):
        detail = make_key_value_detail()
        mocker.patch(
            "render_sdk.experimental.key_value.api.create_key_value.asyncio_detailed",
            new_callable=AsyncMock,
            return_value=ok(detail),
        )
        body = KeyValuePOSTInput(
            name="test-redis", owner_id="tea-abc", plan=KeyValuePlan.FREE
        )
        result = await api.create_instance(body)
        assert isinstance(result, KeyValueInstance)
        assert result.id == detail.id
        assert result.plan == detail.plan


class TestUpdateInstance:
    @pytest.mark.asyncio
    async def test_handles_api_token_error(self, api, mocker):
        mocker.patch(
            "render_sdk.experimental.key_value.api.update_key_value.asyncio_detailed",
            new_callable=AsyncMock,
            return_value=err(401),
        )
        with pytest.raises(ClientError, match="API Token is not authorized"):
            await api.update_instance("red-abc", KeyValuePATCHInput())

    @pytest.mark.asyncio
    async def test_handles_unknown_client_error(self, api, mocker):
        mocker.patch(
            "render_sdk.experimental.key_value.api.update_key_value.asyncio_detailed",
            new_callable=AsyncMock,
            return_value=err(429),
        )
        with pytest.raises(ClientError):
            await api.update_instance("red-abc", KeyValuePATCHInput())

    @pytest.mark.asyncio
    async def test_handles_server_error(self, api, mocker):
        mocker.patch(
            "render_sdk.experimental.key_value.api.update_key_value.asyncio_detailed",
            new_callable=AsyncMock,
            return_value=err(500),
        )
        with pytest.raises(ServerError):
            await api.update_instance("red-abc", KeyValuePATCHInput())

    @pytest.mark.asyncio
    async def test_returns_instance_on_success(self, api, mocker):
        detail = make_key_value_detail(plan=KeyValuePlan.STARTER)
        mocker.patch(
            "render_sdk.experimental.key_value.api.update_key_value.asyncio_detailed",
            new_callable=AsyncMock,
            return_value=ok(detail),
        )
        result = await api.update_instance(
            "red-abc", KeyValuePATCHInput(plan=KeyValuePlan.STARTER)
        )
        assert isinstance(result, KeyValueInstance)
        assert result.id == detail.id
        assert result.plan == KeyValuePlan.STARTER
