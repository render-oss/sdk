# sdk

The official SDK for Render

> [!WARNING]
> **Early Access:** This SDK is in early access and subject to breaking changes without notice.

SDK support is provided for the following languages:

Language   | README                                 | Package
-----------|----------------------------------------|-----------------
TypeScript | [./typescript](./typescript/README.md) | `@renderinc/sdk`
Python     | [./python](./python/README.md)         | `render_sdk`

# Quickstart

To get started you'll need a couple things:
- [A Render API Key](https://render.com/docs/api#1-create-an-api-key)
- The SDK for your language

## Python

To start, get the latest SDK from pypi
```bash
pip install render_sdk
# or
uv add render_sdk
# or
poetry add render_sdk
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
```

Then initialize a SDK client with your API key
```typescript
import { Render } from "@renderinc/sdk";

const render = new Render({token: "rnd_..."})
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
│   └── render_sdk
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

For Python we support a minimum of `3.10`, and use poetry to manage our dependecies - [see more in our pyproject.toml](https://github.com/renderinc/sdk/blob/main/python/pyproject.toml)

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
