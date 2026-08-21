# sdk

The official SDK for Render

> [!WARNING]
> **Early Access:** This SDK is in early access and subject to breaking changes without notice.

SDK support is provided for the following languages

| Language   | README                                 | Package          |
| ---------- | -------------------------------------- | ---------------- |
| TypeScript | [./typescript](./typescript/README.md) | `@renderinc/sdk` |
| Python     | [./python](./python/README.md)         | `render`         |

With the following features

| Feature        | Python                                                                  | TypeScript                                                               |
| -------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| REST API       | ✔️                                                                      | ✔️                                                                       |
| Workflows      | [⚠️ Early Access client](./python/render/client/workflows.py)           | [⚠️ Early Access client](./typescript/src/workflows/client/client.ts)    |
| Object Storage | [⚠️ Early Access client](./python/render/experimental/object/client.py) | [⚠️ Early Access client](./typescript/src/experimental/object/client.ts) |

# Quickstart

To get started you'll need a couple things:

- [A Render API Key](https://render.com/docs/api#1-create-an-api-key)
- The SDK for your language

## Python

To start, get the latest SDK from pypi

```bash
pip install render
# or
uv add render
# or
poetry add render
```

Then initialize a SDK client with your API key

```python
from render import Render

render = Render(token="rnd_...")
```

You may also provide a `RENDER_API_KEY` environment variable instead of providing the key to the constructor.

For more detail see the [Python SDK README](./python/README.md)

## TypeScript

To start get the latest SDK from npm

```bash
npm i @renderinc/sdk
# or
pnpm add @renderinc/sdk
# or
yarn add @renderinc/sdk
# or
bun add @renderinc/sdk
```

Then initialize a SDK client with your API key

```typescript
import { Render } from "@renderinc/sdk";

const render = new Render({ token: "rnd_..." });
```

You may also provide a `RENDER_API_KEY` environment variable instead of providing the key to the constructor.

For more detail see the [TypeScript SDK README](./typescript/README.md)

# Contributing

## Development

### Folder structure

```
.
├── python/
│   ├── example
│   └── render
├── typescript/
│   ├── examples
│   └── src
├── openapi/
│   └── openapi.yaml # Local API Schema for Workflows
└── go/
    ├── example
    └── pkg
```

### Setup

For Python we support a minimum of `3.10`, and use [uv](https://docs.astral.sh/uv/) to manage our dependencies - [see more in our pyproject.toml](https://github.com/renderinc/sdk/blob/main/python/pyproject.toml)

For TypeScript we support a minimum node version of `18.0.0` and use `npm` to manage our dependecies - [see more in our package.json](https://github.com/renderinc/sdk/blob/main/typescript/package.json)

To install pre-commit hooks, run:

```bash
pre-commit install
pre-commit autoupdate
```

### API Documentation

To view workflow API documentation from the OpenAPI spec:

```bash
npx @redocly/cli preview-docs openapi/openapi.yaml
```
