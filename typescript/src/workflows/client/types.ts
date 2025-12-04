import type { components, paths } from './schema';

/**
 * Task identifier in the format "workflow-slug/task-name"
 */
export type TaskIdentifier = string;

/**
 * Task input data as an array of parameters
 */
export type TaskData = Array<any>;

/**
 * Task run status enum
 */
export enum TaskRunStatus {
  PENDING = 'pending',
  RUNNING = 'running',
  COMPLETED = 'completed',
  FAILED = 'failed',
}

/**
 * Basic task run information
 */

export type TaskRun = components['schemas']['TaskRun'];

/**
 * Detailed task run information including results and errors
 */

export type TaskRunDetails = components['schemas']['TaskRunDetails'];

/**
 * Parameters for listing task runs
 */
export type ListTaskRunsParams = paths['/task-runs']['get']['parameters']['query'];

/**
 * Request body for running a task
 */
export interface RunTaskRequest {
  task: TaskIdentifier;
  input: TaskData;
}

/**
 * Client configuration options
 */
export interface ClientOptions {
  token?: string;
  baseUrl?: string;
  useLocalDev?: boolean;
  localDevUrl?: string;
}
