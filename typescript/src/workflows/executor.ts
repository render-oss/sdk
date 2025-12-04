import { RenderError } from './client/errors.js';
import { TaskRegistry } from './registry.js';
import { setCurrentContext } from './task.js';
import type { TaskContext, TaskFunction, TaskResult } from './types.js';
import { UDSClient } from './uds.js';

/**
 * Implementation of TaskResult
 */
class TaskResultImpl<T> implements TaskResult<T> {
  constructor(
    private subtaskId: string,
    private udsClient: UDSClient
  ) {}

  async get(): Promise<T> {
    // Poll for subtask result
    const maxAttempts = 120; // 10 minutes with 5 second intervals
    const pollInterval = 500; // half a second seconds

    for (let i = 0; i < maxAttempts; i++) {
      const result = await this.udsClient.getSubtaskResult(this.subtaskId);

      if (!result.still_running && result.complete) {
        if (result.complete.output) {
          const json = Buffer.from(result.complete.output, 'base64').toString();
          const decoded = JSON.parse(json);
          return decoded[0];
        }
        return undefined as T;
      } else if (!result.still_running && result.error) {
        throw new RenderError(`Subtask failed: ${result.error}`);
      }

      // Still pending, wait and retry
      await new Promise((resolve) => setTimeout(resolve, pollInterval));
    }

    throw new RenderError('Subtask did not complete within timeout');
  }
}

/**
 * Implementation of TaskContext
 */
class TaskContextImpl implements TaskContext {
  constructor(private udsClient: UDSClient) {}

  executeTask<TArgs extends any[], TResult>(
    _task: TaskFunction<TArgs, TResult>,
    taskName: string,
    ...args: TArgs
  ): TaskResult<TResult> {
    const registry = TaskRegistry.getInstance();

    if (!registry.has(taskName)) {
      throw new RenderError(`Task '${taskName}' is not registered`);
    }

    // Execute subtask via UDS
    const subtaskIdPromise = this.udsClient.runSubtask(taskName, args);

    // Return a TaskResult that will poll for completion
    return {
      get: async () => {
        const subtaskId = await subtaskIdPromise;
        const result = new TaskResultImpl<TResult>(subtaskId, this.udsClient);
        return result.get();
      },
    };
  }
}

/**
 * Task executor that runs tasks via Unix socket communication
 */
export class TaskExecutor {
  private udsClient: UDSClient;
  private context: TaskContext;

  constructor(socketPath: string) {
    this.udsClient = new UDSClient(socketPath);
    this.context = new TaskContextImpl(this.udsClient);
  }

  /**
   * Execute a single task
   */
  async executeTask(): Promise<void> {
    const registry = TaskRegistry.getInstance();

    try {
      // Get task input
      const input = await this.udsClient.getInput();
      const taskName = input.task_name;
      const inputData = JSON.parse(Buffer.from(input.input, 'base64').toString());

      // Get task from registry
      const taskMetadata = registry.get(taskName);
      if (!taskMetadata) {
        throw new RenderError(`Task '${taskName}' not found in registry`);
      }

      // Execute task with context
      const result = await setCurrentContext(this.context, async () => {
        return await taskMetadata.func(...inputData);
      });

      // Send result
      await this.udsClient.sendCallback(result);
    } catch (error) {
      // Send error
      const errorMessage = error instanceof Error ? error.message : String(error);
      await this.udsClient.sendCallback(undefined, errorMessage);
      throw error;
    }
  }

  /**
   * Register all tasks with the workflow system
   */
  async registerTasks(): Promise<void> {
    const registry = TaskRegistry.getInstance();
    const tasks = registry.getAllTasks();
    await this.udsClient.registerTasks(tasks);
  }
}
