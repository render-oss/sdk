import { randomUUID } from "node:crypto";
import http from "node:http";
import { inputQuery } from "../startup.js";
import { getUserAgent } from "../version.js";
import { encodeArgs, encodeOutput } from "./encoding.js";

import type {
  CallbackRequest,
  FlowMetadata,
  GetInputResponse,
  GetSubtaskResultRequest,
  GetSubtaskResultResponse,
  RegisterTasksRequest,
  RunSubtaskRequest,
  RunSubtaskResponse,
  StepAttemptRequest,
  StepAttemptResponse,
  StepCompleteRequest,
  StepCompleteResponse,
  StepKey,
  StepStartRequest,
  StepStartResponse,
  TaskErrorBody,
  TaskMetadata,
  WaitRequest,
  WaitResponse,
} from "./types.js";

// Total retry window is ~5 minutes (303.75 seconds)
const UDS_MAX_RETRIES = 25;
const UDS_INITIAL_DELAY_MS = 250;
const UDS_BACKOFF_FACTOR = 2;
const UDS_MAX_DELAY_MS = 16_000;
const CLIENT_ERROR_RE = /^HTTP 4\d{2}:/;
const RETRY_ERROR_RE = /^HTTP 429:/;
// /step-wait isn't polled: it's one request that renderd may hold open while
// it waits on the child. These retries only cover failed requests (a dropped
// connection, 5xx or 429). The request is safe to repeat, so it retries for
// as long as the process lives; if the attempt suspends, renderd stops the
// process.
const LONG_POLL_MAX_RETRIES = Number.POSITIVE_INFINITY;

/**
 * An HTTP error status from the socket server. The message keeps the
 * `HTTP <status>: <body>` form.
 */
export class SocketHttpError extends Error {
  constructor(
    readonly status: number,
    readonly body: string,
  ) {
    super(`HTTP ${status}: ${body}`);
    this.name = "SocketHttpError";
  }

  /** The `code` field of a JSON error body, if there is one. */
  get code(): string | undefined {
    try {
      const code = JSON.parse(this.body)?.code;
      return typeof code === "string" ? code : undefined;
    } catch {
      return undefined;
    }
  }
}

/**
 * Unix Domain Socket client for communicating with the workflow system
 */
export class UDSClient {
  constructor(private readonly socketPath: string) {}

  /**
   * Get task input and name
   */
  async getInput(): Promise<GetInputResponse> {
    return this.request<GetInputResponse>(`/input${inputQuery()}`, "GET");
  }

  private buildCallbackBody(results?: any, error?: string | TaskErrorBody): CallbackRequest {
    // A result wins over an error; with neither, the task completed with no
    // output, which encodes as "".
    if (results !== undefined || !error) {
      return {
        complete: {
          output: encodeOutput(results),
        },
      };
    }

    return {
      error: typeof error === "string" ? { details: error } : error,
    };
  }

  /**
   * Send task result or error
   */
  async sendCallback(results?: any, error?: string | TaskErrorBody): Promise<void> {
    await this.request<void>("/callback", "POST", this.buildCallbackBody(results, error));
  }

  /**
   * Run a subtask
   */
  async runSubtask(taskName: string, input: any[], step?: StepKey): Promise<string> {
    // Build the body outside request(), which retries internally, so every
    // retry resends the same idempotency_key and created_at.
    const body: RunSubtaskRequest = {
      task_name: taskName,
      input: encodeArgs(input),
      idempotency_key: randomUUID(),
      created_at: new Date().toISOString(),
      step_key: step,
    };
    const response = await this.request<RunSubtaskResponse>("/run-subtask", "POST", body);
    return response.task_run_id;
  }

  /**
   * Get subtask result
   */
  async getSubtaskResult(subtaskId: string): Promise<GetSubtaskResultResponse> {
    const body: GetSubtaskResultRequest = {
      task_run_id: subtaskId,
    };
    return this.request<GetSubtaskResultResponse>("/get-subtask-result", "POST", body);
  }

