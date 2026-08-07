"""Example: create a sandbox, run a command, then terminate it.

Requires RENDER_API_KEY and RENDER_WORKSPACE_ID in the environment.
Run: uv run python example/sandbox/main.py
"""

import asyncio

from render_sdk import RenderAsync
from render_sdk.experimental.sandbox import SandboxExecOutput


async def main() -> None:
    render = RenderAsync()
    sandboxes = render.experimental.sandboxes

    sandbox = await sandboxes.create()
    print(f"created {sandbox.id} ({sandbox.status})")
    try:
        async for event in sandboxes.exec(sandbox.id, "echo hello from render"):
            if isinstance(event, SandboxExecOutput):
                print(event.data, end="")
            else:
                print(f"exit code: {event.exit_code}")
    finally:
        await sandboxes.terminate(sandbox.id)
        print("terminated")


if __name__ == "__main__":
    asyncio.run(main())
