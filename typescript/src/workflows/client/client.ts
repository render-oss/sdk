import type { Client as ApiClient } from "openapi-fetch";
import { AbortError, ClientError, ServerError } from "../../errors.js";
import type { paths } from "../../generated/schema.js";
import { SSEClient } from "./sse.js";
import { TaskRunResult } from "./task-run-result.js";
import type {
  ListTaskRunsParams,
  TaskData,
  TaskIdentifier,
  TaskRun,
  TaskRunDetails,
} from "./types.js";

/**
 * Helper function to handle API errors and throw appropriate custom error types
 */
function handleApiError(error: any, response: Response, context: string): never {
  const statusCode = response.status;
  const errorMessage = `${context}: ${error}`;

  if (statusCode >= 500) {
    throw new ServerError(errorMessage, statusCode, error);
  } else if (statusCode >= 400) {
    throw new ClientError(errorMessage, statusCode, error);
  }
  throw new ClientError(errorMessage, statusCode, error);
}

/**
 * Main Render SDK Client
 */
export class WorkflowsClient {
  private readonly sse: SSEClient;
  private readonly apiClient: ApiClient<paths>;

  /**
   * Create a new Render SDK client
   * @param options Client configuration options
   * @returns New client instance
   */
  constructor(apiClient: ApiClient<paths>, baseUrl: string, token: string) {
    this.sse = new SSEClient(baseUrl, token);
    this.apiClient = apiClient;
  }

  /**
   * Start a task run and return a TaskRunResult promise.
   * Results are not streamed until you call .get() on the returned result.
   * Use this when you just need the task run ID, want to defer awaiting, or
   * want fire-and-forget.
   */
  async startTask(
    taskIdentifier: TaskIdentifier,
    inputData: TaskData,
    signal?: AbortSignal,
  ): Promise<TaskRunResult> {
    if (signal?.aborted) {
      throw new AbortError();
    }

    try {
      const { data, error, response } = await this.apiClient.POST("/task-runs", {
        body: {
          task: taskIdentifier,
          input: inputData,
        },
        signal,
      });

      if (error) {
        handleApiError(error, response, "Failed to run task");
      }

      return new TaskRunResult(this.sse, data.id, signal);
    } catch (err) {
      if (err instanceof DOMException && err.name === "AbortError") {
        throw new AbortError();
      }
      throw err;
    }
  }

  /**
   * Start a task run and wait for it to complete, returning the final result.
   * This is a convenience wrapper around startTask() + .get().
   */
  async runTask(
    taskIdentifier: TaskIdentifier,
    inputData: TaskData,
    signal?: AbortSignal,
  ): Promise<TaskRunDetails> {
    const result = await this.startTask(taskIdentifier, inputData, signal);
    return result.get();
  }

  /**
   * Get task run details by ID
   * @param taskRunId Task run ID
   * @returns Task run details
   */

  async getTaskRun(taskRunId: string): Promise<TaskRunDetails> {
    const { data, error, response } = await this.apiClient.GET("/task-runs/{taskRunId}", {
      params: { path: { taskRunId } },
    });
    if (error) {
      handleApiError(error, response, "Failed to get task run");
    }
    return data;
  }

  /**
   * Cancel a task run
   * @param taskRunId Task run ID
   */
  async cancelTaskRun(taskRunId: string): Promise<void> {
    const { error, response } = await this.apiClient.DELETE("/task-runs/{taskRunId}", {
      params: { path: { taskRunId } },
    });
    if (error) {
      handleApiError(error, response, "Failed to cancel task run");
    }
  }

  /**
   * List task runs with optional filters
   * @param params Filter parameters
   * @returns List of task runs
   */

  async listTaskRuns(params: ListTaskRunsParams): Promise<TaskRun[]> {
    const { data, error, response } = await this.apiClient.GET("/task-runs", {
      params: { query: params },
    });
    if (error) {
      handleApiError(error, response, "Failed to list task runs");
    }
    return data;
  }
}
