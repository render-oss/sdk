import { TaskRegistry } from "./registry.js";
import type { RegisterTaskOptions, TaskContext, TaskDefinition, TaskFunction } from "./types.js";

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
 * Register a task with the workflow system.
 *
 * A task takes a {@link TaskContext} as its first parameter, followed by its
 * inputs. Use the context to reach other tasks: `ctx.run(other, input)`
 * runs one on its own compute and waits for its result.
 *
 * When running in a workflow environment (RENDER_SDK_SOCKET_PATH is set),
 * the task server will automatically start after all synchronously-defined
 * tasks are registered. This can be disabled by setting RENDER_SDK_AUTO_START=false.
 *
 * @param options Task options, including the name it registers under
 * @param func Task function, taking a TaskContext as its first parameter
 * @returns A task definition to pass to `ctx.run`
 */
export function task<TArgs extends unknown[], TResult>(
  options: RegisterTaskOptions,
  func: TaskFunction<TArgs, TResult>,
): TaskDefinition<TArgs, TResult> {
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

  return Object.freeze({
    name: options.name,
    func,
  });
}
