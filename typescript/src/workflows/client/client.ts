import { type ErrorEvent, EventSource } from "eventsource";
import type { Client as ApiClient } from "openapi-fetch";
import { AbortError } from "../../errors.js";
import type { paths } from "../../generated/schema.js";
import { getApiError, isConnectionError } from "../../utils/http.js";
import { getUserAgent } from "../../version.js";
import { TaskEventType } from "./sse.js";
import { TaskRunResult } from "./task-run-result.js";
import type {
  ListTaskRunsParams,
  TaskData,
  TaskRunDetails,
  TaskRunWithCursor,
  TaskSlug,
} from "./types.js";

/**
 * Main Workflow SDK Client
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
   * Yields a TaskRunDetails for each terminal event (completed, failed, or canceled)
   * received on the SSE stream.
   *
   * @param taskRunIds - One or more task run IDs to subscribe to
   * @param signal - Optional AbortSignal to cancel the stream
   * @param options - Optional configuration for retry behavior
   */
  async *taskRunEvents(
    taskRunIds: string[],
    signal?: AbortSignal,
    options?: {
      maxRetries?: number;
      initialDelayMs?: number;
      backoffFactor?: number;
      maxDelayMs?: number;
    },
  ): AsyncGenerator<TaskRunDetails> {
    if (signal?.aborted) {
      throw new AbortError();
    }

    const maxRetries = options?.maxRetries ?? 5;
    const initialDelayMs = options?.initialDelayMs ?? 250;
    const backoffFactor = options?.backoffFactor ?? 2;
    const maxDelayMs = options?.maxDelayMs ?? 16_000;

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

    const token = this.token;
    let eventSource: EventSource | null = null;
    let attempt = 0;
    let retryTimeout: NodeJS.Timeout | null = null;

    const eventHandler = (event: MessageEvent) => {
      try {
        const details = JSON.parse(event.data) as TaskRunDetails;
        attempt = 0; // Reset retry counter on successful event
        push(details);
      } catch (e) {
        fail(new Error(`Failed to parse task run details: ${e}`));
      }
    };

    const errorHandler = (error: ErrorEvent) => {
      // If error is not connection related, propagate immediately
      if (!isConnectionError(error)) {
        fail(new Error(`SSE connection error: ${error.message || "Unknown error"}`));
        return;
      }

      // If connection related but we exhausted retries, propagate
      if (attempt >= maxRetries) {
        fail(new Error(`SSE connection error: ${error.message || "Unknown error"}`));
        return;
      }

      // Schedule a retry with exponential backoff
      const delay = Math.min(initialDelayMs * backoffFactor ** attempt, maxDelayMs);
      attempt++;

      cleanupEventSource();

      retryTimeout = setTimeout(() => {
        retryTimeout = null;
        connect();
      }, delay);
    };

    const openHandler = () => {
      attempt = 0; // Reset retry counter on successful open
    };

    const abortHandler = () => {
      cleanup();
      fail(new AbortError());
    };

    const cleanupEventSource = () => {
      if (eventSource) {
        eventSource.removeEventListener(TaskEventType.COMPLETED, eventHandler);
        eventSource.removeEventListener(TaskEventType.FAILED, eventHandler);
        eventSource.removeEventListener(TaskEventType.CANCELED, eventHandler);
        eventSource.removeEventListener("error", errorHandler);
        eventSource.removeEventListener("open", openHandler);
        eventSource.close();
        eventSource = null;
      }
    };

    const cleanup = () => {
      if (retryTimeout) {
        clearTimeout(retryTimeout);
        retryTimeout = null;
      }
      cleanupEventSource();
      signal?.removeEventListener("abort", abortHandler);
    };

    const connect = () => {
      cleanupEventSource();

      if (signal?.aborted) {
        fail(new AbortError());
        return;
      }

      eventSource = new EventSource(url.toString(), {
        fetch: (input, init) => {
          const headers: Record<string, string> = {
            ...(init?.headers as Record<string, string> | undefined),
            "User-Agent": getUserAgent(),
          };
          if (token) {
            headers.Authorization = `Bearer ${token}`;
          }
          return fetch(input, { ...init, headers });
        },
      });

      eventSource.addEventListener(TaskEventType.COMPLETED, eventHandler);
      eventSource.addEventListener(TaskEventType.FAILED, eventHandler);
      eventSource.addEventListener(TaskEventType.CANCELED, eventHandler);
      eventSource.addEventListener("error", errorHandler);
      eventSource.addEventListener("open", openHandler);
    };

    // Start initial connection
    connect();
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
    taskSlug: TaskSlug,
    inputData: TaskData,
    signal?: AbortSignal,
  ): Promise<TaskRunResult> {
    if (signal?.aborted) {
      throw new AbortError();
    }

    try {
      const { data, error, response } = await this.apiClient.POST("/task-runs", {
        body: {
          task: taskSlug,
          input: inputData,
        },
        signal,
      });

      if (error) {
        throw getApiError(`${error.message} ${error.id}`, response, "Failed to run task");
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
    taskSlug: TaskSlug,
    inputData: TaskData,
    signal?: AbortSignal,
  ): Promise<TaskRunDetails> {
    const result = await this.startTask(taskSlug, inputData, signal);
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
      throw getApiError(`${error.message} ${error.id}`, response, "Failed to get task run");
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
      throw getApiError(`${error.message} ${error.id}`, response, "Failed to cancel task run");
    }
  }

  /**
   * List task runs with optional filters
   * @param params Filter parameters
   * @returns List of task runs
   */

  async listTaskRuns(params: ListTaskRunsParams): Promise<TaskRunWithCursor[]> {
    const { data, error, response } = await this.apiClient.GET("/task-runs", {
      params: { query: params },
    });
    if (error) {
      throw getApiError(`${error.message} ${error.id}`, response, "Failed to list task runs");
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
