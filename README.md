# Render SDK

Build on Render with official SDKs for Python and TypeScript.

[Python](#python) · [TypeScript](#typescript) · [Documentation](https://render.com/docs) · [Examples](#examples) · [Support](#documentation-and-support)

## Choose your SDK

| Language | Package | Requirements | Language guide |
| --- | --- | --- | --- |
| Python | [`render`](https://pypi.org/project/render/) | Python 3.10+ | [Python SDK](./python/README.md) |
| TypeScript | [`@renderinc/sdk`](https://www.npmjs.com/package/@renderinc/sdk) | Node.js 18+ | [TypeScript SDK](./typescript/README.md) |

## Supported products

| Product | What it enables | Status | Python | TypeScript |
| --- | --- | --- | :---: | :---: |
| [Workflows](https://render.com/docs/workflows) | Define tasks and manage durable, distributed task runs | Released | [✓](./python/render/client/workflows.py) | [✓](./typescript/src/workflows/client/client.ts) |
| Sandboxes | Run code in isolated environments | Early Access | [✓](./python/render/experimental/sandbox/client.py) | [✓](./typescript/src/experimental/sandboxes/index.ts) |
| Object Storage | Upload, retrieve, and list objects | Early Access | [✓](./python/render/experimental/object/client.py) | [✓](./typescript/src/experimental/object/client.ts) |

## Install and authenticate

Create a [Render API key](https://render.com/docs/api#1-create-an-api-key), then set it in your environment:

```bash
export RENDER_API_KEY=rnd_...
```

The SDK automatically reads `RENDER_API_KEY`. You can also pass a token directly when constructing a client.

### Python

Install the SDK from PyPI:

```bash
pip install render
```

Initialize a client:

```python
from render import Render

render = Render()
```

Using uv or Poetry?

<details>
<summary>Alternative installation commands</summary>

```bash
uv add render
# or
poetry add render
```

</details>

Continue to the [Python SDK guide](./python/README.md).

### TypeScript

Install the SDK from npm:

```bash
npm install @renderinc/sdk
```

Initialize a client:

```typescript
import { Render } from "@renderinc/sdk";

const render = new Render();
```

Using pnpm, Yarn, or Bun?

<details>
<summary>Alternative installation commands</summary>

```bash
pnpm add @renderinc/sdk
# or
yarn add @renderinc/sdk
# or
bun add @renderinc/sdk
```

</details>

Continue to the [TypeScript SDK guide](./typescript/README.md).

## Explore SDK features

### Workflows

Render Workflows orchestrates long-running, distributed tasks. Define tasks as Python or TypeScript functions, configure retries and compute resources, and trigger task runs from your applications.

The fastest way to create a starter project is with the Render CLI:

```bash
render workflows init
```

- [Create your first Workflow](https://render.com/docs/workflows-tutorial)
- [Python SDK reference](https://render.com/docs/workflows-sdk-python)
- [TypeScript SDK reference](https://render.com/docs/workflows-sdk-typescript)
- [Local development](https://render.com/docs/workflows-local-development)

### Sandboxes (Early Access)

Use the experimental SDK clients to create and interact with isolated execution environments:

- [Python Sandbox client](./python/render/experimental/sandbox/client.py)
- [TypeScript Sandbox client](./typescript/src/experimental/sandboxes/index.ts)

### Object Storage (Early Access)

Use the experimental SDK clients to upload, retrieve, and list objects:

- [Python Object Storage client](./python/render/experimental/object/client.py)
- [TypeScript Object Storage client](./typescript/src/experimental/object/client.ts)

## Examples

- [Python examples](./python/example)
- [TypeScript examples](./typescript/examples)
- [Your first Workflow](https://render.com/docs/workflows-tutorial)

## Documentation and support

- [Render documentation](https://render.com/docs)
- [Render API reference](https://api-docs.render.com)
- [GitHub issues](https://github.com/render-oss/sdk/issues)
- [SDK releases](https://github.com/render-oss/sdk/releases)

## Contributing

Contributions are welcome. For language-specific development commands, see:

- [Python development setup](./python/README.md#development)
- [TypeScript development setup](./typescript/README.md#development)

Please open an issue before proposing a substantial API or architectural change.
