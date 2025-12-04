# Render Workflow SDK for TypeScript

The official TypeScript SDK for Render Workflows, providing a simple and intuitive API for managing and executing tasks.

## Features

- **REST API Client**: Run, monitor, and manage task runs
- **Task Definition SDK**: Define and register tasks with decorators
- **Server-Sent Events**: Real-time streaming of task run events
- **Async/Await Support**: Modern Promise-based API
- **TypeScript First**: Full type safety and IntelliSense support
- **Retry Logic**: Configurable retry behavior for tasks
- **Subtask Execution**: Execute tasks from within other tasks

## Installation

```bash
npm install @render/sdk
```

Or with yarn:

```bash
yarn add @render/sdk
```

Or with pnpm:

```bash
pnpm add @render/sdk
```

## Quick Start

### REST API Client

Use the client to run tasks and monitor their execution:

```typescript
import { Client } from '@render/sdk/workflows';

// Create a client (uses RENDER_API_KEY from environment)
const client = new Client();

// Run a task and wait for completion
const result = await client.runTask('my-workflow/my-task', [42, 'hello']);
console.log('Status:', result.status);
console.log('Results:', result.results);

// List recent task runs
const taskRuns = await client.listTaskRuns({ limit: 10 });

// Get specific task run
const details = await client.getTaskRun(result.id);
```

### Task Definition

Define tasks that can be executed by the workflow system:

```typescript
import { task, startTaskServer } from '@render/sdk/workflows';

// Simple task
const square = task(
  { name: 'square' },
  function square(a: number): number {
    return a * a;
  }
);

// Async task with subtask execution
task(
  { name: 'addSquares' },
  async function addSquares(a: number, b: number): Promise<number> {
    const result1 = await square(a);
    const result2 = await square(b);
    return result1 + result2;
  }
);

// Task with custom options
task(
  {
    name: 'retryableTask',
    retry: {
      maxRetries: 3,
      waitDurationMs: 1000,
      factor: 1.5,
    },
  },
  async function retryableTask(input: string): Promise<string> {
    // Task implementation
    return input.toUpperCase();
  }
);

// Start the task server
await startTaskServer();
```

## API Reference

### Client API

#### `new Client(options?)`

Creates a new Render SDK client.

**Options:**
- `token?: string` - API token (defaults to `RENDER_API_KEY` env var)
- `baseUrl?: string` - Base URL (defaults to `https://api.render.com`)
- `useLocalDev?: boolean` - Use local development mode
- `localDevUrl?: string` - Local development URL

**Example:**
```typescript
const client = new Client({
  token: 'your-api-token',
  baseUrl: 'https://api.render.com',
});
```

### Client Methods

#### `client.runTask(taskIdentifier, inputData, signal?)`

Runs a task and waits for completion.

**Parameters:**
- `taskIdentifier: string` - Task identifier in format "workflow-slug/task-name"
- `inputData: any[]` - Input data as array of parameters
- `signal?: AbortSignal` - Optional abort signal for cancellation

**Returns:** `Promise<TaskRunDetails>`

**Example:**
```typescript
const result = await client.runTask('my-workflow/square', [5]);
console.log('Results:', result.results);
```

#### `client.getTaskRun(taskRunId)`

Gets task run details by ID.

**Parameters:**
- `taskRunId: string` - Task run ID

**Returns:** `Promise<TaskRunDetails>`

**Example:**
```typescript
const details = await client.getTaskRun('task-run-id');
```

#### `client.listTaskRuns(params)`

Lists task runs with optional filters.

**Parameters:**
- `params.limit?: number` - Maximum number of results
- `params.cursor?: string` - Pagination cursor
- `params.ownerId?: string[]` - Filter by owner IDs

**Returns:** `Promise<TaskRun[]>`

**Example:**
```typescript
const taskRuns = await client.listTaskRuns({ limit: 10 });
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
    - `factor?: number` - Backoff factor (default: 1.5)
- `func: TaskFunction` - The task function to register

**Returns:** The registered function with the same signature

**Usage:**
```typescript
// Basic usage
const myTask = task(
  { name: 'myTask' },
  function myTask(arg: string): string {
    return arg.toUpperCase();
  }
);

// With retry options
task(
  {
    name: 'retryableTask',
    retry: {
      maxRetries: 3,
      waitDurationMs: 1000,
      factor: 1.5,
    },
  },
  function retryableTask(arg: string): string {
    return arg.toUpperCase();
  }
);

// Async task with subtasks
const square = task(
  { name: 'square' },
  function square(a: number): number {
    return a * a;
  }
);

task(
  { name: 'addSquares' },
  async function addSquares(a: number, b: number): Promise<number> {
    const result1 = await square(a);
    const result2 = await square(b);
    return result1 + result2;
  }
);
```

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
  PENDING = 'pending',
  RUNNING = 'running',
  COMPLETED = 'completed',
  FAILED = 'failed',
}
```

