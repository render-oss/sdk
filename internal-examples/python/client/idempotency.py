#!/usr/bin/env python3
"""
Render Python Client — idempotency key check

Submits the same task three times: twice under one idempotency key and once
under a different one. Two submissions sharing a key must resolve to a single
task run; a different key must start a new one.

Setup:
1. export RENDER_API_KEY="your_token_here"
2. export RENDER_TASK_SLUG="my-workflow-slug/task-name"
3. Optionally export RENDER_TASK_INPUT='[4]' (defaults to [4])
4. Run: uv run client/idempotency.py

To run against a dev server also set:
  export RENDER_LOCAL_DEV_URL="https://api.localhost.render.com:8443"
"""

import json
import os
import sys
import time
import uuid

from render import Render
from render.client.errors import RenderError
from render.client.types import TaskRunStatusValues

TERMINAL = (
    TaskRunStatusValues.COMPLETED,
    TaskRunStatusValues.SUCCEEDED,
    TaskRunStatusValues.FAILED,
    TaskRunStatusValues.CANCELED,
)


def wait_for_terminal(render: Render, task_run_id: str, timeout_s: float = 180.0):
    """Poll a task run until it reaches a terminal state."""
    deadline = time.monotonic() + timeout_s
    while True:
        details = render.workflows.get_task_run(task_run_id)
        if details.status.value in TERMINAL:
            return details
        if time.monotonic() > deadline:
            raise TimeoutError(f"{task_run_id} still {details.status.value}")
        time.sleep(1.0)


def main() -> int:
    task_slug = os.environ.get("RENDER_TASK_SLUG")
    if not task_slug:
        print("RENDER_TASK_SLUG is required, e.g. my-workflow/square", file=sys.stderr)
        return 2
    input_data = json.loads(os.environ.get("RENDER_TASK_INPUT", "[4]"))

    render = Render()
    print(f"base url:   {render._client.base_url}")

    # Fresh keys every run. A key stays claimed for 24 hours, so reusing one
    # across runs would resolve to the previous run rather than testing anything.
    shared_key = f"sdk-idempotency-check-{uuid.uuid4()}"
    other_key = f"sdk-idempotency-check-{uuid.uuid4()}"
    print(f"task:       {task_slug}")
    print(f"shared key: {shared_key}")
    print(f"other key:  {other_key}\n")

    first = render.workflows.start_task(
        task_slug, input_data, idempotency_key=shared_key
    )
    print(f"1. submitted with shared key -> {first.id}")

    repeat = render.workflows.start_task(
        task_slug, input_data, idempotency_key=shared_key
    )
    print(f"2. resubmitted same key      -> {repeat.id}")

    different = render.workflows.start_task(
        task_slug, input_data, idempotency_key=other_key
    )
    print(f"3. submitted with other key  -> {different.id}")

    failures = []
    if repeat.id != first.id:
        failures.append(
            f"reusing a key started a second run ({first.id} then {repeat.id})"
        )
    if different.id == first.id:
        failures.append(f"a different key resolved to the first run ({first.id})")

    print("\nwaiting for both runs to finish...")
    first_details = wait_for_terminal(render, first.id)
    different_details = wait_for_terminal(render, different.id)
    print(f"   {first.id}: {first_details.status.value} {first_details.results}")
    print(
        f"   {different.id}: {different_details.status.value} {different_details.results}"
    )

    # A claim outlives the run it created, so replaying the key after the run
    # finishes returns that finished run rather than starting a fresh one.
    replay = render.workflows.start_task(
        task_slug, input_data, idempotency_key=shared_key
    )
    print(f"\n4. replayed shared key after completion -> {replay.id}")
    if replay.id != first.id:
        failures.append(
            f"replaying a key after completion started a new run ({replay.id})"
        )

    print()
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1
    print("PASS: one key produced one run, a second key produced another")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except RenderError as exc:
        # Reaching the wrong server, or none at all, is the common way to run
        # this: report it as that rather than as a failed assertion.
        sys.stdout.flush()
        print(f"\nERROR: {exc}", file=sys.stderr)
        print(
            "Check the base url above. For a local dev server set "
            "RENDER_LOCAL_DEV_URL.",
            file=sys.stderr,
        )
        sys.exit(3)
