"""Example: create a sandbox, copy files into it, run a command, then terminate.

Requires RENDER_API_KEY and RENDER_WORKSPACE_ID in the environment.
Run: uv run python example/sandbox/main.py
"""

import asyncio
import tempfile
from pathlib import Path

from render import RenderAsync
from render.experimental.sandbox import SandboxClient, SandboxExecOutput


async def run(sandboxes: SandboxClient, sandbox_id: str, command: str) -> None:
    async for event in sandboxes.exec(sandbox_id, command):
        if isinstance(event, SandboxExecOutput):
            print(event.data, end="")
        else:
            print(f"exit code: {event.exit_code}")


async def main() -> None:
    render = RenderAsync()
    sandboxes = render.experimental.sandboxes

    sandbox = await sandboxes.create()
    print(f"created {sandbox.id} ({sandbox.status})")
    try:
        await run(sandboxes, sandbox.id, "echo hello from render")

        with tempfile.TemporaryDirectory() as workspace:
            local = Path(workspace)
            (local / "greeting.txt").write_text("hello from copy_to\n")
            tree = local / "tree"
            (tree / "nested").mkdir(parents=True)
            (tree / "nested" / "data.txt").write_text("nested file\n")
            (tree / "link.txt").symlink_to("nested/data.txt")

            # A relative remote path resolves under the sandbox's home
            # directory, scp style; an absolute one addresses the filesystem.
            await sandboxes.copy_to(sandbox.id, local / "greeting.txt", "greeting.txt")
            print("copied greeting.txt")
            await sandboxes.copy_to(sandbox.id, tree, "tree")
            print("copied tree/")

        await run(sandboxes, sandbox.id, 'cat "$HOME/greeting.txt"')
        await run(sandboxes, sandbox.id, 'ls -lR "$HOME/tree"')
    finally:
        await sandboxes.terminate(sandbox.id)
        print("terminated")


if __name__ == "__main__":
    asyncio.run(main())
