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
