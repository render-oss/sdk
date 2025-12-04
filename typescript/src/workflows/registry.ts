import type { RegisterTaskOptions, TaskFunction, TaskMetadata, TaskOptions } from './types.js';

/**
 * Global task registry
 */
export class TaskRegistry {
  private static instance: TaskRegistry;
  private tasks: Map<string, TaskMetadata> = new Map();

  private constructor() {}

  static getInstance(): TaskRegistry {
    if (!TaskRegistry.instance) {
      TaskRegistry.instance = new TaskRegistry();
    }
    return TaskRegistry.instance;
  }

  /**
   * Register a task with optional name and options
   */
  register(func: TaskFunction, options: RegisterTaskOptions): void {
    const taskName = options.name;
    if (!taskName) {
      throw new Error('Task function must have a name or name must be provided');
    }

    let taskOptions: TaskOptions | undefined;

    if (options.retry) {
      taskOptions = {
        retry: {
          max_retries: options.retry.maxRetries,
          wait_duration_ms: options.retry.maxRetries,
          factor: options.retry.factor,
        },
      };
    }

    this.tasks.set(taskName, {
      name: taskName,
      func,
      options: taskOptions,
    });
  }

  /**
   * Get a task by name
   */
  get(name: string): TaskMetadata | undefined {
    return this.tasks.get(name);
  }

  /**
   * Get all registered task names
   */
  getAllTaskNames(): string[] {
    return Array.from(this.tasks.keys());
  }

  getAllTasks(): TaskMetadata[] {
    return Array.from(this.tasks.values());
  }

  /**
   * Check if a task is registered
   */
  has(name: string): boolean {
    return this.tasks.has(name);
  }

  /**
   * Clear all registered tasks (useful for testing)
   */
  clear(): void {
    this.tasks.clear();
  }
}
