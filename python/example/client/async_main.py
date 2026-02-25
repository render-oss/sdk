#!/usr/bin/env python3
"""
Render Python Async Client Example

This example demonstrates how to use the RenderAsync client for async
contexts (e.g. FastAPI, async scripts). For synchronous contexts, the
Render client (see main.py) is the safer default.

Setup:
1. Set your Render API token: export RENDER_API_KEY="your_token_here"
2. Replace "your-task-name" with an actual task from your Render dashboard
3. Run: poetry run python example/client/async_main.py
"""

import asyncio
from typing import Any

from render_sdk import RenderAsync
from render_sdk.client import ListTaskRunsParams
from render_sdk.client.errors import RenderError, TaskRunError


async def main():
    """Demonstrate async workflow operations using the RenderAsync client."""
    # Create client (uses RENDER_API_KEY from environment)
    render = RenderAsync()

    # Replace with your workflow slug and task identifier
    task_identifier = "my-workflow-slug/task-name"
    # Input data can be specified as a list of positional arguments or a
    # dictionary of named arguments
    input_data: dict[str, Any] = {"arg1": 3}

    # run_task() starts a task and waits for the result in one call
    result = await render.workflows.run_task(task_identifier, input_data)
    print(f"Task completed: {result.status}, results: {result.results}")

    # start_task() returns an awaitable task run for fire-and-forget or deferred waiting
    task_run = await render.workflows.start_task(task_identifier, input_data)
    print(f"Task started with ID: {task_run.id}")

    # Wait for task completion by awaiting the task run
    try:
        result = await task_run
        print(f"Task completed: {result.status}, results: {result.results}")
    except TaskRunError as e:
        print(f"Task failed or was cancelled: {e}")
    except RenderError as e:
        print(f"Error waiting for task: {e}")

    # Stream task run events directly. This is useful when you want to monitor
    # multiple task runs or handle events as they arrive.
    task_run2 = await render.workflows.start_task(task_identifier, input_data)
    print("Streaming task run events...")
    async for event in render.workflows.task_run_events([task_run2.id]):
        print(f"  Event: {event.id} status={event.status}")
        if event.error:
            print(f"  Error: {event.error}")

    # Get task run details by ID
    details = await render.workflows.get_task_run(task_run.id)
    print(f"Task run details: {details.id} status={details.status}")

    # Cancel a task run
    task_run3 = await render.workflows.start_task(task_identifier, input_data)
    await render.workflows.cancel_task_run(task_run3.id)
    print(f"Cancelled task run: {task_run3.id}")

    # List recent task runs
    params = ListTaskRunsParams(limit=5)
    task_runs = await render.workflows.list_task_runs(params)
    print(f"Found {len(task_runs)} recent task runs")
    for i, tr in enumerate(task_runs, 1):
        print(f"  {i}. {tr.id} {tr.status}")


if __name__ == "__main__":
    asyncio.run(main())