  /**
   * Record an inline step's start, before its first attempt runs
   */
  async stepStart(body: StepStartRequest): Promise<StepStartResponse> {
    return this.request<StepStartResponse>("/step-inline/start", "POST", body);
  }

  /**
   * Record a failed attempt of an inline step that will be retried
   */
  async stepAttempt(body: StepAttemptRequest): Promise<StepAttemptResponse> {
    return this.request<StepAttemptResponse>("/step-inline/attempt", "POST", body);
  }

  /**
   * Record an inline step's outcome
   */
  async stepComplete(body: StepCompleteRequest): Promise<StepCompleteResponse> {
    return this.request<StepCompleteResponse>("/step-inline/complete", "POST", body);
  }

  /**
   * Wait for a detached subtask. This is one request, not a polling loop:
   * renderd holds it while it polls the child, then answers `done` with the
   * result or `suspending`. After a suspend, the replay posts it again for the
   * same child, and renderd answers right away once the child has finished.
   */
  async stepWait(body: WaitRequest): Promise<WaitResponse> {
    return this.request<WaitResponse>("/step-wait", "POST", body, LONG_POLL_MAX_RETRIES);
  }

  /**
   * Register tasks with the workflow system
   */
  async registerTasks(tasks: TaskMetadata[], workflows: FlowMetadata[] = []): Promise<void> {
    const body: RegisterTasksRequest = {
      tasks: [
        ...tasks.map((task) => ({
          name: task.name,
          options: task.options,
        })),
        ...workflows.map((workflow) => ({
          name: workflow.name,
          options: workflow.options,
          workflow: true,
        })),
      ],
    };
    await this.request<void>("/register-tasks", "POST", body);
  }

  /**
   * Make a request to the Unix socket with retry on transient errors.
   */
  private async request<T>(
    path: string,
    method: string,
    body?: any,
    maxRetries = UDS_MAX_RETRIES,
  ): Promise<T> {
    const bodyString = body ? JSON.stringify(body) : "";
    let lastError: Error = new Error("UDS request failed");

    for (let attempt = 0; attempt < maxRetries; attempt++) {
      try {
        return await this.requestOnce<T>(path, method, bodyString);
      } catch (e) {
        lastError = e instanceof Error ? e : new Error(String(e));

        // Don't retry on 4xx client errors except for 429s (rate limited)
        if (CLIENT_ERROR_RE.test(lastError.message) && !RETRY_ERROR_RE.test(lastError.message)) {
          throw lastError;
        }

        if (attempt < maxRetries - 1) {
          const delay = Math.min(
            UDS_INITIAL_DELAY_MS * UDS_BACKOFF_FACTOR ** attempt,
            UDS_MAX_DELAY_MS,
          );
          console.warn(
            `Request to Render failed (attempt ${attempt + 1}/${maxRetries}), ` +
              `retrying in ${delay}ms: ${lastError.message}`,
          );
          await new Promise<void>((resolve) => setTimeout(resolve, delay));
        }
      }
    }

    throw lastError;
  }

  /**
   * Make a single request to the Unix socket (no retry).
   */
  private async requestOnce<T>(path: string, method: string, bodyString: string): Promise<T> {
    return new Promise((resolve, reject) => {
      const req = http.request(
        {
          socketPath: this.socketPath,
          path: path,
          method: method,
          headers: {
            "Content-Length": Buffer.byteLength(bodyString),
            "Content-Type": "application/json",
            "User-Agent": getUserAgent(),
          },
        },
        async (res) => {
          const chunks: Buffer[] = [];
          for await (const chunk of res) chunks.push(chunk);
          const responseBody = Buffer.concat(chunks).toString();

          if (res.statusCode && res.statusCode >= 400) {
            reject(new SocketHttpError(res.statusCode, responseBody));
            return;
          }

          if (responseBody.length === 0) {
            resolve(undefined as T);
            return;
          }

          try {
            resolve(JSON.parse(responseBody));
          } catch (error) {
            reject(error);
          }
        },
      );
      req.on("error", (error) => {
        reject(error);
      });

      // Write the body to the request
      req.end(bodyString);
    });
  }
}
