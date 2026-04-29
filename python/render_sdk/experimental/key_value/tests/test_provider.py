"""Tests for KeyValueProvider."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from render_sdk.client.errors import RenderError
from render_sdk.experimental.key_value.provider import KeyValueProvider
from render_sdk.experimental.key_value.types import (
    InstanceConfiguration,
    KeyValueInstance,
    NameOwnerIdOptions,
    ServiceIdOptions,
)
from render_sdk.public_api.models.database_status import DatabaseStatus
from render_sdk.public_api.models.key_value_plan import KeyValuePlan
from render_sdk.public_api.models.maxmemory_policy import MaxmemoryPolicy


def make_detail(
    id_: str = "red-abc",
    status: DatabaseStatus = DatabaseStatus.AVAILABLE,
    plan: str = "free",
    maxmemory_policy: MaxmemoryPolicy = MaxmemoryPolicy.ALLKEYS_LRU,
    ip_allow_list=None,
) -> KeyValueInstance:
    return KeyValueInstance(
        id=id_,
        status=status,
        plan=KeyValuePlan(plan),
        maxmemory_policy=maxmemory_policy,
        ip_allow_list=ip_allow_list if ip_allow_list is not None else [],
    )


@pytest.fixture
def api():
    mock = MagicMock()
    mock.find_by_id = AsyncMock(
        side_effect=Exception("find_by_id should not be called")
    )
    mock.find_by_name = AsyncMock(
        side_effect=Exception("find_by_name should not be called")
    )
    mock.get_connection_info = AsyncMock(
        side_effect=Exception("get_connection_info should not be called")
    )
    mock.create_instance = AsyncMock(
        side_effect=Exception("create_instance should not be called")
    )
    mock.update_instance = AsyncMock(
        side_effect=Exception("update_instance should not be called")
    )
    return mock


@pytest.fixture(autouse=True)
def mock_sleep(mocker):
    return mocker.patch(
        "render_sdk.experimental.key_value.provider.asyncio.sleep",
        new_callable=AsyncMock,
    )


@pytest.fixture(autouse=True)
def mock_redis(mocker):
    return mocker.patch("redis.asyncio.Redis.from_url", return_value=MagicMock())


class TestWithDefaultOwnerId:
    @pytest.fixture
    def client(self, api):
        return KeyValueProvider(api, default_owner_id="tea-abc")

    @pytest.mark.asyncio
    async def test_new_client_with_name_creates_client(self, client, api):
        api.find_by_name.side_effect = None
        api.find_by_name.return_value = make_detail()
        api.get_connection_info.side_effect = None
        api.get_connection_info.return_value = "redis://localhosta:6239"

        result = await client.new_client(NameOwnerIdOptions(name="test-redis"))

        assert result is not None
        api.get_connection_info.assert_called_once_with("red-abc")

    @pytest.mark.asyncio
    async def test_connection_info_with_name_parses_connection(self, client, api):
        api.find_by_name.side_effect = None
        api.find_by_name.return_value = make_detail()
        api.get_connection_info.side_effect = None
        api.get_connection_info.return_value = "redis://localhosta:6239"

        result = await client.connection_info(NameOwnerIdOptions(name="test-redis"))

        assert result.host == "localhosta"
        assert result.port == 6239
        api.get_connection_info.assert_called_once_with("red-abc")


class TestWithoutDefaultOwnerId:
    @pytest.fixture
    def client(self, api):
        return KeyValueProvider(api)

    class TestNewClientWithServiceId:
        @pytest.mark.asyncio
        async def test_creates_client(self, client, api):
            api.find_by_id.side_effect = None
            api.find_by_id.return_value = make_detail()
            api.get_connection_info.side_effect = None
            api.get_connection_info.return_value = "redis://localhosta:6239"

            result = await client.new_client(ServiceIdOptions(service_id="red-abc"))

            assert result is not None
            api.get_connection_info.assert_called_once_with("red-abc")

        @pytest.mark.asyncio
        async def test_errors_if_service_id_not_found(self, client, api):
            error = RenderError("Unable to find ID")
            api.find_by_id.side_effect = error

            with pytest.raises(RenderError):
                await client.new_client(ServiceIdOptions(service_id="red-abc"))

        @pytest.mark.asyncio
        async def test_errors_if_connection_info_not_found(self, client, api):
            api.find_by_id.side_effect = None
            api.find_by_id.return_value = make_detail()
            api.get_connection_info.side_effect = RenderError(
                "Unable to find connection info"
            )

            with pytest.raises(RenderError):
                await client.new_client(ServiceIdOptions(service_id="red-abc"))

    class TestNewClientWithName:
        @pytest.mark.asyncio
        async def test_creates_client(self, client, api):
            api.find_by_name.side_effect = None
            api.find_by_name.return_value = make_detail()
            api.get_connection_info.side_effect = None
            api.get_connection_info.return_value = "redis://localhosta:6239"

            result = await client.new_client(
                NameOwnerIdOptions(name="test-redis", owner_id="tea-abc")
            )

            assert result is not None
            api.get_connection_info.assert_called_once_with("red-abc")

        @pytest.mark.asyncio
        async def test_errors_if_owner_id_missing(self, client, api):
            with pytest.raises(RenderError, match="owner_id is required"):
                await client.new_client(NameOwnerIdOptions(name="test-redis"))

        @pytest.mark.asyncio
        async def test_errors_if_not_found_and_auto_provision_disabled(
            self, client, api
        ):
            api.find_by_name.side_effect = None
            api.find_by_name.return_value = None

            with pytest.raises(RenderError, match="Unable to locate Key Value"):
                await client.new_client(
                    NameOwnerIdOptions(
                        name="test-redis",
                        owner_id="tea-abc",
                        auto_provision=False,
                    )
                )

        @pytest.mark.asyncio
        async def test_errors_if_connection_info_not_found(self, client, api):
            api.find_by_name.side_effect = None
            api.find_by_name.return_value = make_detail()
            api.get_connection_info.side_effect = RenderError(
                "Unable to find connection info"
            )

            with pytest.raises(RenderError):
                await client.new_client(
                    NameOwnerIdOptions(name="test-redis", owner_id="tea-abc")
                )

    class TestConnectionInfoWithServiceId:
        @pytest.mark.asyncio
        async def test_parses_connection_info(self, client, api):
            api.find_by_id.side_effect = None
            api.find_by_id.return_value = make_detail()
            api.get_connection_info.side_effect = None
            api.get_connection_info.return_value = "redis://localhosta:6239"

            result = await client.connection_info(
                ServiceIdOptions(service_id="red-abc")
            )

            assert result.host == "localhosta"
            assert result.port == 6239
            assert result.username is None
            assert result.password is None

        @pytest.mark.asyncio
        async def test_parses_connection_info_with_credentials(self, client, api):
            api.find_by_id.side_effect = None
            api.find_by_id.return_value = make_detail()
            api.get_connection_info.side_effect = None
            api.get_connection_info.return_value = "redis://user:pass@localhosta:6239"

            result = await client.connection_info(
                ServiceIdOptions(service_id="red-abc")
            )

            assert result.host == "localhosta"
            assert result.port == 6239
            assert result.username == "user"
            assert result.password == "pass"  # noqa: S105 (not a hardcoded password)

        @pytest.mark.asyncio
        async def test_errors_on_invalid_connection_string_format(self, client, api):
            api.find_by_id.side_effect = None
            api.find_by_id.return_value = make_detail()
            api.get_connection_info.side_effect = None
            api.get_connection_info.return_value = "redis://noport.com"

            with pytest.raises(RenderError, match="unexpected format"):
                await client.connection_info(ServiceIdOptions(service_id="red-abc"))

        @pytest.mark.asyncio
        async def test_errors_if_service_id_not_found(self, client, api):
            api.find_by_id.side_effect = RenderError("Unable to find service ID")

            with pytest.raises(RenderError):
                await client.connection_info(ServiceIdOptions(service_id="red-abc"))

        @pytest.mark.asyncio
        async def test_errors_if_connection_info_not_found(self, client, api):
            api.find_by_id.side_effect = None
            api.find_by_id.return_value = make_detail()
            api.get_connection_info.side_effect = RenderError(
                "Unable to find connection info"
            )

            with pytest.raises(RenderError):
                await client.connection_info(ServiceIdOptions(service_id="red-abc"))

    class TestConnectionInfoWithName:
        @pytest.mark.asyncio
        async def test_parses_connection_info(self, client, api):
            api.find_by_name.side_effect = None
            api.find_by_name.return_value = make_detail()
            api.get_connection_info.side_effect = None
            api.get_connection_info.return_value = "rediss://localhosta:6239"

            result = await client.connection_info(
                NameOwnerIdOptions(name="test-redis", owner_id="tea-abc")
            )

            assert result.host == "localhosta"
            assert result.port == 6239

        @pytest.mark.asyncio
        async def test_parses_connection_info_with_credentials(self, client, api):
            api.find_by_name.side_effect = None
            api.find_by_name.return_value = make_detail()
            api.get_connection_info.side_effect = None
            api.get_connection_info.return_value = "rediss://user:pass@localhosta:6239"

            result = await client.connection_info(
                NameOwnerIdOptions(name="test-redis", owner_id="tea-abc")
            )

            assert result.host == "localhosta"
            assert result.port == 6239
            assert result.username == "user"
            assert result.password == "pass"  # noqa: S105 (not a hardcoded password)

        @pytest.mark.asyncio
        async def test_errors_on_invalid_connection_string_format(self, client, api):
            api.find_by_name.side_effect = None
            api.find_by_name.return_value = make_detail()
            api.get_connection_info.side_effect = None
            api.get_connection_info.return_value = "redis://noport.com"

            with pytest.raises(RenderError, match="unexpected format"):
                await client.connection_info(
                    NameOwnerIdOptions(name="test-redis", owner_id="tea-abc")
                )

        @pytest.mark.asyncio
        async def test_errors_if_owner_id_missing(self, client, api):
            with pytest.raises(RenderError, match="owner_id is required"):
                await client.connection_info(NameOwnerIdOptions(name="test-redis"))

        @pytest.mark.asyncio
        async def test_errors_if_not_found_and_auto_provision_disabled(
            self, client, api
        ):
            api.find_by_name.side_effect = None
            api.find_by_name.return_value = None

            with pytest.raises(RenderError, match="Unable to locate Key Value"):
                await client.connection_info(
                    NameOwnerIdOptions(
                        name="test-redis",
                        owner_id="tea-abc",
                        auto_provision=False,
                    )
                )

        @pytest.mark.asyncio
        async def test_errors_if_connection_info_not_found(self, client, api):
            api.find_by_name.side_effect = None
            api.find_by_name.return_value = make_detail()
            api.get_connection_info.side_effect = RenderError(
                "Unable to locate connection info"
            )

            with pytest.raises(RenderError):
                await client.connection_info(
                    NameOwnerIdOptions(name="test-redis", owner_id="tea-abc")
                )

    class TestAutomaticProvisioning:
        """Tests for auto-provisioning when no instance is found by name."""

        @pytest.fixture(autouse=True)
        def setup(self, api):
            api.find_by_name.side_effect = None
            api.find_by_name.return_value = None
            api.get_connection_info.side_effect = None
            api.get_connection_info.return_value = "rediss://localhosta:6239"

        @pytest.mark.asyncio
        async def test_new_client_sends_post_with_options_if_not_found(
            self, client, api
        ):
            api.create_instance.side_effect = RenderError("Early exit")

            with pytest.raises(RenderError):
                await client.new_client(
                    NameOwnerIdOptions(name="test-redis", owner_id="tea-abc")
                )

            api.create_instance.assert_called_once()
            call_body = api.create_instance.call_args.args[0]
            assert call_body.name == "test-redis"
            assert call_body.owner_id == "tea-abc"
            assert call_body.plan == KeyValuePlan.FREE

        @pytest.mark.asyncio
        async def test_new_client_waits_for_available_after_creating(self, client, api):
            api.create_instance.side_effect = None
            api.create_instance.return_value = make_detail(
                status=DatabaseStatus.CREATING
            )
            api.find_by_id.side_effect = [
                make_detail(status=DatabaseStatus.CREATING),
                make_detail(status=DatabaseStatus.AVAILABLE),
            ]

            result = await client.new_client(
                NameOwnerIdOptions(name="test-redis", owner_id="tea-abc")
            )

            assert result is not None
            assert api.find_by_id.call_count == 2

        @pytest.mark.asyncio
        async def test_new_client_errors_on_unrecoverable_status(self, client, api):
            api.create_instance.side_effect = None
            api.create_instance.return_value = make_detail(
                status=DatabaseStatus.CREATING
            )
            api.find_by_id.side_effect = [
                make_detail(status=DatabaseStatus.CREATING),
                make_detail(status=DatabaseStatus.RECOVERY_FAILED),
            ]

            with pytest.raises(RenderError, match="instance is not available"):
                await client.new_client(
                    NameOwnerIdOptions(name="test-redis", owner_id="tea-abc")
                )

            assert api.find_by_id.call_count == 2

        @pytest.mark.asyncio
        async def test_connection_info_sends_post_with_options_if_not_found(
            self, client, api
        ):
            api.create_instance.side_effect = RenderError("Early exit")

            with pytest.raises(RenderError):
                await client.connection_info(
                    NameOwnerIdOptions(name="test-redis", owner_id="tea-abc")
                )

            api.create_instance.assert_called_once()
            call_body = api.create_instance.call_args.args[0]
            assert call_body.name == "test-redis"
            assert call_body.owner_id == "tea-abc"
            assert call_body.plan == KeyValuePlan.FREE

        @pytest.mark.asyncio
        async def test_connection_info_waits_for_available_after_creating(
            self, client, api
        ):
            api.create_instance.side_effect = None
            api.create_instance.return_value = make_detail(
                status=DatabaseStatus.CREATING
            )
            api.find_by_id.side_effect = [
                make_detail(status=DatabaseStatus.CREATING),
                make_detail(status=DatabaseStatus.AVAILABLE),
            ]

            result = await client.connection_info(
                NameOwnerIdOptions(name="test-redis", owner_id="tea-abc")
            )

            assert result.host == "localhosta"
            assert result.port == 6239
            assert api.find_by_id.call_count == 2

        @pytest.mark.asyncio
        async def test_connection_info_errors_on_unrecoverable_status(
            self, client, api
        ):
            api.create_instance.side_effect = None
            api.create_instance.return_value = make_detail(
                status=DatabaseStatus.CREATING
            )
            api.find_by_id.side_effect = [
                make_detail(status=DatabaseStatus.CREATING),
                make_detail(status=DatabaseStatus.RECOVERY_FAILED),
            ]

            with pytest.raises(RenderError, match="instance is not available"):
                await client.connection_info(
                    NameOwnerIdOptions(name="test-redis", owner_id="tea-abc")
                )

            assert api.find_by_id.call_count == 2

    class TestConfigurationSync:
        """Tests for configuration sync when options differ from current state."""

        CONNECTION_STRING = "rediss://user:pass@localhosta:6239"

        @pytest.fixture(autouse=True)
        def setup(self, api):
            api.get_connection_info.side_effect = None
            api.get_connection_info.return_value = self.CONNECTION_STRING

        class TestNewClientWithServiceId:
            @pytest.mark.asyncio
            async def test_no_update_if_no_settings_set(self, client, api):
                api.find_by_id.side_effect = None
                api.find_by_id.return_value = make_detail(plan="starter")

                result = await client.new_client(ServiceIdOptions(service_id="red-abc"))

                assert result is not None
                api.update_instance.assert_not_called()
                assert api.find_by_id.call_count == 1

            @pytest.mark.asyncio
            async def test_no_update_if_config_matches(self, client, api):
                api.find_by_id.side_effect = None
                api.find_by_id.return_value = make_detail(
                    plan="starter", maxmemory_policy=MaxmemoryPolicy.ALLKEYS_LRU
                )

                result = await client.new_client(
                    ServiceIdOptions(
                        service_id="red-abc",
                        auto_provision=InstanceConfiguration(
                            plan="starter",
                            maxmemory_policy=MaxmemoryPolicy.ALLKEYS_LRU,
                        ),
                    )
                )

                assert result is not None
                api.update_instance.assert_not_called()
                assert api.find_by_id.call_count == 1

            @pytest.mark.asyncio
            async def test_sends_patch_if_changes_needed(self, client, api):
                api.find_by_id.side_effect = None
                api.find_by_id.return_value = make_detail(
                    plan="free", maxmemory_policy=MaxmemoryPolicy.ALLKEYS_LRU
                )
                api.update_instance.side_effect = RenderError("early exit")

                with pytest.raises(RenderError):
                    await client.new_client(
                        ServiceIdOptions(
                            service_id="red-abc",
                            auto_provision=InstanceConfiguration(
                                plan="starter",
                                maxmemory_policy=MaxmemoryPolicy.ALLKEYS_RANDOM,
                            ),
                        )
                    )

                api.update_instance.assert_called_once()
                assert api.update_instance.call_args.args[0] == "red-abc"
                patch = api.update_instance.call_args.args[1]
                assert patch.plan == KeyValuePlan.STARTER
                assert patch.maxmemory_policy == MaxmemoryPolicy.ALLKEYS_RANDOM

            @pytest.mark.asyncio
            async def test_waits_for_available_after_update(self, client, api):
                available = make_detail(
                    plan="starter", maxmemory_policy=MaxmemoryPolicy.ALLKEYS_RANDOM
                )
                updating = make_detail(
                    plan="starter",
                    maxmemory_policy=MaxmemoryPolicy.ALLKEYS_RANDOM,
                    status=DatabaseStatus.UPDATING_INSTANCE,
                )
                api.find_by_id.side_effect = [
                    make_detail(
                        plan="free", maxmemory_policy=MaxmemoryPolicy.ALLKEYS_LRU
                    ),
                    updating,
                    available,
                ]
                api.update_instance.side_effect = None
                api.update_instance.return_value = updating

                result = await client.new_client(
                    ServiceIdOptions(
                        service_id="red-abc",
                        auto_provision=InstanceConfiguration(
                            plan="starter",
                            maxmemory_policy=MaxmemoryPolicy.ALLKEYS_RANDOM,
                        ),
                    )
                )

                assert result is not None
                assert api.find_by_id.call_count == 3

            @pytest.mark.asyncio
            async def test_errors_on_unrecoverable_state_after_update(
                self, client, api
            ):
                updating = make_detail(
                    plan="starter",
                    status=DatabaseStatus.UPDATING_INSTANCE,
                )
                failed = make_detail(
                    plan="starter", status=DatabaseStatus.RECOVERY_FAILED
                )
                api.find_by_id.side_effect = [
                    make_detail(plan="free"),
                    updating,
                    failed,
                ]
                api.update_instance.side_effect = None
                api.update_instance.return_value = updating

                with pytest.raises(RenderError, match="instance is not available"):
                    await client.new_client(
                        ServiceIdOptions(
                            service_id="red-abc",
                            auto_provision=InstanceConfiguration(
                                plan="starter",
                                maxmemory_policy=MaxmemoryPolicy.ALLKEYS_RANDOM,
                            ),
                        )
                    )

                assert api.find_by_id.call_count == 3

        class TestNewClientWithNameAndOwnerId:
            @pytest.mark.asyncio
            async def test_no_update_if_no_settings_set(self, client, api):
                api.find_by_name.side_effect = None
                api.find_by_name.return_value = make_detail(plan="starter")

                result = await client.new_client(
                    NameOwnerIdOptions(name="test-redis", owner_id="tea-abc")
                )

                assert result is not None
                api.update_instance.assert_not_called()
                api.find_by_name.assert_called_once()
                api.find_by_id.assert_not_called()

            @pytest.mark.asyncio
            async def test_no_update_if_config_matches(self, client, api):
                api.find_by_name.side_effect = None
                api.find_by_name.return_value = make_detail(
                    plan="starter", maxmemory_policy=MaxmemoryPolicy.ALLKEYS_LRU
                )

                result = await client.new_client(
                    NameOwnerIdOptions(
                        name="test-redis",
                        owner_id="tea-abc",
                        auto_provision=InstanceConfiguration(
                            plan="starter",
                            maxmemory_policy=MaxmemoryPolicy.ALLKEYS_LRU,
                        ),
                    )
                )

                assert result is not None
                api.update_instance.assert_not_called()
                api.find_by_name.assert_called_once()
                api.find_by_id.assert_not_called()

            @pytest.mark.asyncio
            async def test_sends_patch_if_changes_needed(self, client, api):
                api.find_by_name.side_effect = None
                api.find_by_name.return_value = make_detail(
                    plan="free", maxmemory_policy=MaxmemoryPolicy.ALLKEYS_LRU
                )
                api.update_instance.side_effect = RenderError("early exit")

                with pytest.raises(RenderError):
                    await client.new_client(
                        NameOwnerIdOptions(
                            name="test-redis",
                            owner_id="tea-abc",
                            auto_provision=InstanceConfiguration(
                                plan="starter",
                                maxmemory_policy=MaxmemoryPolicy.ALLKEYS_RANDOM,
                            ),
                        )
                    )

                api.update_instance.assert_called_once()
                assert api.update_instance.call_args.args[0] == "red-abc"
                patch = api.update_instance.call_args.args[1]
                assert patch.plan == KeyValuePlan.STARTER
                assert patch.maxmemory_policy == MaxmemoryPolicy.ALLKEYS_RANDOM

            @pytest.mark.asyncio
            async def test_waits_for_available_after_update(self, client, api):
                api.find_by_name.side_effect = None
                api.find_by_name.return_value = make_detail(
                    plan="free", maxmemory_policy=MaxmemoryPolicy.ALLKEYS_LRU
                )
                updating = make_detail(
                    plan="starter",
                    maxmemory_policy=MaxmemoryPolicy.ALLKEYS_RANDOM,
                    status=DatabaseStatus.UPDATING_INSTANCE,
                )
                available = make_detail(
                    plan="starter", maxmemory_policy=MaxmemoryPolicy.ALLKEYS_RANDOM
                )
                api.find_by_id.side_effect = [updating, available]
                api.update_instance.side_effect = None
                api.update_instance.return_value = updating

                result = await client.new_client(
                    NameOwnerIdOptions(
                        name="test-redis",
                        owner_id="tea-abc",
                        auto_provision=InstanceConfiguration(
                            plan="starter",
                            maxmemory_policy=MaxmemoryPolicy.ALLKEYS_RANDOM,
                        ),
                    )
                )

                assert result is not None
                assert api.find_by_id.call_count == 2

            @pytest.mark.asyncio
            async def test_errors_on_unrecoverable_state_after_update(
                self, client, api
            ):
                api.find_by_name.side_effect = None
                api.find_by_name.return_value = make_detail(
                    plan="free", maxmemory_policy=MaxmemoryPolicy.ALLKEYS_LRU
                )
                updating = make_detail(
                    plan="starter",
                    status=DatabaseStatus.UPDATING_INSTANCE,
                )
                failed = make_detail(
                    plan="starter", status=DatabaseStatus.RECOVERY_FAILED
                )
                api.find_by_id.side_effect = [updating, failed]
                api.update_instance.side_effect = None
                api.update_instance.return_value = updating

                with pytest.raises(RenderError, match="instance is not available"):
                    await client.new_client(
                        NameOwnerIdOptions(
                            name="test-redis",
                            owner_id="tea-abc",
                            auto_provision=InstanceConfiguration(
                                plan="starter",
                                maxmemory_policy=MaxmemoryPolicy.ALLKEYS_RANDOM,
                            ),
                        )
                    )

                assert api.find_by_id.call_count == 2

        class TestConnectionInfoWithServiceId:
            @pytest.mark.asyncio
            async def test_no_update_if_no_settings_set(self, client, api):
                api.find_by_id.side_effect = None
                api.find_by_id.return_value = make_detail(plan="starter")

                result = await client.connection_info(
                    ServiceIdOptions(service_id="red-abc")
                )

                assert result.username == "user"
                assert (
                    result.password == "pass"  # noqa: S105 (not a hardcoded password)
                )
                assert result.host == "localhosta"
                assert result.port == 6239
                api.update_instance.assert_not_called()
                assert api.find_by_id.call_count == 1

            @pytest.mark.asyncio
            async def test_no_update_if_config_matches(self, client, api):
                api.find_by_id.side_effect = None
                api.find_by_id.return_value = make_detail(
                    plan="starter", maxmemory_policy=MaxmemoryPolicy.ALLKEYS_LRU
                )

                result = await client.connection_info(
                    ServiceIdOptions(
                        service_id="red-abc",
                        auto_provision=InstanceConfiguration(
                            plan="starter",
                            maxmemory_policy=MaxmemoryPolicy.ALLKEYS_LRU,
                        ),
                    )
                )

                assert result.host == "localhosta"
                api.update_instance.assert_not_called()
                assert api.find_by_id.call_count == 1

            @pytest.mark.asyncio
            async def test_sends_patch_if_changes_needed(self, client, api):
                api.find_by_id.side_effect = None
                api.find_by_id.return_value = make_detail(
                    plan="free", maxmemory_policy=MaxmemoryPolicy.ALLKEYS_LRU
                )
                api.update_instance.side_effect = RenderError("early exit")

                with pytest.raises(RenderError):
                    await client.connection_info(
                        ServiceIdOptions(
                            service_id="red-abc",
                            auto_provision=InstanceConfiguration(
                                plan="starter",
                                maxmemory_policy=MaxmemoryPolicy.ALLKEYS_RANDOM,
                            ),
                        )
                    )

                api.update_instance.assert_called_once()
                assert api.update_instance.call_args.args[0] == "red-abc"

            @pytest.mark.asyncio
            async def test_waits_for_available_after_update(self, client, api):
                available = make_detail(
                    plan="starter", maxmemory_policy=MaxmemoryPolicy.ALLKEYS_RANDOM
                )
                updating = make_detail(
                    plan="starter",
                    maxmemory_policy=MaxmemoryPolicy.ALLKEYS_RANDOM,
                    status=DatabaseStatus.UPDATING_INSTANCE,
                )
                api.find_by_id.side_effect = [
                    make_detail(
                        plan="free", maxmemory_policy=MaxmemoryPolicy.ALLKEYS_LRU
                    ),
                    updating,
                    available,
                ]
                api.update_instance.side_effect = None
                api.update_instance.return_value = updating

                result = await client.connection_info(
                    ServiceIdOptions(
                        service_id="red-abc",
                        auto_provision=InstanceConfiguration(
                            plan="starter",
                            maxmemory_policy=MaxmemoryPolicy.ALLKEYS_RANDOM,
                        ),
                    )
                )

                assert result.host == "localhosta"
                assert api.find_by_id.call_count == 3

            @pytest.mark.asyncio
            async def test_errors_on_unrecoverable_state_after_update(
                self, client, api
            ):
                updating = make_detail(
                    plan="starter",
                    status=DatabaseStatus.UPDATING_INSTANCE,
                )
                failed = make_detail(
                    plan="starter", status=DatabaseStatus.RECOVERY_FAILED
                )
                api.find_by_id.side_effect = [
                    make_detail(plan="free"),
                    updating,
                    failed,
                ]
                api.update_instance.side_effect = None
                api.update_instance.return_value = updating

                with pytest.raises(RenderError, match="instance is not available"):
                    await client.connection_info(
                        ServiceIdOptions(
                            service_id="red-abc",
                            auto_provision=InstanceConfiguration(
                                plan="starter",
                                maxmemory_policy=MaxmemoryPolicy.ALLKEYS_RANDOM,
                            ),
                        )
                    )

                assert api.find_by_id.call_count == 3

        class TestConnectionInfoWithNameAndOwnerId:
            @pytest.mark.asyncio
            async def test_no_update_if_no_settings_set(self, client, api):
                api.find_by_name.side_effect = None
                api.find_by_name.return_value = make_detail(plan="starter")

                result = await client.connection_info(
                    NameOwnerIdOptions(name="test-redis", owner_id="tea-abc")
                )

                assert result.username == "user"
                assert (
                    result.password == "pass"  # noqa: S105 (not a hardcoded password)
                )
                assert result.host == "localhosta"
                assert result.port == 6239
                api.update_instance.assert_not_called()
                api.find_by_name.assert_called_once()
                api.find_by_id.assert_not_called()

            @pytest.mark.asyncio
            async def test_no_update_if_config_matches(self, client, api):
                api.find_by_name.side_effect = None
                api.find_by_name.return_value = make_detail(
                    plan="starter", maxmemory_policy=MaxmemoryPolicy.ALLKEYS_LRU
                )

                result = await client.connection_info(
                    NameOwnerIdOptions(
                        name="test-redis",
                        owner_id="tea-abc",
                        auto_provision=InstanceConfiguration(
                            plan="starter",
                            maxmemory_policy=MaxmemoryPolicy.ALLKEYS_LRU,
                        ),
                    )
                )

                assert result.host == "localhosta"
                api.update_instance.assert_not_called()
                api.find_by_name.assert_called_once()
                api.find_by_id.assert_not_called()

            @pytest.mark.asyncio
            async def test_sends_patch_if_changes_needed(self, client, api):
                api.find_by_name.side_effect = None
                api.find_by_name.return_value = make_detail(
                    plan="free", maxmemory_policy=MaxmemoryPolicy.ALLKEYS_LRU
                )
                api.update_instance.side_effect = RenderError("early exit")

                with pytest.raises(RenderError):
                    await client.connection_info(
                        NameOwnerIdOptions(
                            name="test-redis",
                            owner_id="tea-abc",
                            auto_provision=InstanceConfiguration(
                                plan="starter",
                                maxmemory_policy=MaxmemoryPolicy.ALLKEYS_RANDOM,
                            ),
                        )
                    )

                api.update_instance.assert_called_once()
                assert api.update_instance.call_args.args[0] == "red-abc"

            @pytest.mark.asyncio
            async def test_waits_for_available_after_update(self, client, api):
                api.find_by_name.side_effect = None
                api.find_by_name.return_value = make_detail(
                    plan="free", maxmemory_policy=MaxmemoryPolicy.ALLKEYS_LRU
                )
                updating = make_detail(
                    plan="starter",
                    maxmemory_policy=MaxmemoryPolicy.ALLKEYS_RANDOM,
                    status=DatabaseStatus.UPDATING_INSTANCE,
                )
                available = make_detail(
                    plan="starter", maxmemory_policy=MaxmemoryPolicy.ALLKEYS_RANDOM
                )
                api.find_by_id.side_effect = [updating, available]
                api.update_instance.side_effect = None
                api.update_instance.return_value = updating

                result = await client.connection_info(
                    NameOwnerIdOptions(
                        name="test-redis",
                        owner_id="tea-abc",
                        auto_provision=InstanceConfiguration(
                            plan="starter",
                            maxmemory_policy=MaxmemoryPolicy.ALLKEYS_RANDOM,
                        ),
                    )
                )

                assert result.host == "localhosta"
                assert api.find_by_id.call_count == 2

            @pytest.mark.asyncio
            async def test_errors_on_unrecoverable_state_after_update(
                self, client, api
            ):
                api.find_by_name.side_effect = None
                api.find_by_name.return_value = make_detail(
                    plan="free", maxmemory_policy=MaxmemoryPolicy.ALLKEYS_LRU
                )
                updating = make_detail(
                    plan="starter",
                    status=DatabaseStatus.UPDATING_INSTANCE,
                )
                failed = make_detail(
                    plan="starter", status=DatabaseStatus.RECOVERY_FAILED
                )
                api.find_by_id.side_effect = [updating, failed]
                api.update_instance.side_effect = None
                api.update_instance.return_value = updating

                with pytest.raises(RenderError, match="instance is not available"):
                    await client.connection_info(
                        NameOwnerIdOptions(
                            name="test-redis",
                            owner_id="tea-abc",
                            auto_provision=InstanceConfiguration(
                                plan="starter",
                                maxmemory_policy=MaxmemoryPolicy.ALLKEYS_RANDOM,
                            ),
                        )
                    )

                assert api.find_by_id.call_count == 2
