# Render SDK for TypeScript

The official TypeScript SDK for Render. Define Workflow tasks and flows, manage task runs and flow runs, and access experimental platform features like object storage.

## Features

- **REST API Client**: Run, monitor, and manage task runs and flow runs
- **Task Definition SDK**: Define and register tasks with decorators
- **Durable Flows**: Flows that replay after a crash, with steps that retry in-process
- **Server-Sent Events**: Real-time streaming of task run events
- **Async/Await Support**: Modern Promise-based API
- **TypeScript First**: Full type safety and IntelliSense support
- **Retry Logic**: Configurable retry behavior for tasks
- **Subtask Execution**: Execute tasks from within other tasks
- **Object Storage**: Experimental object storage API with upload, download, and list
- **Key Value**: Experimental Render Key Value client with auto-provisioning and configuration sync

## Installation

```bash
npm install @renderinc/sdk
```

Or with yarn:

```bash
yarn add @renderinc/sdk
```

Or with pnpm:

```bash
pnpm add @renderinc/sdk
```

Or with Bun:

```bash
bun add @renderinc/sdk
```

## Quick Start

### REST API Client

Use the Render SDK to run tasks and monitor their execution:

```typescript
import { Render } from "@renderinc/sdk";

// Create a Render SDK instance (uses RENDER_API_KEY from environment)
const render = new Render();

// Run a task and wait for completion
const result = await render.workflows.runTask("my-workflow/my-task", [
  42,
  "hello",
]);
console.log("Status:", result.status);
console.log("Results:", result.results);

// Or start a task and decide when to await the result
const run = await render.workflows.startTask("my-workflow/my-task", [
  42,
  "hello",
]);
console.log("Task run ID:", run.taskRunId);
const details = await run.get();

// List recent task runs
const taskRuns = await render.workflows.listTaskRuns({ limit: 10 });
```

Alternatively, you can create a workflows client directly:

```typescript
import { createWorkflowsClient } from "@renderinc/sdk/workflows";

const client = createWorkflowsClient();
const result = await client.runTask("my-workflow/my-task", [42, "hello"]);
```

### Task Definition

Define tasks that can be executed by the workflow system. Every task takes a
`TaskContext` as its first parameter, followed by its inputs:

```typescript
import { task, type TaskContext } from "@renderinc/sdk/workflows";

// Simple task
const square = task(
  { name: "square" },
  function square(ctx: TaskContext, a: number): number {
    return a * a;
  },
);

// Async task that reaches other tasks through its context
task(
  { name: "addSquares" },
  async function addSquares(
    ctx: TaskContext,
    a: number,
    b: number,
  ): Promise<number> {
    // .run runs the task on its own compute
    const result1 = await ctx.run(square, a);
    const result2 = await ctx.run(square, b);
    return result1 + result2;
  },
);

// Task with custom options
task(
  {
    name: "retryableTask",
    retry: {
      maxRetries: 3,
      waitDurationMs: 1000,
      backoffScaling: 1.5,
    },
    timeoutSeconds: 86400, // 24h
    plan: "starter",
  },
  async function retryableTask(
    ctx: TaskContext,
    input: string,
  ): Promise<string> {
    // Task implementation
    return input.toUpperCase();
  },
);

// The task server starts automatically when running in a workflow environment
// (when RENDER_SDK_SOCKET_PATH is set). No need to call startTaskServer() explicitly.
//
// To disable auto-start, set RENDER_SDK_AUTO_START=false in your environment.
```

Run several tasks at once by awaiting them together:

```typescript
task({ name: "sumSquares" }, async (ctx: TaskContext, values: number[]) => {
  const squares = await Promise.all(values.map((v) => ctx.run(square, v)));
  return squares.reduce((a, b) => a + b, 0);
});
```

#### The task context

| Method                   | Description                                                 |
| ------------------------ | ----------------------------------------------------------- |
| `ctx.run(task, ...args)` | Runs `task` on its own compute and resolves with its result |

The context exposes read-only execution metadata at `ctx.metadata.taskRunId`,
`ctx.metadata.rootTaskRunId`, and `ctx.metadata.parentTaskRunId`. The SDK reads
it from the initial input response and keeps it for that execution. Accessing
it does not make a network request.

