import { AsyncLocalStorage } from 'node:async_hooks';
import { TaskRegistry } from './registry.js';
import type { RegisterTaskOptions, TaskContext, TaskFunction } from './types.js';

/**
 * Storage for the current task execution context
 */
const taskContextStorage = new AsyncLocalStorage<TaskContext>();

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
 * Manually register a task
 * @param func Task function
 * @param name Optional custom name
 * @param options Optional task options
 * @returns The registered function with the same signature
 */
export function task<TArgs extends any[], TResult>(
  options: RegisterTaskOptions,
  func: TaskFunction<TArgs, TResult>
): TaskFunction<TArgs, TResult> {
  const registry = TaskRegistry.getInstance();
  registry.register(func, options);

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
