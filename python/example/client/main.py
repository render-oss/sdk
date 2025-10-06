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
import os
from typing import Any

from render_sdk.client import Client, ListTaskRunsParams
from render_sdk.client.errors import RenderError, TaskRunError


async def main():
    """Demonstrate async workflow operations."""
    # Get API token from environment
    token = os.getenv("RENDER_API_KEY")
    if not token:
        print("⚠️  RENDER_API_KEY environment variable not set")
        return
    # Create client
    client = Client(token)

    # Example task data - replace with your actual task
    task_identifier = "package-renaming-slug/square"  # Replace with your task name
    input_data: list[Any] = [3]

    # Run the task
    try:
        task_run = await client.workflows.run_task(task_identifier, input_data)
        print(f"Task started with ID: {task_run.id}")
    except Exception as e:
        print(f"Error running task: {e}")
        raise

    # Wait for completion using SSE streaming (Pythonic way!)
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

    # List recent task runs
    print("📋 Listing recent task runs...")
    params = ListTaskRunsParams(limit=5)  # Get last 5 task runs

    task_runs = await client.workflows.list_task_runs(params)
    print(f"✓ Found {len(task_runs)} recent task runs")

    for i, task_run in enumerate(task_runs, 1):
        print(f"   {i}. {task_run.id} {task_run.status}")


if __name__ == "__main__":
    asyncio.run(main())
