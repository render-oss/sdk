import { EventSource } from "eventsource";
import type { Client as ApiClient } from "openapi-fetch";
import { AbortError, ClientError, ServerError } from "../../errors.js";
import type { paths } from "../../generated/schema.js";
import { getUserAgent } from "../../version.js";
import { TaskEventType } from "./sse.js";
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
  private readonly apiClient: ApiClient<paths>;
  private readonly baseUrl: string;
  private readonly token: string;

  /**
   * Create a new Render SDK client
   * @param options Client configuration options
   * @returns New client instance
   */
  constructor(apiClient: ApiClient<paths>, baseUrl: string, token: string) {
    this.apiClient = apiClient;
    this.baseUrl = baseUrl;
    this.token = token;
  }

  /**
   * Stream task run events as an async iterable.
   * Yields a TaskRunDetails for each terminal event (completed or failed)
   * received on the SSE stream.
   *
   * @param taskRunIds - One or more task run IDs to subscribe to
   * @param signal - Optional AbortSignal to cancel the stream
   */
  async *taskRunEvents(taskRunIds: string[], signal?: AbortSignal): AsyncGenerator<TaskRunDetails> {
    if (signal?.aborted) {
      throw new AbortError();
    }

    // Simple async queue: push events from EventSource handlers,
    // yield them from the generator loop.
    const queue: TaskRunDetails[] = [];
    let resolve: (() => void) | null = null;
    let finished = false;
    let streamError: Error | null = null;

    const push = (item: TaskRunDetails) => {
      queue.push(item);
      if (resolve) {
        resolve();
        resolve = null;
      }
    };

    const fail = (err: Error) => {
      streamError = err;
      finished = true;
      if (resolve) {
        resolve();
        resolve = null;
      }
    };

    const url = new URL("/v1/task-runs/events", this.baseUrl);
    url.searchParams.append("taskRunIds", taskRunIds.join(","));

    const eventSource = new EventSource(url.toString(), {
      fetch: (input, init) =>
        fetch(input, {
          ...init,
          headers: {
            ...init?.headers,
            Authorization: `Bearer ${this.token}`,
            "User-Agent": getUserAgent(),
          },
        }),
    });

    const eventHandler = (event: MessageEvent) => {
      try {
        const details = JSON.parse(event.data) as TaskRunDetails;
        push(details);
      } catch (e) {
        fail(new Error(`Failed to parse task run details: ${e}`));
      }
    };

    const errorHandler = (error: any) => {
      fail(new Error(`SSE connection error: ${error.message || "Unknown error"}`));
    };

    const abortHandler = () => {
      cleanup();
      fail(new AbortError());
    };

    const cleanup = () => {
      eventSource.removeEventListener(TaskEventType.COMPLETED, eventHandler);
      eventSource.removeEventListener(TaskEventType.FAILED, eventHandler);
      eventSource.removeEventListener("error", errorHandler);
      eventSource.close();
      signal?.removeEventListener("abort", abortHandler);
    };

    eventSource.addEventListener(TaskEventType.COMPLETED, eventHandler);
    eventSource.addEventListener(TaskEventType.FAILED, eventHandler);
    eventSource.addEventListener("error", errorHandler);
    signal?.addEventListener("abort", abortHandler);

    try {
      while (true) {
        // Drain anything already in the queue
        while (queue.length > 0) {
          yield queue.shift() as TaskRunDetails;
        }

        if (finished) {
          break;
        }

        // Wait for the next event
        await new Promise<void>((r) => {
          resolve = r;
        });
      }

      if (streamError) {
        throw streamError;
      }
    } finally {
      cleanup();
    }
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

      return new TaskRunResult((id, sig) => this.waitOnTaskRun(id, sig), data.id, signal);
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

  /**
   * Wait for a single task run to complete or fail via SSE.
   * Used internally by TaskRunResult.get().
   */
  private async waitOnTaskRun(taskRunId: string, signal?: AbortSignal): Promise<TaskRunDetails> {
    for await (const event of this.taskRunEvents([taskRunId], signal)) {
      return event;
    }
    throw new Error(`SSE stream ended without receiving an event for task run ${taskRunId}`);
  }
}
