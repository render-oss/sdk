# Internal Examples

These are example tasks intended for internal testing use cases. These should not be published externally.

Both examples resolve the SDK from this repo rather than from a package
registry, so a workflow built from a branch runs that branch's SDK code:

- [`python/`](python) — depends on `../../python` via a `[tool.uv.sources]` editable path entry.
- [`ts/`](ts) — depends on `../../typescript` via a `file:` dependency.

## Using these examples

1. Create a new workflow in the dashboard.
1. For `Source Code`, select the `renderinc/sdk` repository.
1. For `Language`, select `Python` or `Node` depending on which example you want.
1. For `Branch`, select `main` unless you are testing a specific branch
1. For `Auto-Deploy`, select `Off` if you don't need this workflow to update automatically
1. For `Region`, select the region you want to run the workflow in.
    - If you want to run the workflow in a specific cluster, use the workspace email override: https://slab.render.com/posts/how-to-test-in-a-specific-cluster-9cjlhb7p#h82dc-using-workspace-email-override
1. For `Root Directory`, `Build Command`, and `Start Command`, use the values for your language below.

Both examples reach outside their root directory to pick up the SDK source, so
the whole repo has to be checked out — don't limit the build to a subdirectory.

### Python

| Setting | Value |
| --- | --- |
| `Root Directory` | `internal-examples/python` |
| `Build Command` | `uv sync` |
| `Start Command` | `uv run main.py` |

`uv` is already on the build image, so there is nothing to install first.

### TypeScript

| Setting | Value |
| --- | --- |
| `Root Directory` | `internal-examples/ts` |
| `Build Command` | `npm install` |
| `Start Command` | `npm start` |

`npm install` runs a `preinstall` hook that installs and builds the SDK in
`typescript/`, since the `file:` dependency resolves to its compiled `dist/`.

## Client scripts

Each language directory has a `client/` subdirectory holding scripts that drive
the REST API against an already deployed workflow, rather than tasks to be
deployed. They run from their language's project, so they pick up the same
checked-out SDK the tasks beside them do. They need a workflow running one of
the examples above, and a task to call.

### Idempotency key check

Submits one task three times under two idempotency keys and asserts that the
shared key yields a single run while the other yields a second, then replays the
shared key after both finish to confirm a claim outlives the run it created.
Exits non-zero on any failure.

```bash
export RENDER_API_KEY="your_token_here"
export RENDER_TASK_SLUG="my-workflow-slug/task-name"
export RENDER_TASK_INPUT='[4]'   # optional, defaults to [4]

cd python && uv run client/idempotency.py
cd ts && npm install && npm run idempotency
```

Against a local dev server, point the SDK at it instead and the API key becomes
optional:

```bash
export RENDER_LOCAL_DEV_URL="https://api.localhost.render.com:8443"
```
