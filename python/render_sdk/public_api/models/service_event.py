import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.service_event_type import ServiceEventType

if TYPE_CHECKING:
    from ..models.autoscaling_config_changed import AutoscalingConfigChanged
    from ..models.autoscaling_ended import AutoscalingEnded
    from ..models.autoscaling_started import AutoscalingStarted
    from ..models.branch_deleted import BranchDeleted
    from ..models.build_ended import BuildEnded
    from ..models.build_started import BuildStarted
    from ..models.commit_ignored import CommitIgnored
    from ..models.cron_job_run_ended import CronJobRunEnded
    from ..models.cron_job_run_started import CronJobRunStarted
    from ..models.deploy_ended import DeployEnded
    from ..models.deploy_started import DeployStarted
    from ..models.disk_created import DiskCreated
    from ..models.disk_deleted import DiskDeleted
    from ..models.disk_updated import DiskUpdated
    from ..models.edge_cache_disabled import EdgeCacheDisabled
    from ..models.edge_cache_enabled import EdgeCacheEnabled
    from ..models.edge_cache_purged import EdgeCachePurged
    from ..models.image_pull_failed import ImagePullFailed
    from ..models.initial_deploy_hook_ended import InitialDeployHookEnded
    from ..models.initial_deploy_hook_started import InitialDeployHookStarted
    from ..models.instance_count_changed import InstanceCountChanged
    from ..models.instance_type_changed import InstanceTypeChanged
    from ..models.job_run_ended import JobRunEnded
    from ..models.maintenance_ended import MaintenanceEnded
    from ..models.maintenance_mode_enabled import MaintenanceModeEnabled
    from ..models.maintenance_mode_uri_updated import MaintenanceModeURIUpdated
    from ..models.maintenance_started import MaintenanceStarted
    from ..models.pipeline_minutes_exhausted import PipelineMinutesExhausted
    from ..models.pre_deploy_ended import PreDeployEnded
    from ..models.pre_deploy_started import PreDeployStarted
    from ..models.server_available import ServerAvailable
    from ..models.server_failed import ServerFailed
    from ..models.server_hardware_failure import ServerHardwareFailure
    from ..models.server_restarted import ServerRestarted
    from ..models.server_unhealthy import ServerUnhealthy
    from ..models.service_resumed import ServiceResumed
    from ..models.service_suspended import ServiceSuspended
    from ..models.suspender_added import SuspenderAdded
    from ..models.suspender_removed import SuspenderRemoved
    from ..models.zero_downtime_redeploy_ended import ZeroDowntimeRedeployEnded
    from ..models.zero_downtime_redeploy_started import ZeroDowntimeRedeployStarted


T = TypeVar("T", bound="ServiceEvent")


