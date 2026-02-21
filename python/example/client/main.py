#!/usr/bin/env python3
"""
Render Python Client Example

This example demonstrates how to use the Render Python REST API client
to interact with Render's workflows API. It shows both async and sync patterns,
task execution, monitoring, and error handling.

Setup:
1. Set your Render API token: export RENDER_API_KEY="your_token_here"
2. Replace "your-task-name" with an actual task from your Render dashboard
3. Run: poetry run python example/client/main.py
"""

import asyncio
from typing import Any

from render_sdk import Render
from render_sdk.client import ListTaskRunsParams
from render_sdk.client.errors import RenderError, TaskRunError


async def main():
    """Demonstrate async workflow operations using the Render client."""
    # Create client (uses RENDER_API_KEY from environment)
    render = Render()

    # Example task data - replace with your actual task
    task_identifier = "my-workflow-slug/task-name"  # Replace with your task identifier
    # Input data can be specified as a list of positional arguments or a
    # dictionary of named arguments
    input_data: dict[str, Any] = {"arg1": 3}

    # Run the task
    try:
        task_run = await render.workflows.run_task(task_identifier, input_data)
        print(f"Task started with ID: {task_run.id}")
    except Exception as e:
        print(f"Error running task: {e}")
        raise

    # Wait for completion using SSE streaming
    print("\n⏳ Waiting for task completion (using SSE streaming)...")
    try:
        result = await task_run
        print("✅ Task completed successfully!")
        print(f"   Final status: {result.status}")
        print(f"   Task run ID: {result.results}")
    except TaskRunError as e:
        print("❌ Task failed or was cancelled")
        print(f"   Final status: {result.status}")
        print(f"   Error: {e}")
    except RenderError as e:
        print(f"Error waiting for task completion: {e}")

    # Stream task run events directly
    # This is useful when you want to monitor multiple task runs
    # or handle events as they arrive
    print("\n📡 Streaming task run events...")
    task_run2 = await render.workflows.run_task(task_identifier, input_data)
    async for event in render.workflows.task_run_events([task_run2.id]):
        print(f"   Event: {event.id} status={event.status}")
        if event.error:
            print(f"   Error: {event.error}")

    # Get task run details by ID
    details = await render.workflows.get_task_run(task_run.id)
    print(f"\nTask run details: {details.id} status={details.status}")

    # Cancel a task run
    task_run3 = await render.workflows.run_task(task_identifier, input_data)
    await render.workflows.cancel_task_run(task_run3.id)
    print(f"Cancelled task run: {task_run3.id}")

    # List recent task runs
    print("📋 Listing recent task runs...")
    params = ListTaskRunsParams(limit=5)  # Get last 5 task runs

    task_runs = await render.workflows.list_task_runs(params)
    print(f"✓ Found {len(task_runs)} recent task runs")

    for i, task_run in enumerate(task_runs, 1):
        print(f"   {i}. {task_run.id} {task_run.status}")


if __name__ == "__main__":
    asyncio.run(main())
