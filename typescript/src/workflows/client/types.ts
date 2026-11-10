import type { components, paths } from "../../generated/schema";

/**
 * Task slug in the format "workflow-slug/task-name"
 */
export type TaskSlug = string;

/**
 * Task input data as an array of parameters
 */
export type TaskData = Array<any>;

/**
 * Task run status enum
 */
export enum TaskRunStatus {
  PENDING = "pending",
  RUNNING = "running",
  COMPLETED = "completed", // deprecated, use SUCCEEDED instead
  SUCCEEDED = "succeeded",
  FAILED = "failed",
  CANCELED = "canceled",
}

/**
 * Basic task run information
 */

export type TaskRun = components["schemas"]["TaskRun"];

/**
 * A task run paired with a pagination cursor, returned by list endpoints.
 */
export type TaskRunWithCursor = components["schemas"]["taskRunWithCursor"];

/**
 * Detailed task run information including results and errors
 */

export type TaskRunDetails = components["schemas"]["TaskRunDetails"];

/**
 * Parameters for listing task runs
 */
export type ListTaskRunsParams = paths["/task-runs"]["get"]["parameters"]["query"];

/**
 * Request body for running a task
 */
export interface RunTaskRequest {
  task: TaskSlug;
  input: TaskData;
  idempotencyKey?: string;
}

/**
 * Options for starting a task run or a flow run.
 */
export interface StartRunOptions {
  signal?: AbortSignal;
  /**
   * A client-generated key that makes starting the run safe to retry.
   * Repeating a call with the same key within 24 hours returns the run the
   * first call started instead of starting another one.
   */
  idempotencyKey?: string;
}

/**
 * Options for startTask() and runTask(). Idempotency keys are scoped to a
 * single workflow version.
 */
export type StartTaskOptions = StartRunOptions;

/**
 * Flow slug in the format "workflow-slug/flow-name". An optional version can be
 * appended ("workflow-slug/flow-name:version"); without one, the latest version is used.
 */
export type FlowSlug = string;

/**
 * Flow input data: an array of positional arguments or an object of named parameters
 */
export type FlowData = components["schemas"]["FlowInput"];

/**
 * Flow run status enum
 */
export enum FlowRunStatus {
  PENDING = "pending",
  RUNNING = "running",
  PAUSED = "paused",
  SUCCEEDED = "succeeded",
  FAILED = "failed",
  CANCELED = "canceled",
  SUSPENDED = "suspended",
  SLEEPING = "sleeping",
}

/**
 * Basic flow run information
 */
export type FlowRun = components["schemas"]["FlowRun"];

/**
 * A flow run paired with a pagination cursor, returned by list endpoints.
 */
export type FlowRunWithCursor = components["schemas"]["flowRunWithCursor"];

/**
 * Detailed flow run information including input, results, errors and attempts
 */
export type FlowRunDetails = components["schemas"]["FlowRunDetails"];

/**
 * Parameters for listing flow runs
 */
export type ListFlowRunsParams = paths["/flow-runs"]["get"]["parameters"]["query"];

/**
 * Request body for running a flow
 */
export type RunFlowRequest = components["schemas"]["StartFlowRun"];

/**
 * Options for startFlow(). Idempotency keys are scoped to a workflow.
 */
export type StartFlowOptions = StartRunOptions;

/**
 * Client configuration options
 */
export interface ClientOptions {
  token?: string;
  baseUrl?: string;
  useLocalDev?: boolean;
  localDevUrl?: string;
  /** Default owner ID for object storage. Falls back to RENDER_WORKSPACE_ID env var. */
  ownerId?: string;
  /** Default region for object storage. Falls back to RENDER_REGION env var. */
  region?: string;
}
