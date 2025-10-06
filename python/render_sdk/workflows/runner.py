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
    Tasks,
)
from render_sdk.workflows.client import UDSClient
from render_sdk.workflows.executor import TaskExecutor
from render_sdk.workflows.task import get_task_registry

logger = logging.getLogger(__name__)


async def run_async(socket_path: str) -> None:
    """
    Run a single task execution asynchronously.

    It gets the input from the server, executes the task, and sends the result back.
    """
    logger.info("Starting task runner")

    # Create client
    client = UDSClient(socket_path)

    try:
        # Get input from server
        logger.info("Getting input from server")
        input_response = await client.get_input()

        logger.info(f"Input response: {input_response}")

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

        logger.info(f"Received input - task: {task_name}, input: {input_data}")

        # Create executor and execute task
        task_registry = get_task_registry()
        executor = TaskExecutor(task_registry, client)

        result = await executor.execute(task_name, input_data)

        logger.info(f"Task executed successfully with result: {result}")

    except Exception as e:
        logger.error(f"Task execution failed: {e}")
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
    logger.info("Registering tasks")

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
            if task_info and task_info.options and task_info.options.retry:
                retry = task_info.options.retry
                options.retry = RetryConfig(
                    max_retries=retry.max_retries,
                    wait_duration_ms=retry.wait_duration_ms,
                    factor=retry.factor,
                )

            task_def = Task(name=name, options=options)
            tasks.append(task_def)

        # Register tasks with server
        logger.info(f"Registering {len(tasks)} tasks: {[t.name for t in tasks]}")
        await client.register_tasks(Tasks(tasks=tasks))

        logger.info("Tasks registered successfully")

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

    logger.info(f"Starting in mode: {mode}")

    if mode == "run":
        run(socket_path)
    elif mode == "register":
        register(socket_path)
    else:
        raise ValueError(f"Unknown mode: {mode}")
