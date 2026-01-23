"""Runner functionality for the Python SDK."""

import asyncio
import base64
import json
import logging
import os

from render_sdk.workflows.callback_api.models import (
    RetryConfig,
    Task,
    TaskOptions,
    TaskParameter,
    Tasks,
)
from render_sdk.workflows.callback_api.types import UNSET, Unset
from render_sdk.workflows.client import UDSClient
from render_sdk.workflows.executor import TaskExecutor
from render_sdk.workflows.task import ParameterInfo, get_task_registry

logger = logging.getLogger(__name__)


async def run_async(socket_path: str) -> None:
    """
    Run a single task execution asynchronously.

    It gets the input from the server, executes the task, and sends the result back.
    """
    logger.debug("Starting task runner")

    # Create client
    client = UDSClient(socket_path)

    try:
        # Get input from server
        logger.debug("Getting task input")
        input_response = await client.get_input()

        task_name = input_response.task_name
        raw_input = input_response.input_

        if not task_name:
            raise ValueError("No task name provided in input")

        # Parse the input
        if raw_input:
            # The input is base64 encoded JSON
            input_data = json.loads(base64.b64decode(raw_input).decode())
        else:
            input_data = []

        # Create executor and execute task
        task_registry = get_task_registry()
        executor = TaskExecutor(task_registry, client)

        logger.debug(f"Executing task: {task_name}")
        await executor.execute(task_name, input_data)
    except Exception:
        raise


def run(socket_path: str) -> None:
    """
    Run a single task execution (sync wrapper).
    """
    asyncio.run(run_async(socket_path))


async def register_async(socket_path: str) -> None:
    """
    Register all tasks with the server asynchronously.
    """
    logger.debug("Registering tasks")

    # Create client
    client = UDSClient(socket_path)

    try:
        # Get all registered tasks
        task_registry = get_task_registry()
        task_names = task_registry.get_task_names()

        # Convert to the format expected by the API
        tasks: list[Task] = []
        for name in task_names:
            task_info = task_registry.get_task(name)

            options = TaskOptions()
            # Add options if present
            if task_info and task_info.options:
                if task_info.options.retry:
                    retry = task_info.options.retry
                    options.retry = RetryConfig(
                        max_retries=retry.max_retries,
                        wait_duration_ms=retry.wait_duration,
                        factor=retry.backoff_scaling,
                    )
                if task_info.options.timeout_seconds:
                    options.timeout_seconds = task_info.options.timeout_seconds
                if task_info.options.plan:
                    options.plan = task_info.options.plan

            parameters: list[TaskParameter] | Unset = UNSET
            if task_info and task_info.parameters:
                parameters = [
                    _convert_parameter_info_to_api_model(param)
                    for param in task_info.parameters
                ]

            task_def = Task(name=name, options=options, parameters=parameters)
            tasks.append(task_def)

        # Register tasks with server
        logger.debug(f"Registering {len(tasks)} tasks: {[t.name for t in tasks]}")
        await client.register_tasks(Tasks(tasks=tasks))

        logger.debug("Tasks registered successfully")

    except Exception as e:
        logger.error(f"Task registration failed: {e}")
        raise


def register(socket_path: str) -> None:
    """
    Register all tasks with the server (sync wrapper).
    """
    asyncio.run(register_async(socket_path))


def start() -> None:
    """
    Start the task runner based on environment configuration.

    It reads the RENDER_SDK_MODE and RENDER_SDK_SOCKET_PATH environment variables
    to determine whether to run tasks or register them.
    """
    # Get configuration from environment
    mode = os.environ.get("RENDER_SDK_MODE")
    socket_path = os.environ.get("RENDER_SDK_SOCKET_PATH")

    if not mode:
        raise ValueError("RENDER_SDK_MODE environment variable is required")

    if not socket_path:
        raise ValueError("RENDER_SDK_SOCKET_PATH environment variable is required")

    if mode == "run":
        run(socket_path)
    elif mode == "register":
        register(socket_path)
    else:
        raise ValueError(f"Unknown mode: {mode}")


def _convert_parameter_info_to_api_model(param_info: ParameterInfo) -> TaskParameter:
    """Convert internal ParameterInfo to API TaskParameter model."""
    # JSON-encode the default value if it exists
    default_value_str = None
    if param_info.has_default and param_info.default_value is not None:
        try:
            default_value_str = json.dumps(param_info.default_value)
        except (TypeError, ValueError):
            # If the default can't be serialized, skip it
            default_value_str = None

    return TaskParameter(
        name=param_info.name,
        has_default=param_info.has_default,
        type_=param_info.type_hint if param_info.type_hint is not None else UNSET,
        default_value=default_value_str if default_value_str is not None else UNSET,
    )
