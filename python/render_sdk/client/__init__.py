"""Render REST API Client

A Python client library for interacting with Render's REST API.

Symbols are lazy-loaded so the workflow worker path stays fast — importing
this package does not pull in the REST client or its models until a caller
actually references them.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from render_sdk.client.client import Client
    from render_sdk.client.types import (
        CursorParam,
        LimitParam,
        ListTaskRunsParams,
        OwnerIDParam,
        TaskData,
        TaskRun,
        TaskRunDetails,
        TaskRunStatus,
        TaskSlug,
    )
    from render_sdk.client.workflows import WorkflowsService
    from render_sdk.client.workflows_sync import SyncWorkflowsService
    from render_sdk.experimental import (
        DownloadResponse,
        ExperimentalService,
        ObjectApi,
        ObjectClient,
        ObjectData,
        OwnerID,
        PutObjectResult,
        Region,
        ScopedObjectClient,
        StorageService,
        SyncExperimentalService,
        SyncStorageService,
        UploadResponse,
    )

__all__ = [
    "Client",
    "WorkflowsService",
    "SyncWorkflowsService",
    "TaskData",
    "TaskSlug",
    "TaskRun",
    "TaskRunDetails",
    "TaskRunStatus",
    "ListTaskRunsParams",
    "LimitParam",
    "CursorParam",
    "OwnerIDParam",
    # Experimental exports
    "ExperimentalService",
    "StorageService",
    "SyncExperimentalService",
    "SyncStorageService",
    "ObjectApi",
    "ObjectClient",
    "ScopedObjectClient",
    "DownloadResponse",
    "ObjectData",
    "OwnerID",
    "PutObjectResult",
    "Region",
    "UploadResponse",
]


_LAZY_ATTRS = {
    "Client": ("render_sdk.client.client", "Client"),
    "WorkflowsService": ("render_sdk.client.workflows", "WorkflowsService"),
    "SyncWorkflowsService": (
        "render_sdk.client.workflows_sync",
        "SyncWorkflowsService",
    ),
    "TaskData": ("render_sdk.client.types", "TaskData"),
    "TaskSlug": ("render_sdk.client.types", "TaskSlug"),
    "TaskRun": ("render_sdk.client.types", "TaskRun"),
    "TaskRunDetails": ("render_sdk.client.types", "TaskRunDetails"),
    "TaskRunStatus": ("render_sdk.client.types", "TaskRunStatus"),
    "ListTaskRunsParams": ("render_sdk.client.types", "ListTaskRunsParams"),
    "LimitParam": ("render_sdk.client.types", "LimitParam"),
    "CursorParam": ("render_sdk.client.types", "CursorParam"),
    "OwnerIDParam": ("render_sdk.client.types", "OwnerIDParam"),
    "ExperimentalService": ("render_sdk.experimental", "ExperimentalService"),
    "StorageService": ("render_sdk.experimental", "StorageService"),
    "SyncExperimentalService": ("render_sdk.experimental", "SyncExperimentalService"),
    "SyncStorageService": ("render_sdk.experimental", "SyncStorageService"),
    "ObjectApi": ("render_sdk.experimental", "ObjectApi"),
    "ObjectClient": ("render_sdk.experimental", "ObjectClient"),
    "ScopedObjectClient": ("render_sdk.experimental", "ScopedObjectClient"),
    "DownloadResponse": ("render_sdk.experimental", "DownloadResponse"),
    "ObjectData": ("render_sdk.experimental", "ObjectData"),
    "OwnerID": ("render_sdk.experimental", "OwnerID"),
    "PutObjectResult": ("render_sdk.experimental", "PutObjectResult"),
    "Region": ("render_sdk.experimental", "Region"),
    "UploadResponse": ("render_sdk.experimental", "UploadResponse"),
}


def __getattr__(name: str):
    target = _LAZY_ATTRS.get(name)
    if target is None:
        raise AttributeError(f"module 'render_sdk.client' has no attribute {name!r}")

    import importlib

    module_name, attr_name = target
    value = getattr(importlib.import_module(module_name), attr_name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(_LAZY_ATTRS) | set(__all__))
