"""Run a real workflow process against HTTP failures on a Unix socket.

Only the retry delay is shortened. The client, retry count, workflow runner,
and process exit are real; renderd and its persistence are represented here by
a small HTTP fixture.
"""

from __future__ import annotations

import asyncio
import base64
import json
import os
import sys
import tempfile
from pathlib import Path

import pytest
from aiohttp import web

_WORKFLOW = """
import os
from render.workflows.app import Workflows
import render.workflows.client as client

# Preserve all 25 attempts without spending five minutes in backoff.
client._UDS_INITIAL_DELAY_S = 0
app = Workflows()

def failing_step():
    print("failing step executed", flush=True)
    raise ValueError("dependency unavailable")

def fallback():
    print("fallback executed", flush=True)
    return "recovered"

@app.flow
def wf(ctx):
    try:
        return ctx.step("failing_step", failing_step)
    except Exception:
        if os.environ["CATCH_STEP_ERROR"] != "1":
            raise
        return ctx.step("fallback", fallback)

app.start()
"""


@pytest.fixture
def run_workflow():
    async def run(*, completion_failures: int, catch: bool, reject_callback=False):
        requests: list[tuple[str, dict]] = []
        completion_acknowledged = False

        async def handle(request: web.Request) -> web.Response:
            nonlocal completion_acknowledged
            if request.path == "/input":
                return web.json_response(
                    {
                        "task_name": "wf",
                        "input": "W10=",
                        "task_run_id": "trn-test",
                        "is_workflow": True,
                        "attempt": 0,
                    }
                )
            body = await request.json()
            requests.append((request.path, body))
            if request.path == "/step-inline/complete" and body["key"]["seq"] == 0:
                completions = sum(path == request.path for path, _ in requests)
                if completions <= completion_failures:
                    return web.json_response(
                        {"message": "history unavailable"}, status=500
                    )
                completion_acknowledged = True
            if request.path == "/step-inline/start" and body["step_key"]["seq"] == 1:
                # A fallback must never run while the failed step is unrecorded.
                assert completion_acknowledged
            if request.path == "/callback" and reject_callback:
                return web.json_response(
                    {"message": "callback unavailable"}, status=500
                )
            return web.json_response({"applied": True})

        app = web.Application()
        app.router.add_route("*", "/{tail:.*}", handle)
        runner = web.AppRunner(app)
        await runner.setup()
        # Keep the socket path below the macOS Unix socket length limit.
        with tempfile.TemporaryDirectory(prefix="rds-") as directory:
            socket_path = str(Path(directory) / "s")
            process = None
            try:
                await web.UnixSite(runner, socket_path).start()
                process = await asyncio.create_subprocess_exec(
                    sys.executable,
                    "-c",
                    _WORKFLOW,
                    env={
                        "PATH": os.environ.get("PATH", ""),
                        "PYTHONPATH": str(Path(__file__).resolve().parents[3]),
                        "RENDER_SDK_MODE": "run",
                        "RENDER_SDK_SOCKET_PATH": socket_path,
                        "CATCH_STEP_ERROR": "1" if catch else "0",
                    },
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(), timeout=10
                )
                return process.returncode, stdout.decode(), stderr.decode(), requests
            finally:
                if process is not None and process.returncode is None:
                    process.kill()
                    await process.communicate()
                await runner.cleanup()

    return run


@pytest.mark.asyncio
@pytest.mark.parametrize("catch", [False, True])
async def test_failed_step_waits_for_recording_before_reporting_its_outcome(
    run_workflow, catch
):
    code, stdout, stderr, requests = await run_workflow(
        completion_failures=2, catch=catch
    )
    completions = [
        body
        for path, body in requests
        if path == "/step-inline/complete" and body["key"]["seq"] == 0
    ]
    assert len(completions) == 3
    assert completions == [completions[0]] * 3
    assert stdout.count("failing step executed") == 1
    callbacks = [body for path, body in requests if path == "/callback"]
    assert len(callbacks) == 1
    if catch:
        assert code == 0, stderr
        assert stdout.count("fallback executed") == 1
        assert json.loads(base64.b64decode(callbacks[0]["complete"]["output"])) == [
            "recovered"
        ]
    else:
        assert code == 1, stderr
        assert "fallback executed" not in stdout
        assert "dependency unavailable" in callbacks[0]["error"]["details"]
        assert "reason" not in callbacks[0]["error"]


@pytest.mark.asyncio
@pytest.mark.parametrize("reject_callback", [False, True])
async def test_exhausted_recording_retries_end_the_process_even_if_callback_fails(
    run_workflow, reject_callback
):
    code, stdout, stderr, requests = await run_workflow(
        completion_failures=25, catch=True, reject_callback=reject_callback
    )
    assert code == 1, stderr
    assert stdout.count("failing step executed") == 1
    assert "fallback executed" not in stdout
    completions = [body for path, body in requests if path == "/step-inline/complete"]
    assert len(completions) == 25
    assert completions == [completions[0]] * 25
    callbacks = [body for path, body in requests if path == "/callback"]
    assert len(callbacks) == (25 if reject_callback else 1)
    assert all(body["error"]["reason"] == "system_error" for body in callbacks)
    assert "history unavailable" in callbacks[0]["error"]["details"]
