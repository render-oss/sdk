"""Render REST API Client

A Python client library for interacting with Render's REST API.

Symbols are lazy-loaded so the workflow worker path stays fast — importing
this package does not pull in the REST client or its models until a caller
actually references them.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from render.client.client import Client
    from render.client.types import (
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
    from render.client.workflows import WorkflowsService
    from render.client.workflows_sync import SyncWorkflowsService
    from render.experimental import (
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
    "Client": ("render.client.client", "Client"),
    "WorkflowsService": ("render.client.workflows", "WorkflowsService"),
    "SyncWorkflowsService": (
        "render.client.workflows_sync",
        "SyncWorkflowsService",
    ),
    "TaskData": ("render.client.types", "TaskData"),
    "TaskSlug": ("render.client.types", "TaskSlug"),
    "TaskRun": ("render.client.types", "TaskRun"),
    "TaskRunDetails": ("render.client.types", "TaskRunDetails"),
    "TaskRunStatus": ("render.client.types", "TaskRunStatus"),
    "ListTaskRunsParams": ("render.client.types", "ListTaskRunsParams"),
    "LimitParam": ("render.client.types", "LimitParam"),
    "CursorParam": ("render.client.types", "CursorParam"),
    "OwnerIDParam": ("render.client.types", "OwnerIDParam"),
    "ExperimentalService": ("render.experimental", "ExperimentalService"),
    "StorageService": ("render.experimental", "StorageService"),
    "SyncExperimentalService": ("render.experimental", "SyncExperimentalService"),
    "SyncStorageService": ("render.experimental", "SyncStorageService"),
    "ObjectApi": ("render.experimental", "ObjectApi"),
    "ObjectClient": ("render.experimental", "ObjectClient"),
    "ScopedObjectClient": ("render.experimental", "ScopedObjectClient"),
    "DownloadResponse": ("render.experimental", "DownloadResponse"),
    "ObjectData": ("render.experimental", "ObjectData"),
    "OwnerID": ("render.experimental", "OwnerID"),
    "PutObjectResult": ("render.experimental", "PutObjectResult"),
    "Region": ("render.experimental", "Region"),
    "UploadResponse": ("render.experimental", "UploadResponse"),
}


def __getattr__(name: str):
    target = _LAZY_ATTRS.get(name)
    if target is None:
        raise AttributeError(f"module 'render.client' has no attribute {name!r}")

    import importlib

    module_name, attr_name = target
    value = getattr(importlib.import_module(module_name), attr_name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(_LAZY_ATTRS) | set(__all__))
