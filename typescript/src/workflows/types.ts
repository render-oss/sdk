import type { components } from './schema.js';

/**
 * Task function signature
 */
export type TaskFunction<TArgs extends any[] = any[], TResult = any> = (
  ...args: TArgs
) => TResult | Promise<TResult>;

export type TaskOptions = components['schemas']['TaskOptions'];

/**
 * Task metadata
 */
export interface TaskMetadata {
  name: string;
  func: TaskFunction;
  options?: TaskOptions;
}

/**
 * Task context for executing subtasks
 */
export interface TaskContext {
  executeTask<TArgs extends any[], TResult>(
    task: TaskFunction<TArgs, TResult>,
    taskName: string,
    ...args: TArgs
  ): TaskResult<TResult>;
}

/**
 * Result of a task execution
 */
export interface TaskResult<T> {
  get(): Promise<T>;
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

export type CallbackRequest = components['schemas']['CallbackRequest'];

export type GetInputResponse = components['schemas']['InputResponse'];

export type RunSubtaskRequest = components['schemas']['RunSubtaskRequest'];

export type RunSubtaskResponse = components['schemas']['RunSubtaskResponse'];

export type GetSubtaskResultRequest = components['schemas']['SubtaskResultRequest'];

export type GetSubtaskResultResponse = components['schemas']['SubtaskResultResponse'];

export type RegisterTasksRequest = components['schemas']['Tasks'];

/**
 * Retry configuration for task execution
 */
export interface Retry {
  maxRetries: number;
  waitDurationMs: number;
  factor?: number; // default 1.5
}

/**
 * Task execution options
 */
export interface RegisterTaskOptions {
  retry?: Retry;
  name: string;
}
