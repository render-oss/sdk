import { RenderError } from "../errors.js";
import type {
  AnyFlowFunction,
  AnyTaskFunction,
  FlowMetadata,
  FlowOptions,
  RegisterTaskOptions,
  TaskMetadata,
  TaskOptions,
} from "./types.js";

/**
 * Global task registry
 */
export class TaskRegistry {
  private static instance: TaskRegistry;
  private readonly tasks: Map<string, TaskMetadata> = new Map();
  private readonly flows: Map<string, FlowMetadata> = new Map();

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
  register(func: AnyTaskFunction, options: RegisterTaskOptions): void {
    const name = requireName(options);
    // Tasks and workflows share one namespace; the latest registration wins.
    this.flows.delete(name);
    this.tasks.set(name, { name, func, options: toTaskOptions(options) });
  }

  /**
   * Register a workflow. A workflow may not set a retry policy.
   */
  registerFlow(func: AnyFlowFunction, options: FlowOptions): void {
    // FlowOptions already makes this a compile error. The check is for
    // JavaScript and other untyped callers, so they see the problem when the
    // module loads rather than as a 400 at registration.
    if (options.retry !== undefined) {
      throw new RenderError(
        `Workflow '${options.name}': a retry policy is not allowed on a workflow. ` +
          "Workflows recover and replay instead; set retries on the steps it runs.",
      );
    }
    const name = requireName(options);
    this.tasks.delete(name);
    this.flows.set(name, { name, func, options: toTaskOptions(options) });
  }

  /**
   * Get a task by name
   */
  get(name: string): TaskMetadata | undefined {
    return this.tasks.get(name);
  }

  /**
   * Get a workflow by name
   */
  getFlow(name: string): FlowMetadata | undefined {
    return this.flows.get(name);
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

  getAllFlows(): FlowMetadata[] {
    return Array.from(this.flows.values());
  }

  /**
   * Check if a task is registered
   */
  has(name: string): boolean {
    return this.tasks.has(name);
  }

  /**
   * Clear all registered tasks and workflows (useful for testing)
   */
  clear(): void {
    this.tasks.clear();
    this.flows.clear();
  }
}

function requireName(options: RegisterTaskOptions | FlowOptions): string {
  if (!options.name) {
    throw new Error("Task function must have a name or name must be provided");
  }
  return options.name;
}

/** Convert task or workflow options to their wire form. */
function toTaskOptions(options: RegisterTaskOptions | FlowOptions): TaskOptions | undefined {
  if (!(options.retry || options.timeoutSeconds || options.plan)) {
    return undefined;
  }

  const taskOptions: TaskOptions = {};

  if (options.retry) {
    taskOptions.retry = {
      max_retries: options.retry.maxRetries,
      wait_duration_ms: options.retry.waitDurationMs,
      factor: options.retry.backoffScaling,
    };
  }

  if (options.timeoutSeconds) {
    taskOptions.timeout_seconds = options.timeoutSeconds;
  }

  if (options.plan) {
    taskOptions.plan = options.plan;
  }

  return taskOptions;
}
