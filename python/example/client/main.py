#!/usr/bin/env python3
"""
Render Python Client Example

This example demonstrates how to use the Render Python REST API client
to interact with Render's workflows API. It shows task execution,
monitoring, and error handling.

Setup:
1. Set your Render API token: export RENDER_API_KEY="your_token_here"
2. Replace "your-task-name" with an actual task from your Render dashboard
3. Run: uv run python example/client/main.py
"""

from typing import Any

from render_sdk import Render
from render_sdk.client import ListTaskRunsParams
from render_sdk.client.errors import RenderError, TaskRunError

# Create client (uses RENDER_API_KEY from environment)
render = Render()

# Replace with your workflow slug and task identifier
task_identifier = "my-workflow-slug/task-name"
# Input data can be specified as a list of positional arguments or a
# dictionary of named arguments
input_data: dict[str, Any] = {"arg1": 3}

# run_task() starts a task and waits for the result in one call
try:
    result = render.workflows.run_task(task_identifier, input_data)
    print(f"Task completed: {result.status}, results: {result.results}")
except TaskRunError as e:
    print(f"Task failed or was cancelled: {e}")
except RenderError as e:
    print(f"Error running task: {e}")

# start_task() starts a task without waiting for the result
task_run = render.workflows.start_task(task_identifier, input_data)
print(f"Task started with ID: {task_run.id}")

# Get task run details by ID
details = render.workflows.get_task_run(task_run.id)
print(f"Task run details: {details.id} status={details.status}")

# Cancel a task run
task_run2 = render.workflows.start_task(task_identifier, input_data)
render.workflows.cancel_task_run(task_run2.id)
print(f"Cancelled task run: {task_run2.id}")

# Stream task run events. This is useful when you want to monitor
# multiple task runs or handle events as they arrive.
task_run3 = render.workflows.start_task(task_identifier, input_data)
print("Streaming task run events...")
for event in render.workflows.task_run_events([task_run3.id]):
    print(f"  Event: {event.id} status={event.status}")
    if event.error:
        print(f"  Error: {event.error}")

# List recent task runs
params = ListTaskRunsParams(limit=5)
task_runs = render.workflows.list_task_runs(params)
print(f"Found {len(task_runs)} recent task runs")
for i, tr in enumerate(task_runs, 1):
    print(f"  {i}. {tr.id} {tr.status}")
