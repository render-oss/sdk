import http from "node:http";
import { getUserAgent } from "../version.js";

import type {
  CallbackRequest,
  GetInputResponse,
  GetSubtaskResultRequest,
  GetSubtaskResultResponse,
  RegisterTasksRequest,
  RunSubtaskRequest,
  RunSubtaskResponse,
  TaskMetadata,
} from "./types.js";

// Total retry window is ~2 minutes (175.5 seconds)
const UDS_MAX_RETRIES = 15;
const UDS_INITIAL_DELAY_MS = 250;
const UDS_BACKOFF_FACTOR = 2;
const UDS_MAX_DELAY_MS = 16_000;
const CLIENT_ERROR_RE = /^HTTP 4\d{2}:/;
const RETRY_ERROR_RE = /^HTTP 429:/;

/**
 * Unix Domain Socket client for communicating with the workflow system
 */
export class UDSClient {
  constructor(private readonly socketPath: string) {}

  /**
   * Get task input and name
   */
  async getInput(): Promise<GetInputResponse> {
    return this.request<GetInputResponse>("/input", "GET");
  }

  private buildCallbackBody(results?: any, error?: string): CallbackRequest {
    if (results !== undefined) {
      const resultsArray = [results];
      const output = Buffer.from(JSON.stringify(resultsArray)).toString("base64");
      return {
        complete: {
          output,
        },
      };
    }

    if (error === undefined) {
      throw new Error("Either results or error must be provided");
    }

    return {
      error: {
        details: error,
      },
    };
  }

  /**
   * Send task result or error
   */
  async sendCallback(results?: any, error?: string): Promise<void> {
    await this.request<void>("/callback", "POST", this.buildCallbackBody(results, error));
  }

  /**
   * Run a subtask
   */
  async runSubtask(taskName: string, input: any[]): Promise<string> {
    const inputBase64 = Buffer.from(JSON.stringify(input)).toString("base64");
    const body: RunSubtaskRequest = {
      task_name: taskName,
      input: inputBase64,
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
   * Register tasks with the workflow system
   */
  async registerTasks(tasks: TaskMetadata[]): Promise<void> {
    const body: RegisterTasksRequest = {
      tasks: tasks.map((task) => ({
        name: task.name,
        options: task.options,
      })),
    };
    await this.request<void>("/register-tasks", "POST", body);
  }

  /**
   * Make a request to the Unix socket with retry on transient errors.
   */
  private async request<T>(path: string, method: string, body?: any): Promise<T> {
    const bodyString = body ? JSON.stringify(body) : "";
    let lastError: Error = new Error("UDS request failed");

    for (let attempt = 0; attempt < UDS_MAX_RETRIES; attempt++) {
      try {
        return await this.requestOnce<T>(path, method, bodyString);
      } catch (e) {
        lastError = e instanceof Error ? e : new Error(String(e));

        // Don't retry on 4xx client errors except for 429s (rate limited)
        if (CLIENT_ERROR_RE.test(lastError.message) && !RETRY_ERROR_RE.test(lastError.message)) {
          throw lastError;
        }

        if (attempt < UDS_MAX_RETRIES - 1) {
          const delay = Math.min(
            UDS_INITIAL_DELAY_MS * UDS_BACKOFF_FACTOR ** attempt,
            UDS_MAX_DELAY_MS,
          );
          console.warn(
            `Request to Render failed (attempt ${attempt + 1}/${UDS_MAX_RETRIES}), ` +
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
            reject(new Error(`HTTP ${res.statusCode}: ${responseBody}`));
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