For a root run, `ctx.metadata.rootTaskRunId` equals `ctx.metadata.taskRunId` and
`ctx.metadata.parentTaskRunId` is `undefined`.

### Durable Flows

A flow is a task that resumes after a crash. Register one with `flow()`.
Each `ctx` call in a flow is a durable **step**, and the SDK records its
result. After a crash, the flow reruns from the top, and `ctx` calls for
finished steps return the recorded results instead of running again.

```typescript
import { flow, StepError } from "@renderinc/sdk/workflows";

// A plain function. From a flow, it runs inline, in the flow's process.
function chargeCard(orderId: string, total: number) {
  return payments.charge(orderId, total);
}

flow({ name: "fulfillOrder" }, async (ctx, order: Order) => {
  const charge = await ctx.step("charge", chargeCard, [order.id, order.total], {
    retry: { maxRetries: 3, waitDurationMs: 1000 },
  });
  const invoice = await ctx.step("invoice", createInvoice, [order.id]);
  const receiptId = await ctx.step("receiptId", () => crypto.randomUUID());

  try {
    await ctx.step("send", sendReceipt, [order.email, invoice.id, receiptId]);
  } catch (error) {
    if (!(error instanceof StepError)) throw error;
    await ctx.step("notify", notifySupport, [order.id]);
  }
  return { charge: charge.id, invoice: invoice.id };
});
```

| Call                                    | Description                                                          |
| --------------------------------------- | -------------------------------------------------------------------- |
| `ctx.step(name, fn, [args], { retry })` | Runs a plain function inline as the step `name`, retrying in-process |
| `ctx.step(name, fn, { retry })`         | Runs a zero-argument function inline as the step `name`              |

Rules for flow code:
- **Be deterministic.** A replay must make the same `ctx` calls in the same
  order with the same inputs. Put I/O, clocks, random values and anything else
  non-deterministic inside a step.
- **Run one step at a time.** Await each `ctx` call before making the next.
  `Promise.all` over `ctx` calls is not supported yet.
- **Steps make no `ctx` calls.** A step's arguments and result are recorded as
  JSON, so a `Date` comes back as a string.
- **Set retries on steps, not flows.** Flows take no retry policy: they replay
  after infrastructure failures instead.
- If a step fails for good, `ctx.step` throws a `StepError`, which you can
  catch; a replay rethrows the same error.
- **Don't pass secrets through step inputs or outputs.** Render stores them.
- `ctx.invoke` and `ctx.sleep` are not supported yet, so flows can't run
  registered tasks. Call the task's plain function with `ctx.step` instead.

