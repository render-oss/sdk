#!/usr/bin/env python3
"""Method parity tests between async and sync service classes.

These tests catch drift: a method added to one class but not its sync
counterpart, or a new async class added without a sync counterpart.
"""

import inspect

import pytest

from render_sdk.client.workflows import WorkflowsService
from render_sdk.client.workflows_sync import SyncWorkflowsService
from render_sdk.experimental.experimental import ExperimentalService, StorageService
from render_sdk.experimental.experimental_sync import (
    SyncExperimentalService,
    SyncStorageService,
)
from render_sdk.experimental.object.api import ObjectApi
from render_sdk.experimental.object.api_sync import SyncObjectApi
from render_sdk.experimental.object.client import ObjectClient, ScopedObjectClient
from render_sdk.experimental.object.client_sync import (
    SyncObjectClient,
    SyncScopedObjectClient,
)

# All async/sync class pairs. Add new pairs here when creating a new service.
ASYNC_SYNC_PAIRS = [
    (WorkflowsService, SyncWorkflowsService),
    (ExperimentalService, SyncExperimentalService),
    (StorageService, SyncStorageService),
    (ObjectApi, SyncObjectApi),
    (ObjectClient, SyncObjectClient),
    (ScopedObjectClient, SyncScopedObjectClient),
]

# Modules that contain async service classes. If you add a new module with
# async services, add it here so the discovery test catches missing pairs.
_ASYNC_SERVICE_MODULES = [
    "render_sdk.client.workflows",
    "render_sdk.experimental.experimental",
    "render_sdk.experimental.object.api",
    "render_sdk.experimental.object.client",
]


def _public_methods(cls):
    return {
        name
        for name in dir(cls)
        if not name.startswith("_") and callable(getattr(cls, name))
    }


def _assert_parity(async_cls, sync_cls):
    async_methods = _public_methods(async_cls)
    sync_methods = _public_methods(sync_cls)
    assert async_methods == sync_methods, (
        f"Method mismatch between {async_cls.__name__} and {sync_cls.__name__}.\n"
        f"  Only in async: {async_methods - sync_methods}\n"
        f"  Only in sync: {sync_methods - async_methods}"
    )


def _has_async_methods(cls):
    """Check if a class has any public async methods."""
    return any(
        inspect.iscoroutinefunction(getattr(cls, name))
        for name in dir(cls)
        if not name.startswith("_") and callable(getattr(cls, name))
    )


@pytest.mark.parametrize(
    "async_cls,sync_cls",
    ASYNC_SYNC_PAIRS,
    ids=[f"{a.__name__}" for a, _ in ASYNC_SYNC_PAIRS],
)
def test_method_parity(async_cls, sync_cls):
    """Each async class must have the same public methods as its sync counterpart."""
    _assert_parity(async_cls, sync_cls)


def test_all_async_classes_have_sync_counterparts():
    """Every async service class in the known modules must appear in ASYNC_SYNC_PAIRS.

    If this test fails, you added a new async service class without adding it
    to ASYNC_SYNC_PAIRS above (and without creating its sync counterpart).
    """
    import importlib

    tested_async_classes = {pair[0] for pair in ASYNC_SYNC_PAIRS}
    missing = []

    for module_path in _ASYNC_SERVICE_MODULES:
        module = importlib.import_module(module_path)
        for name in dir(module):
            obj = getattr(module, name)
            if (
                inspect.isclass(obj)
                and obj.__module__ == module_path
                and _has_async_methods(obj)
                and obj not in tested_async_classes
            ):
                missing.append(f"{module_path}.{name}")

    assert not missing, (
        f"Async service classes without sync parity tests: {missing}. "
        f"Add them to ASYNC_SYNC_PAIRS in test_method_parity.py."
    )
