#!/usr/bin/env python3
"""
Example: Using the REST API client to run tasks

run_task() starts a task and waits for its result in one call.
start_task() starts a task and returns a TaskRunResult, letting you
decide when (or whether) to await the result via .get().

Setup:
1. Set your Render API token: export RENDER_API_KEY="your_token_here"
2. Replace "my-workflow/square" with an actual task from your Render dashboard
3. Run: poetry run python example/client/main.py
"""

import asyncio

from render_sdk import Render
from render_sdk.client import ListTaskRunsParams
from render_sdk.client.errors import RenderError


async def main():
    render = Render()

    try:
        # Run a task and wait for its result in one call.
        result = await render.workflows.run_task("my-workflow/square", [4])
        print(f"Task completed: {result.status} {result.results}")

        # Start a task and grab its ID for later use (e.g. polling, logging).
        # Results aren't streamed until you call .get().
        run = await render.workflows.start_task("my-workflow/square", [7])
        print(f"Started task run: {run.task_run_id}")
        result2 = await run.get()
        print(f"Task completed: {result2.status} {result2.results}")

        # Fire-and-forget: start a task without waiting for the result.
        await render.workflows.start_task("my-workflow/square", [10])

        # Cancel a task run by ID
        run2 = await render.workflows.start_task("my-workflow/square", [99])
        await render.workflows.cancel_task_run(run2.task_run_id)
        print(f"Cancelled task run: {run2.task_run_id}")

        # List recent task runs
        task_runs = await render.workflows.list_task_runs(ListTaskRunsParams(limit=5))
        print(f"\nFound {len(task_runs)} task runs:")
        for task_run in task_runs:
            print(f"  - {task_run.id}: {task_run.status}")

        # Get task run details by ID
        details = await render.workflows.get_task_run(result.id)
        print(f"\nTask run details: {details}")

        # Stream task run events as an async iterable.
        # task_run_events() yields a TaskRunDetails for each terminal event
        # (completed or failed) received on the stream.
        # The stream stays open until you break or abort.
        run3 = await render.workflows.start_task("my-workflow/square", [3])
        run4 = await render.workflows.start_task("my-workflow/square", [6])
        pending = {run3.task_run_id, run4.task_run_id}
        async for event in render.workflows.task_run_events(list(pending)):
            print(f"Event: {event.status} {event.id} {event.results}")
            pending.discard(event.id)
            if not pending:
                break
    except RenderError as e:
        print(f"Error: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
