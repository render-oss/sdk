import * as net from 'node:net';
import type {
  CallbackRequest,
  GetInputResponse,
  GetSubtaskResultRequest,
  GetSubtaskResultResponse,
  RegisterTasksRequest,
  RunSubtaskRequest,
  RunSubtaskResponse,
  TaskMetadata,
} from './types.js';

/**
 * Unix Domain Socket client for communicating with the workflow system
 */
export class UDSClient {
  constructor(private socketPath: string) {}

  /**
   * Get task input and name
   */
  async getInput(): Promise<GetInputResponse> {
    return this.request<GetInputResponse>('/input', 'GET');
  }

  private buildCallbackBody(results?: any, error?: string): CallbackRequest {
    if (results) {
      const resultsArray = [results];
      const output = Buffer.from(JSON.stringify(resultsArray)).toString('base64');
      return {
        complete: {
          output,
        },
      };
    }
    return {
      error: {
        details: error!,
      },
    };
  }

  /**
   * Send task result or error
   */
  async sendCallback(results?: any, error?: string): Promise<void> {
    await this.request<void>('/callback', 'POST', this.buildCallbackBody(results, error));
  }

  /**
   * Run a subtask
   */
  async runSubtask(taskName: string, input: any[]): Promise<string> {
    const inputBase64 = Buffer.from(JSON.stringify(input)).toString('base64');
    const body: RunSubtaskRequest = {
      task_name: taskName,
      input: inputBase64,
    };
    const response = await this.request<RunSubtaskResponse>('/run-subtask', 'POST', body);
    return response.task_run_id;
  }

  /**
   * Get subtask result
   */
  async getSubtaskResult(subtaskId: string): Promise<GetSubtaskResultResponse> {
    const body: GetSubtaskResultRequest = {
      task_run_id: subtaskId,
    };
    return this.request<GetSubtaskResultResponse>('/get-subtask-result', 'POST', body);
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
    await this.request<void>('/register-tasks', 'POST', body);
  }

  /**
   * Make a request to the Unix socket
   */
  private async request<T>(path: string, method: string, body?: any): Promise<T> {
    return new Promise((resolve, reject) => {
      const client = net.createConnection({ path: this.socketPath }, () => {
        const bodyStr = body ? JSON.stringify(body) : '';
        const request = `${method} ${path} HTTP/1.1\r\nHost: unix\r\nContent-Length: ${bodyStr.length}\r\nContent-Type: application/json\r\n\r\n${bodyStr}`;
        client.write(request);
      });

      let data = '';
      let contentLength: number | null = null;
      let headersParsed = false;
      let bodyStartIndex = -1;

      client.on('data', (chunk) => {
        data += chunk.toString();

        // Check if we have received the full response
        if (!headersParsed) {
          const headerEndIndex = data.indexOf('\r\n\r\n');
          if (headerEndIndex !== -1) {
            headersParsed = true;
            bodyStartIndex = headerEndIndex + 4;

            // Parse Content-Length header
            const headers = data.substring(0, headerEndIndex);
            const contentLengthMatch = headers.match(/Content-Length:\s*(\d+)/i);
            if (contentLengthMatch) {
              contentLength = parseInt(contentLengthMatch[1], 10);
            }
          }
        }

        // Check if we have received the complete body
        if (headersParsed && contentLength !== null) {
          const bodyReceived = data.length - bodyStartIndex;
          if (bodyReceived >= contentLength) {
            // We have the complete response, close the connection
            client.end();
          }
        }
      });

      client.on('end', () => {
        try {
          // Parse HTTP response
          const lines = data.split('\r\n');
          const statusLine = lines[0];
          const statusCode = parseInt(statusLine.split(' ')[1], 10);

          if (statusCode >= 400) {
            reject(new Error(`HTTP ${statusCode}: ${data}`));
            return;
          }

          // Find empty line (separates headers from body)
          const emptyLineIndex = lines.indexOf('');
          if (emptyLineIndex === -1) {
            resolve(undefined as T);
            return;
          }

          const bodyLines = lines.slice(emptyLineIndex + 1);
          const responseBody = bodyLines.join('\r\n').trim();

          if (!responseBody) {
            resolve(undefined as T);
            return;
          }

          resolve(JSON.parse(responseBody));
        } catch (error) {
          reject(error);
        }
      });

      client.on('error', (error) => {
        reject(error);
      });
    });
  }
}