#### `TaskRun`

```typescript
interface TaskRun {
  id: string;
  status: TaskRunStatus;
  created_at: string;
  updated_at: string;
  task_identifier: string;
}
```

#### `TaskRunDetails`

```typescript
interface TaskRunDetails extends TaskRun {
  completed_at?: string;
  results?: any[];
  error?: string;
}
```

#### `RegisterTaskOptions`

```typescript
interface RegisterTaskOptions {
  name: string;
  retry?: {
    maxRetries: number;
    waitDurationMs: number;
    factor?: number; // default 1.5
  };
}
```

### Error Handling

The SDK provides several error classes:

```typescript
import {
  RenderError,
  ClientError,
  ServerError,
  AbortError,
} from '@render/sdk/workflows';

try {
  const result = await client.runTask('my-workflow/task', [42]);
} catch (error) {
  if (error instanceof ClientError) {
    console.error('Client error:', error.statusCode, error.cause);
  } else if (error instanceof ServerError) {
    console.error('Server error:', error.statusCode, error.cause);
  } else if (error instanceof AbortError) {
    console.error('Request was aborted');
  } else if (error instanceof RenderError) {
    console.error('General SDK error:', error.message);
  }
}
```

## Environment Variables

- `RENDER_API_KEY` - Your Render API key (required)
- `RENDER_USE_LOCAL_DEV` - Enable local development mode (`true`/`false`)
- `RENDER_LOCAL_DEV_URL` - Local development URL (default: `http://localhost:8120`)
- `RENDER_SDK_MODE` - Task execution mode (`run` or `register`)
- `RENDER_SDK_SOCKET_PATH` - Unix socket path for task communication

## Examples

### Example 1: Running a Task

```typescript
import { Client } from '@render/sdk/workflows';

const client = new Client();

async function runSquareTask() {
  const result = await client.runTask('my-workflow/square', [5]);
  console.log('Square of 5 is:', result.results[0]); // 25
}
```

### Example 2: Defining Tasks with Subtasks

```typescript
import { task, startTaskServer } from '@render/sdk/workflows';

const square = task(
  { name: 'square' },
  function square(a: number): number {
    return a * a;
  }
);

task(
  { name: 'pythagorean' },
  async function pythagorean(a: number, b: number): Promise<number> {
    const aSquared = await square(a);
    const bSquared = await square(b);
    return Math.sqrt(aSquared + bSquared);
  }
);

await startTaskServer();
```

### Example 3: Error Handling in Tasks

```typescript
import { task } from '@render/sdk/workflows';

const divide = task(
  { name: 'divide' },
  async function divide(a: number, b: number): Promise<number> {
    if (b === 0) {
      throw new Error('Cannot divide by zero');
    }
    return a / b;
  }
);

task(
  {
    name: 'safeDivide',
    retry: {
      maxRetries: 3,
      waitDurationMs: 1000,
    },
  },
  async function safeDivide(a: number, b: number): Promise<number> {
    try {
      return await divide(a, b);
    } catch (error) {
      console.error('Division failed:', error);
      return 0; // Return default value
    }
  }
);
```

### Example 4: Using AbortSignal for Cancellation

```typescript
import { Client, AbortError } from '@render/sdk/workflows';

const client = new Client();

async function runTaskWithCancellation() {
  const abortController = new AbortController();

  // Cancel the task after 5 seconds
  setTimeout(() => abortController.abort(), 5000);

  try {
    const result = await client.runTask(
      'my-workflow/long-running-task',
      [42],
      abortController.signal
    );
    console.log('Task completed:', result.results);
  } catch (error) {
    if (error instanceof AbortError) {
      console.log('Task was cancelled');
    } else {
      console.error('Task failed:', error);
    }
  }
}
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
│   ├── client/              # REST API client
│   │   ├── client.ts        # Main Client class
│   │   ├── workflows.ts     # WorkflowsService
│   │   ├── sse.ts           # SSE client
│   │   ├── types.ts         # Type definitions
│   │   ├── errors.ts        # Error classes
│   │   └── index.ts         # Exports
│   ├── workflows/           # Task execution SDK
│   │   ├── task.ts          # @task decorator
│   │   ├── runner.ts        # start() and run()
│   │   ├── executor.ts      # TaskExecutor
│   │   ├── registry.ts      # TaskRegistry
│   │   ├── uds.ts           # Unix socket client
│   │   ├── types.ts         # Type definitions
│   │   └── index.ts         # Exports
│   └── index.ts             # Main exports
├── examples/
│   ├── client/              # Client example
│   │   ├── main.ts
│   │   └── package.json
│   └── task/                # Task example
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
- GitHub Issues: https://github.com/renderinc/workflow-sdk/issues
- Documentation: https://render.com/docs/workflows

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting pull requests.
