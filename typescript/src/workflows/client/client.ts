import createClient, { type Client as ApiClient } from 'openapi-fetch';
import { AbortError, ClientError, RenderError, ServerError } from './errors.js';
import type { paths } from './schema.js';
import { SSEClient } from './sse.js';
import type {
  ClientOptions,
  ListTaskRunsParams,
  TaskData,
  TaskIdentifier,
  TaskRun,
  TaskRunDetails,
} from './types.js';

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
export class Client {
  public readonly sse: SSEClient;
  public readonly apiClient: ApiClient<paths>;

  /**
   * Create a new Render SDK client
   * @param options Client configuration options
   * @returns New client instance
   */
  constructor(options?: ClientOptions) {
    // Determine base URL
    let baseUrl: string;
    const useLocalDev = options?.useLocalDev ?? process.env.RENDER_USE_LOCAL_DEV === 'true';

    if (useLocalDev) {
      baseUrl = options?.localDevUrl || process.env.RENDER_LOCAL_DEV_URL || 'http://localhost:8120';
    } else {
      baseUrl = options?.baseUrl || 'https://api.render.com';
    }

    // Get token
    const token = options?.token || process.env.RENDER_API_KEY;
    if (!token) {
      throw new RenderError(
        'API token is required. Provide it via options.token or RENDER_API_KEY environment variable.'
      );
    }

    this.sse = new SSEClient(baseUrl, token);
    this.apiClient = createClient<paths>({
      baseUrl: `${baseUrl}/v1`,
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  }

  async runTask(
    taskIdentifier: TaskIdentifier,
    inputData: TaskData,
    signal?: AbortSignal
  ): Promise<TaskRunDetails> {
    if (signal?.aborted) {
      throw new AbortError();
    }

    let taskRunId: string | null = null;
    const abortHandler = async () => {
      if (taskRunId) {
        await this.cancelTaskRun(taskRunId);
        throw new AbortError();
      }
    };

    try {
      // Register abort handler before making the request
      signal?.addEventListener('abort', abortHandler);

      const { data, error, response } = await this.apiClient.POST('/task-runs', {
        body: {
          task: taskIdentifier,
          input: inputData,
        },
        signal,
      });

      if (error) {
        handleApiError(error, response, 'Failed to run task');
      }

      taskRunId = data.id;

      // Pass signal to waitForTask so it can handle cancellation during wait
      return await this.waitForTask(data.id, signal);
    } catch (err) {
      // Handle DOMException AbortError from fetch
      if (err instanceof DOMException && err.name === 'AbortError') {
        throw new AbortError();
      }
      throw err;
    } finally {
      signal?.removeEventListener('abort', abortHandler);
    }
  }

  private async waitForTask(taskRunId: string, signal?: AbortSignal): Promise<TaskRunDetails> {
    return this.sse.waitOnTaskRun(taskRunId, signal);
  }

  /**
   * Get task run details by ID
   * @param taskRunId Task run ID
   * @returns Task run details
   */

  async getTaskRun(taskRunId: string): Promise<TaskRunDetails> {
    const { data, error, response } = await this.apiClient.GET('/task-runs/{taskRunId}', {
      params: { path: { taskRunId } },
    });
    if (error) {
      handleApiError(error, response, 'Failed to get task run');
    }
    return data;
  }

  /**
   * Cancel a task run
   * @param taskRunId Task run ID
   */

  private async cancelTaskRun(taskRunId: string): Promise<void> {
    const { error, response } = await this.apiClient.DELETE('/task-runs/{taskRunId}', {
      params: { path: { taskRunId } },
    });
    if (error) {
      handleApiError(error, response, 'Failed to cancel task run');
    }
  }

  /**
   * List task runs with optional filters
   * @param params Filter parameters
   * @returns List of task runs
   */

  async listTaskRuns(params: ListTaskRunsParams): Promise<TaskRun[]> {
    const { data, error, response } = await this.apiClient.GET('/task-runs', {
      params: { query: params },
    });
    if (error) {
      handleApiError(error, response, 'Failed to list task runs');
    }
    return data;
  }
}