@_attrs_define
class ServiceEvent:
    """
    Attributes:
        id (str):  Example: evt-cph1rs3idesc73a2b2mg.
        timestamp (datetime.datetime):
        service_id (str):
        type_ (ServiceEventType):
        details (Union['AutoscalingConfigChanged', 'AutoscalingEnded', 'AutoscalingStarted', 'BranchDeleted',
            'BuildEnded', 'BuildStarted', 'CommitIgnored', 'CronJobRunEnded', 'CronJobRunStarted', 'DeployEnded',
            'DeployStarted', 'DiskCreated', 'DiskDeleted', 'DiskUpdated', 'EdgeCacheDisabled', 'EdgeCacheEnabled',
            'EdgeCachePurged', 'ImagePullFailed', 'InitialDeployHookEnded', 'InitialDeployHookStarted',
            'InstanceCountChanged', 'InstanceTypeChanged', 'JobRunEnded', 'MaintenanceEnded', 'MaintenanceModeEnabled',
            'MaintenanceModeURIUpdated', 'MaintenanceStarted', 'PipelineMinutesExhausted', 'PreDeployEnded',
            'PreDeployStarted', 'ServerAvailable', 'ServerFailed', 'ServerHardwareFailure', 'ServerRestarted',
            'ServerUnhealthy', 'ServiceResumed', 'ServiceSuspended', 'SuspenderAdded', 'SuspenderRemoved',
            'ZeroDowntimeRedeployEnded', 'ZeroDowntimeRedeployStarted']):
    """

    id: str
    timestamp: datetime.datetime
    service_id: str
    type_: ServiceEventType
    details: Union[
        "AutoscalingConfigChanged",
        "AutoscalingEnded",
        "AutoscalingStarted",
        "BranchDeleted",
        "BuildEnded",
        "BuildStarted",
        "CommitIgnored",
        "CronJobRunEnded",
        "CronJobRunStarted",
        "DeployEnded",
        "DeployStarted",
        "DiskCreated",
        "DiskDeleted",
        "DiskUpdated",
        "EdgeCacheDisabled",
        "EdgeCacheEnabled",
        "EdgeCachePurged",
        "ImagePullFailed",
        "InitialDeployHookEnded",
        "InitialDeployHookStarted",
        "InstanceCountChanged",
        "InstanceTypeChanged",
        "JobRunEnded",
        "MaintenanceEnded",
        "MaintenanceModeEnabled",
        "MaintenanceModeURIUpdated",
        "MaintenanceStarted",
        "PipelineMinutesExhausted",
        "PreDeployEnded",
        "PreDeployStarted",
        "ServerAvailable",
        "ServerFailed",
        "ServerHardwareFailure",
        "ServerRestarted",
        "ServerUnhealthy",
        "ServiceResumed",
        "ServiceSuspended",
        "SuspenderAdded",
        "SuspenderRemoved",
        "ZeroDowntimeRedeployEnded",
        "ZeroDowntimeRedeployStarted",
    ]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.autoscaling_config_changed import AutoscalingConfigChanged
        from ..models.autoscaling_ended import AutoscalingEnded
        from ..models.autoscaling_started import AutoscalingStarted
        from ..models.branch_deleted import BranchDeleted
        from ..models.build_ended import BuildEnded
        from ..models.build_started import BuildStarted
        from ..models.commit_ignored import CommitIgnored
        from ..models.cron_job_run_ended import CronJobRunEnded
        from ..models.cron_job_run_started import CronJobRunStarted
        from ..models.deploy_ended import DeployEnded
        from ..models.deploy_started import DeployStarted
        from ..models.disk_created import DiskCreated
        from ..models.disk_deleted import DiskDeleted
        from ..models.disk_updated import DiskUpdated
        from ..models.edge_cache_disabled import EdgeCacheDisabled
        from ..models.edge_cache_enabled import EdgeCacheEnabled
        from ..models.image_pull_failed import ImagePullFailed
        from ..models.initial_deploy_hook_ended import InitialDeployHookEnded
        from ..models.initial_deploy_hook_started import InitialDeployHookStarted
        from ..models.instance_count_changed import InstanceCountChanged
        from ..models.instance_type_changed import InstanceTypeChanged
        from ..models.job_run_ended import JobRunEnded
        from ..models.maintenance_ended import MaintenanceEnded
        from ..models.maintenance_mode_enabled import MaintenanceModeEnabled
        from ..models.maintenance_mode_uri_updated import MaintenanceModeURIUpdated
        from ..models.maintenance_started import MaintenanceStarted
        from ..models.pipeline_minutes_exhausted import PipelineMinutesExhausted
        from ..models.pre_deploy_ended import PreDeployEnded
        from ..models.pre_deploy_started import PreDeployStarted
        from ..models.server_available import ServerAvailable
        from ..models.server_failed import ServerFailed
        from ..models.server_hardware_failure import ServerHardwareFailure
        from ..models.server_restarted import ServerRestarted
        from ..models.server_unhealthy import ServerUnhealthy
        from ..models.service_resumed import ServiceResumed
        from ..models.service_suspended import ServiceSuspended
        from ..models.suspender_added import SuspenderAdded
        from ..models.suspender_removed import SuspenderRemoved
        from ..models.zero_downtime_redeploy_ended import ZeroDowntimeRedeployEnded
        from ..models.zero_downtime_redeploy_started import ZeroDowntimeRedeployStarted

        id = self.id

        timestamp = self.timestamp.isoformat()

        service_id = self.service_id

        type_ = self.type_.value

        details: dict[str, Any]
        if isinstance(self.details, AutoscalingConfigChanged):
            details = self.details.to_dict()
        elif isinstance(self.details, AutoscalingEnded):
            details = self.details.to_dict()
        elif isinstance(self.details, AutoscalingStarted):
            details = self.details.to_dict()
        elif isinstance(self.details, BranchDeleted):
            details = self.details.to_dict()
        elif isinstance(self.details, BuildEnded):
            details = self.details.to_dict()
        elif isinstance(self.details, BuildStarted):
            details = self.details.to_dict()
        elif isinstance(self.details, CommitIgnored):
            details = self.details.to_dict()
        elif isinstance(self.details, CronJobRunEnded):
            details = self.details.to_dict()
        elif isinstance(self.details, CronJobRunStarted):
            details = self.details.to_dict()
        elif isinstance(self.details, DeployEnded):
            details = self.details.to_dict()
        elif isinstance(self.details, DeployStarted):
            details = self.details.to_dict()
        elif isinstance(self.details, DiskCreated):
            details = self.details.to_dict()
        elif isinstance(self.details, DiskUpdated):
            details = self.details.to_dict()
        elif isinstance(self.details, DiskDeleted):
            details = self.details.to_dict()
        elif isinstance(self.details, ImagePullFailed):
            details = self.details.to_dict()
        elif isinstance(self.details, InitialDeployHookStarted):
            details = self.details.to_dict()
        elif isinstance(self.details, InitialDeployHookEnded):
            details = self.details.to_dict()
        elif isinstance(self.details, InstanceCountChanged):
            details = self.details.to_dict()
        elif isinstance(self.details, JobRunEnded):
            details = self.details.to_dict()
        elif isinstance(self.details, MaintenanceModeEnabled):
            details = self.details.to_dict()
        elif isinstance(self.details, MaintenanceModeURIUpdated):
            details = self.details.to_dict()
        elif isinstance(self.details, MaintenanceEnded):
            details = self.details.to_dict()
        elif isinstance(self.details, MaintenanceStarted):
            details = self.details.to_dict()
        elif isinstance(self.details, PipelineMinutesExhausted):
            details = self.details.to_dict()
        elif isinstance(self.details, InstanceTypeChanged):
            details = self.details.to_dict()
        elif isinstance(self.details, PreDeployEnded):
            details = self.details.to_dict()
        elif isinstance(self.details, PreDeployStarted):
            details = self.details.to_dict()
        elif isinstance(self.details, ServerAvailable):
            details = self.details.to_dict()
        elif isinstance(self.details, ServerFailed):
            details = self.details.to_dict()
        elif isinstance(self.details, ServerHardwareFailure):
            details = self.details.to_dict()
        elif isinstance(self.details, ServerRestarted):
            details = self.details.to_dict()
        elif isinstance(self.details, ServerUnhealthy):
            details = self.details.to_dict()
        elif isinstance(self.details, ServiceResumed):
            details = self.details.to_dict()
        elif isinstance(self.details, ServiceSuspended):
            details = self.details.to_dict()
        elif isinstance(self.details, SuspenderAdded):
            details = self.details.to_dict()
        elif isinstance(self.details, SuspenderRemoved):
            details = self.details.to_dict()
        elif isinstance(self.details, ZeroDowntimeRedeployEnded):
            details = self.details.to_dict()
        elif isinstance(self.details, ZeroDowntimeRedeployStarted):
            details = self.details.to_dict()
        elif isinstance(self.details, EdgeCacheDisabled):
            details = self.details.to_dict()
        elif isinstance(self.details, EdgeCacheEnabled):
            details = self.details.to_dict()
        else:
            details = self.details.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "timestamp": timestamp,
                "serviceId": service_id,
                "type": type_,
                "details": details,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.autoscaling_config_changed import AutoscalingConfigChanged
        from ..models.autoscaling_ended import AutoscalingEnded
        from ..models.autoscaling_started import AutoscalingStarted
        from ..models.branch_deleted import BranchDeleted
        from ..models.build_ended import BuildEnded
        from ..models.build_started import BuildStarted
        from ..models.commit_ignored import CommitIgnored
        from ..models.cron_job_run_ended import CronJobRunEnded
        from ..models.cron_job_run_started import CronJobRunStarted
        from ..models.deploy_ended import DeployEnded
        from ..models.deploy_started import DeployStarted
        from ..models.disk_created import DiskCreated
        from ..models.disk_deleted import DiskDeleted
        from ..models.disk_updated import DiskUpdated
        from ..models.edge_cache_disabled import EdgeCacheDisabled
        from ..models.edge_cache_enabled import EdgeCacheEnabled
        from ..models.edge_cache_purged import EdgeCachePurged
        from ..models.image_pull_failed import ImagePullFailed
        from ..models.initial_deploy_hook_ended import InitialDeployHookEnded
        from ..models.initial_deploy_hook_started import InitialDeployHookStarted
        from ..models.instance_count_changed import InstanceCountChanged
        from ..models.instance_type_changed import InstanceTypeChanged
        from ..models.job_run_ended import JobRunEnded
        from ..models.maintenance_ended import MaintenanceEnded
        from ..models.maintenance_mode_enabled import MaintenanceModeEnabled
        from ..models.maintenance_mode_uri_updated import MaintenanceModeURIUpdated
        from ..models.maintenance_started import MaintenanceStarted
        from ..models.pipeline_minutes_exhausted import PipelineMinutesExhausted
        from ..models.pre_deploy_ended import PreDeployEnded
        from ..models.pre_deploy_started import PreDeployStarted
        from ..models.server_available import ServerAvailable
        from ..models.server_failed import ServerFailed
        from ..models.server_hardware_failure import ServerHardwareFailure
        from ..models.server_restarted import ServerRestarted
        from ..models.server_unhealthy import ServerUnhealthy
        from ..models.service_resumed import ServiceResumed
        from ..models.service_suspended import ServiceSuspended
        from ..models.suspender_added import SuspenderAdded
        from ..models.suspender_removed import SuspenderRemoved
        from ..models.zero_downtime_redeploy_ended import ZeroDowntimeRedeployEnded
        from ..models.zero_downtime_redeploy_started import ZeroDowntimeRedeployStarted

        d = dict(src_dict)
        id = d.pop("id")

        timestamp = isoparse(d.pop("timestamp"))

        service_id = d.pop("serviceId")

        type_ = ServiceEventType(d.pop("type"))

        def _parse_details(
            data: object,
        ) -> Union[
            "AutoscalingConfigChanged",
            "AutoscalingEnded",
            "AutoscalingStarted",
            "BranchDeleted",
            "BuildEnded",
            "BuildStarted",
            "CommitIgnored",
            "CronJobRunEnded",
            "CronJobRunStarted",
            "DeployEnded",
            "DeployStarted",
            "DiskCreated",
            "DiskDeleted",
            "DiskUpdated",
            "EdgeCacheDisabled",
            "EdgeCacheEnabled",
            "EdgeCachePurged",
            "ImagePullFailed",
            "InitialDeployHookEnded",
            "InitialDeployHookStarted",
            "InstanceCountChanged",
            "InstanceTypeChanged",
            "JobRunEnded",
            "MaintenanceEnded",
            "MaintenanceModeEnabled",
            "MaintenanceModeURIUpdated",
            "MaintenanceStarted",
            "PipelineMinutesExhausted",
            "PreDeployEnded",
            "PreDeployStarted",
            "ServerAvailable",
            "ServerFailed",
            "ServerHardwareFailure",
            "ServerRestarted",
            "ServerUnhealthy",
            "ServiceResumed",
            "ServiceSuspended",
            "SuspenderAdded",
            "SuspenderRemoved",
            "ZeroDowntimeRedeployEnded",
            "ZeroDowntimeRedeployStarted",
        ]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasservice_event_details_type_0 = AutoscalingConfigChanged.from_dict(data)

                return componentsschemasservice_event_details_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasservice_event_details_type_1 = AutoscalingEnded.from_dict(data)

                return componentsschemasservice_event_details_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasservice_event_details_type_2 = AutoscalingStarted.from_dict(data)

                return componentsschemasservice_event_details_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasservice_event_details_type_3 = BranchDeleted.from_dict(data)

                return componentsschemasservice_event_details_type_3
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasservice_event_details_type_4 = BuildEnded.from_dict(data)

                return componentsschemasservice_event_details_type_4
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasservice_event_details_type_5 = BuildStarted.from_dict(data)

                return componentsschemasservice_event_details_type_5
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasservice_event_details_type_6 = CommitIgnored.from_dict(data)

                return componentsschemasservice_event_details_type_6
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasservice_event_details_type_7 = CronJobRunEnded.from_dict(data)

                return componentsschemasservice_event_details_type_7
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasservice_event_details_type_8 = CronJobRunStarted.from_dict(data)

                return componentsschemasservice_event_details_type_8
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasservice_event_details_type_9 = DeployEnded.from_dict(data)

                return componentsschemasservice_event_details_type_9
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasservice_event_details_type_10 = DeployStarted.from_dict(data)

                return componentsschemasservice_event_details_type_10
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasservice_event_details_type_11 = DiskCreated.from_dict(data)

                return componentsschemasservice_event_details_type_11
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasservice_event_details_type_12 = DiskUpdated.from_dict(data)

                return componentsschemasservice_event_details_type_12
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasservice_event_details_type_13 = DiskDeleted.from_dict(data)

                return componentsschemasservice_event_details_type_13
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasservice_event_details_type_14 = ImagePullFailed.from_dict(data)

                return componentsschemasservice_event_details_type_14
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasservice_event_details_type_15 = InitialDeployHookStarted.from_dict(data)

                return componentsschemasservice_event_details_type_15
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasservice_event_details_type_16 = InitialDeployHookEnded.from_dict(data)

                return componentsschemasservice_event_details_type_16
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasservice_event_details_type_17 = InstanceCountChanged.from_dict(data)

                return componentsschemasservice_event_details_type_17
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasservice_event_details_type_18 = JobRunEnded.from_dict(data)

                return componentsschemasservice_event_details_type_18
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasservice_event_details_type_19 = MaintenanceModeEnabled.from_dict(data)

                return componentsschemasservice_event_details_type_19
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasservice_event_details_type_20 = MaintenanceModeURIUpdated.from_dict(data)

                return componentsschemasservice_event_details_type_20
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasservice_event_details_type_21 = MaintenanceEnded.from_dict(data)

                return componentsschemasservice_event_details_type_21
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasservice_event_details_type_22 = MaintenanceStarted.from_dict(data)

                return componentsschemasservice_event_details_type_22
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasservice_event_details_type_23 = PipelineMinutesExhausted.from_dict(data)

                return componentsschemasservice_event_details_type_23
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasservice_event_details_type_24 = InstanceTypeChanged.from_dict(data)

                return componentsschemasservice_event_details_type_24
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasservice_event_details_type_25 = PreDeployEnded.from_dict(data)

                return componentsschemasservice_event_details_type_25
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasservice_event_details_type_26 = PreDeployStarted.from_dict(data)

                return componentsschemasservice_event_details_type_26
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasservice_event_details_type_27 = ServerAvailable.from_dict(data)

                return componentsschemasservice_event_details_type_27
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasservice_event_details_type_28 = ServerFailed.from_dict(data)

                return componentsschemasservice_event_details_type_28
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasservice_event_details_type_29 = ServerHardwareFailure.from_dict(data)

                return componentsschemasservice_event_details_type_29
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasservice_event_details_type_30 = ServerRestarted.from_dict(data)

                return componentsschemasservice_event_details_type_30
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasservice_event_details_type_31 = ServerUnhealthy.from_dict(data)

                return componentsschemasservice_event_details_type_31
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasservice_event_details_type_32 = ServiceResumed.from_dict(data)

                return componentsschemasservice_event_details_type_32
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasservice_event_details_type_33 = ServiceSuspended.from_dict(data)

                return componentsschemasservice_event_details_type_33
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasservice_event_details_type_34 = SuspenderAdded.from_dict(data)

                return componentsschemasservice_event_details_type_34
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasservice_event_details_type_35 = SuspenderRemoved.from_dict(data)

                return componentsschemasservice_event_details_type_35
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasservice_event_details_type_36 = ZeroDowntimeRedeployEnded.from_dict(data)

                return componentsschemasservice_event_details_type_36
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasservice_event_details_type_37 = ZeroDowntimeRedeployStarted.from_dict(data)

                return componentsschemasservice_event_details_type_37
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasservice_event_details_type_38 = EdgeCacheDisabled.from_dict(data)

                return componentsschemasservice_event_details_type_38
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasservice_event_details_type_39 = EdgeCacheEnabled.from_dict(data)

                return componentsschemasservice_event_details_type_39
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemasservice_event_details_type_40 = EdgeCachePurged.from_dict(data)

            return componentsschemasservice_event_details_type_40

        details = _parse_details(d.pop("details"))

        service_event = cls(
            id=id,
            timestamp=timestamp,
            service_id=service_id,
            type_=type_,
            details=details,
        )

        service_event.additional_properties = d
        return service_event

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
