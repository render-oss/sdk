import type { components } from "./schema.js";

/**
 * Execution context passed to every task as its first argument.
 *
 * The context is how a task reaches the rest of the workflow system.
 */
export interface TaskContext {
  /**
   * Run another task on its own compute and wait for its result.
   */
  run<TArgs extends unknown[], TResult>(
    task: TaskDefinition<TArgs, TResult>,
    ...args: TArgs
  ): Promise<TResult>;
}

/**
 * The function body of a task.
 */
export type TaskFunction<TArgs extends unknown[] = unknown[], TResult = unknown> = (
  ctx: TaskContext,
  ...args: TArgs
) => TResult | Promise<TResult>;

/**
 * A task function with its argument and result types erased.
 *
 * Used where tasks of differing signatures are stored together, such as the
 * registry. The parameters are `any[]` rather than `unknown[]` because
 * parameter positions are checked contravariantly: a
 * `TaskFunction<[number], string>` is not assignable to
 * `TaskFunction<unknown[], unknown>`, so the stricter type would force a cast at
 * every registration site.
 */
export type AnyTaskFunction = TaskFunction<any[], any>;

/**
 * A registered task.
 *
 * Pass it to {@link TaskContext.run}.
 */
export interface TaskDefinition<TArgs extends unknown[] = unknown[], TResult = unknown> {
  /** Name the task is registered under. */
  readonly name: string;
  /**
   * The undecorated function body.
   *
   * Invoke it directly to run the task in-process against a context you
   * supply, which is how tasks are exercised in unit tests.
   */
  readonly func: TaskFunction<TArgs, TResult>;
}

export type TaskOptions = components["schemas"]["TaskOptions"];

/**
 * Task metadata
 */
export interface TaskMetadata {
  name: string;
  func: AnyTaskFunction;
  options?: TaskOptions;
}

/**
 * Task input from the workflow system
 */
export interface TaskInput {
  task_name: string;
  input: any[];
}

/**
 * Task callback request/response types
 */

export type CallbackRequest = components["schemas"]["CallbackRequest"];

export type GetInputResponse = components["schemas"]["InputResponse"];

export type RunSubtaskRequest = components["schemas"]["RunSubtaskRequest"];

export type RunSubtaskResponse = components["schemas"]["RunSubtaskResponse"];

export type GetSubtaskResultRequest = components["schemas"]["SubtaskResultRequest"];

export type GetSubtaskResultResponse = components["schemas"]["SubtaskResultResponse"];

export type RegisterTasksRequest = components["schemas"]["Tasks"];

/**
 * Retry configuration for task execution
 */
export interface Retry {
  maxRetries: number;
  waitDurationMs: number;
  backoffScaling?: number; // default 1.5
}

/**
 * Task execution options
 */
export interface RegisterTaskOptions {
  retry?: Retry;
  timeoutSeconds?: number;
  /**
   * Resource plan for task execution.
   * Common plans include:
   * - "starter": 0.5 CPU, 512MB memory
   * - "standard": 1 CPU, 2GB memory (default)
   * - "pro": 2 CPU, 4GB memory
   */
  plan?: string;
  name: string;
}
