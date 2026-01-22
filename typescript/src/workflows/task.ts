import { AsyncLocalStorage } from "node:async_hooks";
import { TaskRegistry } from "./registry.js";
import type { RegisterTaskOptions, TaskContext, TaskFunction } from "./types.js";

/**
 * Storage for the current task execution context
 */
const taskContextStorage = new AsyncLocalStorage<TaskContext>();

/**
 * Flag to track if auto-start has been scheduled
 */
let autoStartScheduled = false;

/**
 * Flag to track if the server has started (set after startTaskServer completes)
 */
let serverStarted = false;

/**
 * Mark the server as started (called by runner after successful start)
 */
export function markServerStarted(): void {
  serverStarted = true;
}

/**
 * Check if auto-start should be enabled based on environment
 */
function shouldAutoStart(): boolean {
  // Must be in a workflow environment (socket path set)
  if (!process.env.RENDER_SDK_SOCKET_PATH) {
    return false;
  }

  // Check for opt-out via RENDER_SDK_AUTO_START=false
  const autoStartEnv = process.env.RENDER_SDK_AUTO_START;
  if (autoStartEnv !== undefined && autoStartEnv.toLowerCase() === "false") {
    return false;
  }

  return true;
}

/**
 * Get the current task context (only available during task execution)
 */
export function getCurrentContext(): TaskContext | undefined {
  return taskContextStorage.getStore();
}

/**
 * Set the current task context (used internally by executor)
 */
export function setCurrentContext<T>(context: TaskContext, fn: () => Promise<T>): Promise<T> {
  return taskContextStorage.run(context, fn);
}

/**
 * Register a task with the workflow system.
 *
 * When running in a workflow environment (RENDER_SDK_SOCKET_PATH is set),
 * the task server will automatically start after all synchronously-defined
 * tasks are registered. This can be disabled by setting RENDER_SDK_AUTO_START=false.
 *
 * @param func Task function
 * @param options Optional task options
 * @returns The registered function with the same signature
 */
export function task<TArgs extends any[], TResult>(
  options: RegisterTaskOptions,
  func: TaskFunction<TArgs, TResult>,
): TaskFunction<TArgs, TResult> {
  // Warn if task is registered after server has started. This is possible if
  // the task is loaded via dynamic import.
  if (serverStarted) {
    console.warn(
      `Warning: Task '${options.name}' was registered after the task server started. ` +
        `This task will not be available for execution. ` +
        `Ensure all tasks are defined synchronously at module level.`,
    );
  }

  const registry = TaskRegistry.getInstance();
  registry.register(func, options);

  // Schedule auto-start on first task registration when in workflow environment
  if (!autoStartScheduled && shouldAutoStart()) {
    autoStartScheduled = true;
    setImmediate(async () => {
      const { startTaskServer } = await import("./runner.js");
      try {
        await startTaskServer();
      } catch (error) {
        console.error("Failed to start task server:", error);
        process.exit(1);
      }
    });
  }

  // Return a wrapper function that executes the task as a subtask
  return ((...args: TArgs): TResult | Promise<TResult> => {
    const context = getCurrentContext();

    if (!context) {
      // If we're not in a task execution context, just run the function directly
      // This allows for testing and direct invocation
      return func(...args);
    }

    // Execute as a subtask through the context
    const result = context.executeTask(func, options.name, ...args);

    // Return the result wrapped in a promise that awaits the subtask
    return result.get();
  }) as TaskFunction<TArgs, TResult>;
}