For limits, supported regions and how flow runs recover, see the
[Workflows documentation](https://render.com/docs/workflows). To start and
inspect flow runs, see [Flow Client Methods](#flow-client-methods).

### Run the Local Task Server

For local development, use the Render CLI:

```bash
render workflows dev -- <start command>
```

For example:

```bash
render workflows dev -- npm start
```

To interact with tasks registered to the local task server, run CLI commands with the `--local` flag in another terminal. For example:

```bash
render workflows tasks start <task name> --local
```

## API Reference

### Render SDK

#### `new Render(options?)`

Creates a new Render SDK instance with access to all Render products.

**Options:**
- `token?: string` - API token (defaults to `RENDER_API_KEY` env var)
- `baseUrl?: string` - Base URL (defaults to `https://api.render.com`)
- `useLocalDev?: boolean` - Use local development mode
- `localDevUrl?: string` - Local development URL
- `ownerId?: string` - Default owner ID for object storage (falls back to `RENDER_WORKSPACE_ID` env var)
- `region?: string` - Default region for object storage (falls back to `RENDER_REGION` env var)

**Properties:**
- `workflows` - WorkflowsClient instance for managing workflow tasks
- `experimental` - ExperimentalClient instance for object storage and other experimental APIs

**Example:**

```typescript
import { Render } from "@renderinc/sdk";

const render = new Render({
  token: "your-api-token",
  baseUrl: "https://api.render.com",
});

// Access workflows client
const result = await render.workflows.runTask("my-workflow/task", [42]);
```

### Workflows Client API

The workflows client is accessible via `render.workflows` or can be created directly using `createWorkflowsClient`:

```typescript
import { createWorkflowsClient } from "@renderinc/sdk/workflows";

const client = createWorkflowsClient({
  token: "your-api-token",
  baseUrl: "https://api.render.com",
});
```

### Workflows Client Methods

#### `render.workflows.runTask(taskSlug, inputData, signalOrOptions?)`

Runs a task and waits for completion.

**Parameters:**
- `taskSlug: string` - Task slug in format "workflow-slug/task-name"
- `inputData: any[]` - Input data as array of parameters
- `signalOrOptions?: AbortSignal | StartTaskOptions` - An abort signal, or an options object with `signal` and/or `idempotencyKey`

**Returns:** `Promise<TaskRunDetails>`

**Example:**

```typescript
const render = new Render();
const result = await render.workflows.runTask("my-workflow/square", [5]);
console.log("Results:", result.results);
```

#### `render.workflows.startTask(taskSlug, inputData, signalOrOptions?)`

Starts a task run and returns a `TaskRunResult`. Results are not streamed until you call `.get()` on the returned result. Use this when you need the task run ID, want to defer awaiting, or want fire-and-forget.

**Parameters:**
- `taskSlug: string` - Task slug in format "workflow-slug/task-name"
- `inputData: any[]` - Input data as array of parameters
- `signalOrOptions?: AbortSignal | StartTaskOptions` - An abort signal, or an options object with `signal` and/or `idempotencyKey`

**Returns:** `Promise<TaskRunResult>`

**Example:**

```typescript
const render = new Render();

// Start a task and grab its ID
const run = await render.workflows.startTask("my-workflow/square", [5]);
console.log("Task run ID:", run.taskRunId);

// Await the result when you're ready
const result = await run.get();
console.log("Results:", result.results);
```

##### Idempotency keys

Pass an `idempotencyKey` to make starting a run safe to retry. Repeating a call with the same key within 24 hours returns the run the first call started instead of starting another one, so a client that retries after a timeout does not run the task twice. Keys are scoped to a workflow.

```typescript
const run = await render.workflows.startTask("my-workflow/charge", [orderId], {
  idempotencyKey: `charge-${orderId}`,
});
```

#### `render.workflows.taskRunEvents(taskRunIds, signal?)`

Streams task run events as an async iterable. Yields a `TaskRunDetails` for each terminal event (completed, failed, or canceled) received on the stream.

**Parameters:**
- `taskRunIds: string[]` - One or more task run IDs to subscribe to
- `signal?: AbortSignal` - Optional abort signal for cancellation

**Returns:** `AsyncGenerator<TaskRunDetails>`

**Example:**

```typescript
const render = new Render();

const run1 = await render.workflows.startTask("my-workflow/square", [3]);
const run2 = await render.workflows.startTask("my-workflow/square", [6]);

// The stream stays open until you break or abort.
const pending = new Set([run1.taskRunId, run2.taskRunId]);
for await (const event of render.workflows.taskRunEvents([...pending])) {
  console.log("Event:", event.status, event.id, event.results);
  pending.delete(event.id);
  if (pending.size === 0) break;
}
```

#### `render.workflows.getTaskRun(taskRunId)`

Gets task run details by ID.

**Parameters:**
- `taskRunId: string` - Task run ID

**Returns:** `Promise<TaskRunDetails>`

**Example:**

```typescript
const render = new Render();
const details = await render.workflows.getTaskRun("task-run-id");
```

#### `render.workflows.cancelTaskRun(taskRunId)`

Cancels a running task.

**Parameters:**
- `taskRunId: string` - Task run ID to cancel

**Returns:** `Promise<void>`

**Example:**

```typescript
const render = new Render();
const run = await render.workflows.startTask("my-workflow/square", [5]);
await render.workflows.cancelTaskRun(run.taskRunId);
```

#### `render.workflows.listTaskRuns(params)`

Lists task runs with optional filters.

**Parameters:**
- `params.limit?: number` - Maximum number of results
- `params.cursor?: string` - Pagination cursor
- `params.ownerId?: string[]` - Filter by owner IDs

**Returns:** `Promise<TaskRun[]>`

**Example:**

```typescript
const render = new Render();
const taskRuns = await render.workflows.listTaskRuns({ limit: 10 });
```

### Flow Client Methods

The client starts, inspects, lists and cancels flow runs the same way it does task runs. A flow slug has the format `"workflow-slug/flow-name"`. Append `:version` to run a specific version; otherwise the latest version runs.

#### `render.workflows.startFlow(flowSlug, inputData, signalOrOptions?)`

Starts a flow run and returns it without waiting for it to finish. Use `getFlowRun()` with the returned ID to check its status.

**Parameters:**
- `flowSlug: string` - Flow slug in format "workflow-slug/flow-name"
- `inputData: any[] | Record<string, any>` - Input data as an array of positional arguments or an object of named parameters
- `signalOrOptions?: AbortSignal | StartFlowOptions` - An abort signal, or an options object with `signal` and/or `idempotencyKey`

**Returns:** `Promise<FlowRun>`

**Example:**

```typescript
const render = new Render();
const flowRun = await render.workflows.startFlow(
  "my-workflow/fulfillOrder",
  [order],
  { idempotencyKey: `fulfill-${order.id}` },
);
console.log("Flow run ID:", flowRun.id);
```

#### `render.workflows.runFlow(flowSlug, inputData, signalOrOptions?)`

Starts a flow run and waits for it to finish. Resolves with the run's details whether it succeeded, failed or was canceled, so check `status`. The wait has no deadline; pass a signal to stop it.

**Parameters:** Same as `startFlow`.

**Returns:** `Promise<FlowRunDetails>`

**Example:**

```typescript
import { Render } from "@renderinc/sdk";
import { FlowRunStatus } from "@renderinc/sdk/workflows";

const render = new Render();
const details = await render.workflows.runFlow("my-workflow/fulfillOrder", [
  order,
]);
if (details.status === FlowRunStatus.SUCCEEDED) {
  console.log("Results:", details.results);
} else {
  console.error("Flow run ended:", details.status, details.error);
}
```

#### `render.workflows.getFlowRun(flowRunId, signal?)`

Gets flow run details by ID, including its `results`, `error` and `attempts`.

**Returns:** `Promise<FlowRunDetails>`

#### `render.workflows.cancelFlowRun(flowRunId, signal?)`

Cancels a flow run.

**Returns:** `Promise<void>`

#### `render.workflows.listFlowRuns(params?, signal?)`

Lists flow runs with optional filters.

**Parameters:**
- `params.limit?: number` - Maximum number of results
- `params.cursor?: string` - Pagination cursor
- `params.flowSlug?: string[]` - Filter by flow slugs
- `params.flowId?: string[]` - Filter by flow IDs
- `params.status?: FlowRunStatus[]` - Filter by statuses
- `params.ownerId?: string[]` - Filter by owner IDs
- `params.workflowId?: string[]` - Filter by workflow IDs
- `params.workflowVersionId?: string[]` - Filter by workflow version IDs

**Returns:** `Promise<FlowRunWithCursor[]>`

**Example:**

```typescript
import { FlowRunStatus } from "@renderinc/sdk/workflows";

const render = new Render();
const failedRuns = await render.workflows.listFlowRuns({
  status: [FlowRunStatus.FAILED],
  limit: 10,
});
```

### Task API

#### `task(options, func)`

Registers a function as a task.

**Parameters:**
- `options: RegisterTaskOptions` - Task configuration
  - `name: string` - Task name (required)
  - `retry?: RetryOptions` - Optional retry configuration
    - `maxRetries: number` - Maximum number of retries
    - `waitDurationMs: number` - Wait duration between retries in milliseconds
    - `backoffScaling?: number` - Backoff multiplier (default: 1.5)
  - `timeoutSeconds?: number` - Maximum execution time in seconds
  - `plan?: string` - Resource plan for task execution (e.g., `"starter"`, `"standard"`, `"pro"`)
- `func: TaskFunction` - The task function, taking a `TaskContext` as its first parameter

**Returns:** A `TaskDefinition` — pass it to `ctx.run` to invoke the task in its own compute.

**Usage:**

```typescript
// Basic usage
const myTask = task(
  { name: "myTask" },
  function myTask(ctx: TaskContext, arg: string): string {
    return arg.toUpperCase();
  },
);

// With retry, timeout, and plan options
task(
  {
    name: "retryableTask",
    retry: {
      maxRetries: 3,
      waitDurationMs: 1000,
      backoffScaling: 1.5,
    },
    timeoutSeconds: 300,
    plan: "starter",
  },
  function retryableTask(ctx: TaskContext, arg: string): string {
    return arg.toUpperCase();
  },
);

// Async task with subtasks
const square = task(
  { name: "square" },
  function square(ctx: TaskContext, a: number): number {
    return a * a;
  },
);

task(
  { name: "addSquares" },
  async function addSquares(
    ctx: TaskContext,
    a: number,
    b: number,
  ): Promise<number> {
    const result1 = await ctx.run(square, a);
    const result2 = await ctx.run(square, b);
    return result1 + result2;
  },
);
```

#### `TaskContext`

Passed to every task as its first argument.

##### `ctx.run(task, ...args)`

Runs `task` on its own compute and resolves with its result.

**Parameters:**
- `task: TaskDefinition` - The task to run
- `...args` - The task's inputs, matching its signature

**Returns:** `Promise<TResult>` - Rejects with a `RenderError` if the subtask fails

#### `startTaskServer()`

Starts the task server and listens for task execution requests.

**Returns:** `Promise<void>`

**Example:**

```typescript
await startTaskServer();
```

### Types

#### `TaskRunStatus`

```typescript
enum TaskRunStatus {
  PENDING = "pending",
  RUNNING = "running",
  COMPLETED = "completed",
  FAILED = "failed",
  CANCELED = "canceled",
}
```

#### `TaskRun`

```typescript
interface TaskRun {
  id: string;
  taskId: string;
  status: TaskRunStatus;
  startedAt?: string;
  completedAt?: string;
  parentTaskRunId: string;
  rootTaskRunId: string;
  retries: number;
}
```

#### `TaskRunDetails`

```typescript
interface TaskRunDetails {
  id: string;
  taskId: string;
  status: TaskRunStatus;
  results?: any;
  error?: string;
  startedAt?: string;
  completedAt?: string;
}
```

#### `TaskRunResult`

```typescript
class TaskRunResult {
  readonly taskRunId: string;
  get(): Promise<TaskRunDetails>;
}
```

#### `FlowRunStatus`

```typescript
enum FlowRunStatus {
  PENDING = "pending",
  RUNNING = "running",
  PAUSED = "paused",
  SUCCEEDED = "succeeded",
  FAILED = "failed",
  CANCELED = "canceled",
}
```

#### `RegisterTaskOptions`

```typescript
interface RegisterTaskOptions {
  name: string;
  retry?: {
    maxRetries: number;
    waitDurationMs: number;
    backoffScaling?: number; // default 1.5
  };
  timeoutSeconds?: number;
  plan?: string; // e.g., "starter", "standard", "pro"
}
```

### Error Handling

The SDK provides several error classes:

```typescript
import { Render } from "@renderinc/sdk";
import {
  RenderError,
  TaskRunError,
  ClientError,
  ServerError,
  AbortError,
} from "@renderinc/sdk";

const render = new Render();

try {
  const result = await render.workflows.runTask("my-workflow/task", [42]);
} catch (error) {
  if (error instanceof TaskRunError) {
    console.error("Task failed:", error.taskRunId, error.message);
  } else if (error instanceof ClientError) {
    console.error("Client error:", error.statusCode, error.cause);
  } else if (error instanceof ServerError) {
    console.error("Server error:", error.statusCode, error.cause);
  } else if (error instanceof AbortError) {
    console.error("Request was aborted");
  } else if (error instanceof RenderError) {
    console.error("General SDK error:", error.message);
  }
}
```

## Environment Variables

- `RENDER_API_KEY` - Your Render API key
- `RENDER_WORKSPACE_ID` - Default owner ID for object storage (workspace team ID, e.g. `tea-xxxxx`)
- `RENDER_REGION` - Default region for object storage (e.g. `oregon`, `frankfurt`)
- `RENDER_USE_LOCAL_DEV` - Enable local development mode (`true`/`false`)
- `RENDER_LOCAL_DEV_URL` - Local development URL (default: `http://localhost:8120`)
- `RENDER_SDK_MODE` - Task execution mode (`run` or `register`)
- `RENDER_SDK_SOCKET_PATH` - Unix socket path for task communication
- `RENDER_LOCAL_REDIS_HOST` - Custom host for local Redis / Valkey instance (default: `localhost`) (requires `RENDER_USE_LOCAL_DEV=true`)
- `RENDER_LOCAL_REDIS_PORT` - Custom port for local Redis / Valkey instance (default: `6379`) (requires `RENDER_USE_LOCAL_DEV=true`)

### Object Storage

```typescript
import { Render } from "@renderinc/sdk";

const render = new Render(); // Uses env vars for auth + object storage defaults

// Upload (no need to pass ownerId/region when env vars are set)
await render.experimental.storage.objects.put({
  key: "path/to/file.png",
  data: Buffer.from("binary content"),
  contentType: "image/png",
});

// Download
const obj = await render.experimental.storage.objects.get({
  key: "path/to/file.png",
});

// List
const response = await render.experimental.storage.objects.list();
```

### Key Value

The Key Value API provides a Redis client backed by Render's managed Key Value service. It supports automatic instance provisioning and configuration sync.

Under the hood, it uses the [`redis`](https://www.npmjs.com/package/redis) package.

#### Basic usage

You can look up an instance by name and the SDK will create it if it doesn't exist. Note that the workspace ID needs to be set, either through the `RENDER_WORKSPACE_ID` environment variable or by passing the `ownerId` explicitly when calling the SDK:

```typescript
import { Render } from "@renderinc/sdk";

const render = new Render();

// Returns a configured (not yet connected) node-redis client
const client = await render.experimental.keyValue.newClient({
  name: "my-cache",
  ownerId: "tea-abcdefghijklmnopqrst",
});
const conn = await client.connect();

await conn.set("key", "value");
const value = await conn.get("key");

conn.destroy();
```

#### Look up by service ID

If you already have a Render Key Value service ID, pass it directly to skip the name lookup:

```typescript
const client = await render.experimental.keyValue.newClient({
  serviceId: "redis-xxxxxxxxxxxx",
});
```

#### Auto-provisioning with configuration

Pass an `autoProvision` configuration to control the plan and eviction policy. If the instance doesn't exist it will be created; if it exists but its settings differ they will be updated:

```typescript
const client = await render.experimental.keyValue.newClient({
  name: "my-cache",
  autoProvision: {
    plan: "starter",
    maxmemoryPolicy: "allkeys-lru",
  },
});
```

Set `autoProvision: false` to disable all automatic changes and throw if the instance is not found:

```typescript
const client = await render.experimental.keyValue.newClient({
  name: "my-cache",
  autoProvision: false,
});
```

#### Connection info only

Use `connectionInfo` when you need the host and port rather than a ready-made client:

```typescript
const info = await render.experimental.keyValue.connectionInfo({
  name: "my-cache",
}); // { host: 'my.redis.url', port: 1234, username: '...', password: '...' }
```

#### Local development

When `RENDER_USE_LOCAL_DEV=true` is set, the client connects to a local Valkey instance instead of the Render API. The easiest option for getting a local instance running is to use the [official Valkey Docker image](https://hub.docker.com/r/valkey/valkey):

```bash
docker run -p 6379:6379 valkey/valkey
```

When using the SDK in local development mode, the host and port default to `localhost:6379`. They can be overridden with the environment variables `RENDER_LOCAL_REDIS_HOST` and `RENDER_LOCAL_REDIS_PORT`.

## Examples

### Example 1: Running a Task

```typescript
import { Render } from "@renderinc/sdk";

const render = new Render();

const result = await render.workflows.runTask("my-workflow/square", [5]);
console.log("Square of 5 is:", result.results[0]); // 25
```

### Example 2: Defining Tasks with Subtasks

```typescript
import { task, type TaskContext } from "@renderinc/sdk/workflows";

const square = task(
  { name: "square" },
  function square(ctx: TaskContext, a: number): number {
    return a * a;
  },
);

task(
  { name: "pythagorean" },
  async function pythagorean(
    ctx: TaskContext,
    a: number,
    b: number,
  ): Promise<number> {
    const aSquared = await ctx.run(square, a);
    const bSquared = await ctx.run(square, b);
    return Math.sqrt(aSquared + bSquared);
  },
);
```

### Example 3: Error Handling in Tasks

```typescript
import { task, type TaskContext } from "@renderinc/sdk/workflows";

const divide = task(
  { name: "divide" },
  async function divide(
    ctx: TaskContext,
    a: number,
    b: number,
  ): Promise<number> {
    if (b === 0) {
      throw new Error("Cannot divide by zero");
    }
    return a / b;
  },
);

task(
  {
    name: "safeDivide",
    retry: {
      maxRetries: 3,
      waitDurationMs: 1000,
    },
  },
  async function safeDivide(
    ctx: TaskContext,
    a: number,
    b: number,
  ): Promise<number> {
    try {
      return await ctx.run(divide, a, b);
    } catch (error) {
      console.error("Division failed:", error);
      return 0; // Return default value
    }
  },
);
```

### Example 4: Using AbortSignal for Cancellation

```typescript
import { Render, AbortError } from "@renderinc/sdk";

const render = new Render();

async function runTaskWithCancellation() {
  const abortController = new AbortController();

  // Cancel the task after 5 seconds
  setTimeout(() => abortController.abort(), 5000);

  try {
    const result = await render.workflows.runTask(
      "my-workflow/long-running-task",
      [42],
      abortController.signal,
    );
    console.log("Task completed:", result.results);
  } catch (error) {
    if (error instanceof AbortError) {
      console.log("Task was cancelled");
    } else {
      console.error("Task failed:", error);
    }
  }
}

runTaskWithCancellation();
```

### Example 5: Using the Unified Render SDK

```typescript
import { Render } from "@renderinc/sdk";

// Single entry point for all Render products
const render = new Render({
  token: process.env.RENDER_API_KEY,
});

async function workflowExample() {
  try {
    // Run a workflow task
    const result = await render.workflows.runTask("my-workflow/process-data", [
      { userId: 123, data: "example" },
    ]);

    console.log("Workflow completed:", result.status);
    console.log("Results:", result.results);

    // List and monitor recent task runs
    const recentRuns = await render.workflows.listTaskRuns({ limit: 5 });
    console.log(`\nRecent task runs: ${recentRuns.length}`);

    for (const run of recentRuns) {
      console.log(`- ${run.id}: ${run.status} (${run.taskId})`);
    }
  } catch (error) {
    console.error("Error:", error);
  }
}

workflowExample();
```

## Development

### Building

```bash
npm run build
```

### Testing

```bash
npm test
```

### Linting

```bash
npm run lint
```

### Formatting

```bash
npm run format
```

## Project Structure

```
typescript/
├── src/
│   ├── render.ts              # Main Render SDK class
│   ├── errors.ts              # Error classes
│   ├── index.ts               # Main exports
│   ├── version.ts             # SDK version and user-agent
│   ├── workflows/             # Workflows functionality
│   │   ├── task.ts            # task() function
│   │   ├── runner.ts          # startTaskServer() and run()
│   │   ├── executor.ts        # TaskExecutor
│   │   ├── registry.ts        # TaskRegistry
│   │   ├── uds.ts             # Unix socket client
│   │   ├── types.ts           # Type definitions
│   │   ├── client/            # REST API client
│   │   │   ├── client.ts      # WorkflowsClient class
│   │   │   ├── create-client.ts # createWorkflowsClient() factory
│   │   │   ├── task-run-result.ts # TaskRunResult class
│   │   │   ├── sse.ts         # SSE event types
│   │   │   ├── types.ts       # Client type definitions
│   │   │   └── index.ts       # Exports
│   │   └── index.ts           # Workflows exports
│   ├── experimental/          # Experimental features
│   │   └── object/            # Object storage API
│   └── utils/                 # Shared utilities
├── examples/
│   ├── client/                # Client example
│   │   ├── main.ts
│   │   └── package.json
│   └── task/                  # Task example
│       ├── main.ts
│       └── package.json
├── package.json
├── tsconfig.json
└── README.md
```

## License

MIT

## Support

For issues and questions, please visit:
- GitHub Issues: <https://github.com/render-oss/sdk/issues>
- Documentation: <https://render.com/docs/workflows>

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting pull requests.
